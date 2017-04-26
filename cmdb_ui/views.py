# coding = utf-8
#

import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import authenticate
from cmdb.models import User, UserGroup, Asset, AssetGroup, IDC, AssetType
from cmdb_api.utils import encrypt_pwd
from .utils import require_login, get_username, clean_asset_form_data, pages, clean_form_data
from cmdb_api.serializers import (ServerAssetCreateUpdateSerializer, NetDeviceAssetCreateUpdateSerializer,
                                  AssetGroupSerializer, IDCSerializer, UserSerializer, UserGroupSerializer)
from .forms import UserForm, AssetForm, ServerForm, NetworkDeviceForm
from datetime import datetime
# Create your views here.


@ensure_csrf_cookie
@require_login
def index(request):
    # return HttpResponse('welcome ' + request.session['user'])
    username, realname = get_username(request.session['uid'])
    vtypes = AssetType.objects.filter(Q(name='虚拟机') | Q(name='云主机'))
    ptypes = AssetType.objects.filter(Q(name='物理机') | Q(name='服务器'))
    vids, pids = [vt.id for vt in vtypes], [pt.id for pt in ptypes]

    user_number = User.objects.count()
    usergroup_number = UserGroup.objects.count()

    assets_number = Asset.objects.count()
    vhosts_number = Asset.objects.filter(asset_type__id__in=vids).count()
    phosts_number = Asset.objects.filter(asset_type_id__in=pids).count()

    hostgroup_number = AssetGroup.objects.count()
    idc_number = IDC.objects.count()

    if username and realname:
        return render(request, 'statistics.html', locals())
    return HttpResponseRedirect(reverse('cmdb_ui:login'))


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username', '')).first()
        if not user:
            return JsonResponse({'status': 404})

        if encrypt_pwd(request.POST.get('password', '')) == user.password:
            request.session['username'] = user.username
            request.session['uid'] = user.id
            return JsonResponse({'status': 200, 'url': reverse('cmdb_ui:index')})
        return JsonResponse({'status': 400})
    return render(request, 'login.html')


@require_login
def logout(request):
    request.session.flush()
    response = HttpResponseRedirect(reverse('cmdb_ui:login'))
    response.delete_cookie('csrftoken')
    return response


@require_login
def asset_list(request, page_num):
    username, realname = get_username(request.session['uid'])
    servers = ('服务器', '云主机', '虚拟机')

    # delete operation
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids is None:
            return JsonResponse({'code': 400, 'msg': 'request error, not receive any data'},
                                status=400)
        try:
            idlist = [int(i) for i in json.loads(ids)]
            Asset.objects.filter(id__in=idlist).delete()
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
        return JsonResponse({'code': 200, 'msg': 'delete ok'}, status=200)

    # search and list
    page_total_item_num = 30
    if page_num is None:
        page_num = 1
    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = Asset.objects.filter(Q(server__hostname__contains=keyword) |
                                        Q(server__lan_ip=keyword) |
                                        Q(networkdevice__name__contains=keyword))
        start, end, page_html = pages(queryset, page_num, '/asset_list',
                                      page_total_item_num, keyword=keyword)
    else:
        queryset = Asset.objects.all()
        start, end, page_html = pages(queryset, page_num, '/asset_list',
                                      page_total_item_num)
    assets = queryset[start:end]
    return render(request, 'asset_list.html', locals())


@require_login
def asset_add(request):
    username, realname = get_username(request.session['uid'])
    asset_types = AssetType.objects.order_by('id')
    idcs = IDC.objects.order_by('id')
    usergroups = UserGroup.objects.order_by('id')
    assetgroups = AssetGroup.objects.order_by('id')

    if request.method == 'POST':
        data, errors = clean_asset_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_add.html', locals())

        if data['route'] == 'server':
            [data.pop(k) for k in ['networkdevice', 'route', 'csrfmiddlewaretoken']]
            serial = ServerAssetCreateUpdateSerializer(data=data)
        else:
            [data.pop(k) for k in ['server', 'route', 'csrfmiddlewaretoken']]
            serial = NetDeviceAssetCreateUpdateSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_add.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'asset_add.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_add.html', locals())


@require_login
def asset_edit(request, asset_id):
    username, realname = get_username(request.session['uid'])
    asset_types = AssetType.objects.order_by('id')
    idcs = IDC.objects.order_by('id')
    usergroups = UserGroup.objects.order_by('id')
    assetgroups = AssetGroup.objects.order_by('id')

    try:
        pk = int(asset_id)
        asset = Asset.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'asset_edit_server.html', locals())
    
    if asset.asset_type.name in ['服务器', '虚拟机', '云主机']:
        route = 'server'
    else:
        route = 'networkdevice'

    if request.method == 'POST':
        data, errors = clean_asset_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_edit_{0}.html'.format(route), locals())

        if route == 'server':
            [data.pop(k) for k in ['networkdevice', 'route', 'csrfmiddlewaretoken']]
            serial = ServerAssetCreateUpdateSerializer(asset, data=data)
        else:
            [data.pop(k) for k in ['server', 'route', 'csrfmiddlewaretoken']]
            serial = NetDeviceAssetCreateUpdateSerializer(asset, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_edit_{0}.html'.format(route), locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_edit_{0}.html'.format(route), locals())


@require_login
def asset_detail(request, asset_id):
    username, realname = get_username(request.session['uid'])
    servers = ('服务器', '云主机', '虚拟机')

    try:
        pk = int(asset_id)
        asset = Asset.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        raise Http404

    if asset.state == 1:
        active_time = datetime.now(asset.create_time.tzinfo) - asset.create_time
    else:
        active_time = asset.update_time - asset.create_time
    return render(request, 'asset_detail.html', locals())


@require_login
def assetgroup_list(request, page_num):
    username, realname = get_username(request.session['uid'])

    # delete operation
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids is None:
            return JsonResponse({'code': 400, 'msg': 'request error, not receive any data'},
                                status=400)
        try:
            idlist = [int(i) for i in json.loads(ids)]
            AssetGroup.objects.filter(id__in=idlist).delete()
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
        return JsonResponse({'code': 200, 'msg': 'delete ok'}, status=200)

    # search and list
    page_total_item_num = 10
    if page_num is None:
        page_num = 1
    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = AssetGroup.objects.filter(groupname__contains=keyword)
        start, end, page_html = pages(queryset, page_num, '/assetgroup_list',
                                      page_total_item_num, keyword=keyword)
    else:
        queryset = AssetGroup.objects.all()
        start, end, page_html = pages(queryset, page_num, '/assetgroup_list',
                                      page_total_item_num)

    assetgroups = queryset[start:end]
    return render(request, 'assetgroup_list.html', locals())


@require_login
def assetgroup_add(request):
    username, realname = get_username(request.session['uid'])

    if request.method == 'POST':
        data, errors = clean_form_data(request, AssetGroup)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'assetgroup_add.html', locals())

        serial = AssetGroupSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'assetgroup_add.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'assetgroup_add.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'assetgroup_add.html', locals())


@require_login
def assetgroup_edit(request, assetgroup_id):
    username, realname = get_username(request.session['uid'])

    try:
        pk = int(assetgroup_id)
        assetgroup = AssetGroup.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'assetgroup_edit.html', locals())

    if request.method == 'POST':
        data, errors = clean_form_data(request, AssetGroup)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'assetgroup_edit.html', locals())

        serial = AssetGroupSerializer(assetgroup, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'assetgroup_edit.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'assetgroup_edit.html', locals())


@require_login
def idc_list(request, page_num):
    username, realname = get_username(request.session['uid'])

    # delete operation
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids is None:
            return JsonResponse({'code': 400, 'msg': 'request error, not receive any data'},
                                status=400)
        try:
            idlist = [int(i) for i in json.loads(ids)]
            IDC.objects.filter(id__in=idlist).delete()
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
        return JsonResponse({'code': 200, 'msg': 'delete ok'}, status=200)

    # search and list
    page_total_item_num = 10
    if page_num is None:
        page_num = 1
    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = IDC.objects.filter(name__contains=keyword)
        start, end, page_html = pages(queryset, page_num, '/idc_list',
                                      page_total_item_num, keyword=keyword)
    else:
        queryset = IDC.objects.all()
        start, end, page_html = pages(queryset, page_num, '/idc_list',
                                      page_total_item_num)

    idcs = queryset[start:end]
    return render(request, 'idc_list.html', locals())


@require_login
def idc_add(request):
    username, realname = get_username(request.session['uid'])

    if request.method == 'POST':
        data, errors = clean_form_data(request, IDC)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'idc_add.html', locals())

        serial = IDCSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'idc_add.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'idc_add.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'idc_add.html', locals())


@require_login
def idc_edit(request, idc_id):
    username, realname = get_username(request.session['uid'])

    try:
        pk = int(idc_id)
        idc = IDC.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'idc_edit.html', locals())

    if request.method == 'POST':
        data, errors = clean_form_data(request, IDC)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'idc_edit.html', locals())

        serial = IDCSerializer(idc, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'idc_edit.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'idc_edit.html', locals())


@require_login
def user_list(request, page_num):
    username, realname = get_username(request.session['uid'])

    # delete operation
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids is None:
            return JsonResponse({'code': 400, 'msg': 'request error, not receive any data'},
                                status=400)
        try:
            idlist = [int(i) for i in json.loads(ids)]
            User.objects.filter(id__in=idlist).delete()
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
        return JsonResponse({'code': 200, 'msg': 'delete ok'}, status=200)

    # search and list
    page_total_item_num = 10
    if page_num is None:
        page_num = 1
    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = User.objects.filter(Q(username__contains=keyword) |
                                       Q(realname__contains=keyword))
        start, end, page_html = pages(queryset, page_num, '/user_list',
                                      page_total_item_num, keyword=keyword)
    else:
        queryset = User.objects.all()
        start, end, page_html = pages(queryset, page_num, '/user_list',
                                      page_total_item_num)

    users = queryset[start:end]
    return render(request, 'user_list.html', locals())



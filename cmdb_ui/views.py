# coding = utf-8
#

import json
from collections import ChainMap
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
# from django.contrib.auth import authenticate
from cmdb.models import (User, Asset, IDC, History, BusinessLine, NetworkInterface, Memory, CPU,
                         HWSystem, Disk)
from cmdb_api.utils import encrypt_pwd
from .utils import (require_login, get_username, clean_server_form_data, pages, clean_form_data,
                    clean_networkdevice_form_data, Cabinet)
from cmdb_api.serializers import (ServerAssetCreateUpdateSerializer, NetDeviceAssetCreateUpdateSerializer,
                                  IDCSerializer, UserSerializer, BusinessLineSerializer)
# from .forms import UserForm, AssetForm, ServerForm, NetworkDeviceForm
from datetime import datetime
# Create your views here.


@ensure_csrf_cookie
@require_login
def index(request):
    username, realname = get_username(request.session['uid'])

    user_number = User.objects.count()
    assets_number = Asset.objects.count()
    vhosts_number = Asset.objects.filter(Q(asset_type='虚拟机') | Q(asset_type='云主机')).count()
    phosts_number = Asset.objects.filter(asset_type='服务器').count()

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
def asset_add_server(request):
    username, realname = get_username(request.session['uid'])
    idcs = IDC.objects.order_by('id')
    users = User.objects.order_by('id')
    business_line = BusinessLine.objects.order_by('id')

    if request.method == 'POST':
        data, errors = clean_server_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_add_server.html', locals())

        data.pop('csrfmiddlewaretoken')
        serial = ServerAssetCreateUpdateSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_add_server.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'asset_add_server.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_add_server.html', locals())


@require_login
def asset_add_networkdevice(request):
    username, realname = get_username(request.session['uid'])
    idcs = IDC.objects.order_by('id')
    users = User.objects.order_by('id')
    business_line = BusinessLine.objects.order_by('id')

    if request.method == 'POST':
        data, errors = clean_networkdevice_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_add_networkdevice.html', locals())

        data.pop('csrfmiddlewaretoken')
        serial = NetDeviceAssetCreateUpdateSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_add_networkdevice.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'asset_add_networkdevice.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_add_networkdevice.html', locals())


@require_login
def asset_edit_server(request, asset_id):
    username, realname = get_username(request.session['uid'])
    idcs = IDC.objects.order_by('id')
    users = User.objects.order_by('id')
    business_line = BusinessLine.objects.order_by('id')

    try:
        pk = int(asset_id)
        asset = Asset.objects.get(pk=pk)
        networkinterface = NetworkInterface.objects.filter(server=asset.server.id).order_by('name')
        memory = Memory.objects.filter(server=asset.server.id)
        cpu = CPU.objects.filter(server=asset.server.id).order_by('socket')
        disk = Disk.objects.filter(server=asset.server.id)
        hw_system = HWSystem.objects.filter(server=asset.server.id).first()
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'asset_edit_server.html', locals())

    if request.method == 'POST':
        print(request.POST.get('asset_type'))
        data, errors = clean_server_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_edit_server.html', locals())

        data.pop('csrfmiddlewaretoken')
        serial = ServerAssetCreateUpdateSerializer(asset, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_edit_server.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'asset_edit_server.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_edit_server.html', locals())


@require_login
def asset_edit_networkdevice(request, asset_id):
    username, realname = get_username(request.session['uid'])
    idcs = IDC.objects.order_by('id')
    users = User.objects.order_by('id')
    business_line = BusinessLine.objects.order_by('id')

    try:
        pk = int(asset_id)
        asset = Asset.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'asset_edit_networkdevice.html', locals())

    if request.method == 'POST':
        data, errors = clean_networkdevice_form_data(request, Asset)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'asset_edit_networkdevice.html', locals())

        data.pop('csrfmiddlewaretoken')
        serial = NetDeviceAssetCreateUpdateSerializer(asset, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'asset_edit_networkdevice.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'asset_edit_networkdevice.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'asset_edit_networkdevice.html', locals())


@require_login
def asset_detail(request, asset_id):
    username, realname = get_username(request.session['uid'])
    servers = ('服务器', '云主机', '虚拟机')
    networkinterfaces, memorys = [], []
    cpus, disks, hw_system = [], [], []

    try:
        pk = int(asset_id)
        asset = Asset.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        raise Http404

    historys = History.objects.filter(asset=asset).order_by('-id')
    if asset.asset_type in servers:
        networkinterfaces = asset.server.networkinterface.all()
        memorys = asset.server.memory.all()
        cpus = asset.server.cpu.all()
        disks = asset.server.disk.all()
        hw_system = asset.server.hw_system.all()

    if asset.state == 1:
        active_time = datetime.now(asset.create_time.tzinfo) - asset.create_time
    else:
        active_time = asset.update_time - asset.create_time
    return render(request, 'asset_detail.html', locals())


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
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'idc_edit.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'idc_edit.html', locals())


@require_login
def idc_diagram(request, idc_id):
    username, realname = get_username(request.session['uid'])
    position_count = tuple(reversed(range(1, 43)))
    servers = ('服务器', '云主机', '虚拟机')

    try:
        pk = int(idc_id)
        idc = IDC.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        return render(request, 'idc_diagram.html', locals())

    queryset = Asset.objects.filter(idc=idc.id, cabinet_number__isnull=False)
    cabinets = []
    for i in queryset.values('cabinet_number').annotate(Count('cabinet_number')):
        cabinets.append(Cabinet(i['cabinet_number'],
                                queryset.filter(cabinet_number=i['cabinet_number'])))

    return render(request, 'idc_diagram.html', locals())


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
            if 1 in idlist:
                return JsonResponse({'code': 403, 'msg': '不能删除 admin 用户'}, status=403)
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


@require_login
def user_add(request):
    username, realname = get_username(request.session['uid'])

    if request.method == 'POST':
        data, errors = clean_form_data(request, User, multikey=('usergroup', ))
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'user_add.html', locals())

        data['password'] = encrypt_pwd(data['password'])

        serial = UserSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'user_add.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'user_add.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'user_add.html', locals())


@require_login
def user_edit(request, user_id):
    username, realname = get_username(request.session['uid'])

    try:
        pk = int(user_id)
        user = User.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'user_edit.html', locals())

    if request.method == 'POST':
        data, errors = clean_form_data(request, User, multikey=('usergroup', ))
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'user_edit.html', locals())

        if data['password'] == user.password[:20]:
            data.pop('password')
        else:
            data['password'] = encrypt_pwd(data['password'])

        # disable to change username.
        if data.get('username'):
            hidden_success, errors = 'hidden', '不能修改用户名'
            return render(request, 'user_edit.html', locals())

        serial = UserSerializer(user, data=data, partial=True)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'user_edit.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'user_edit.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'user_edit.html', locals())


@require_login
def user_detail(request, user_id):
    username, realname = get_username(request.session['uid'])
    servers = ('服务器', '云主机', '虚拟机')
    try:
        pk = int(user_id)
        user = User.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        raise Http404

    groups = user.usergroup.all()
    assetgroups = (group.assetgroup.all() for group in groups)
    asset_querysets = set(group.asset_set.all() for group in groups)
    if len(asset_querysets) < 10:
        asset_querysets.update(set(group.asset_set.all() for group in ChainMap(*assetgroups)))
    assets = ChainMap(*asset_querysets)
    return render(request, 'user_detail.html', locals())


@require_login
def business_line_list(request, page_num):
    username, realname = get_username(request.session['uid'])

    # delete operation
    if request.method == 'POST':
        ids = request.POST.get('ids')
        if ids is None:
            return JsonResponse({'code': 400, 'msg': 'request error, not receive any data'},
                                status=400)
        try:
            idlist = [int(i) for i in json.loads(ids)]
            if 1 in idlist:
                return JsonResponse({'code': 403, 'msg': '不能删除 管理员组'}, status=403)
            BusinessLine.objects.filter(id__in=idlist).delete()
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
        return JsonResponse({'code': 200, 'msg': 'delete ok'}, status=200)

    # search and list
    page_total_item_num = 10
    if page_num is None:
        page_num = 1
    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = BusinessLine.objects.filter(name__contains=keyword)
        start, end, page_html = pages(queryset, page_num, '/business_list_line',
                                      page_total_item_num, keyword=keyword)
    else:
        queryset = BusinessLine.objects.all()
        start, end, page_html = pages(queryset, page_num, '/business_list_line',
                                      page_total_item_num)

    business_line = queryset[start:end]
    return render(request, 'business_line_list.html', locals())


@require_login
def business_line_add(request):
    username, realname = get_username(request.session['uid'])

    if request.method == 'POST':
        data, errors = clean_form_data(request, BusinessLine)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'business_line_add.html', locals())

        serial = BusinessLineSerializer(data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'business_line_add.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'business_line_add.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'business_line_add.html', locals())


@require_login
def business_line_edit(request, usergroup_id):
    username, realname = get_username(request.session['uid'])

    try:
        pk = int(usergroup_id)
        usergroup = BusinessLine.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        hidden_success, errors = 'hidden', str(e)
        return render(request, 'business_line_edit.html', locals())

    if request.method == 'POST':
        data, errors = clean_form_data(request, BusinessLine)
        if errors is not None:
            hidden_success = 'hidden'
            return render(request, 'business_line_edit.html', locals())

        serial = BusinessLineSerializer(usergroup, data=data)
        if serial.is_valid():
            serial.save()
            hidden_failed = 'hidden'
            return render(request, 'business_line_edit.html', locals())
        hidden_success, errors = 'hidden', serial.errors
        return render(request, 'business_line_edit.html', locals())

    hidden_failed = hidden_success = 'hidden'
    return render(request, 'business_line_edit.html', locals())


@require_login
def business_line_detail(request, usergroup_id):
    username, realname = get_username(request.session['uid'])
    servers = ('服务器', '云主机', '虚拟机')
    try:
        pk = int(usergroup_id)
        usergroup = BusinessLine.objects.get(pk=pk)
    except (ValueError, ObjectDoesNotExist) as e:
        raise Http404

    # groups = user.usergroup.all()
    # assetgroups = (group.assetgroup.all() for group in groups)
    # asset_querysets = set(group.asset_set.all() for group in groups)
    # if len(asset_querysets) < 10:
    #     asset_querysets.update(set(group.asset_set.all() for group in ChainMap(*assetgroups)))
    # assets = ChainMap(*asset_querysets)
    return render(request, 'business_line_detail.html', locals())




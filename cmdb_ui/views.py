# coding = utf-8
#

import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import authenticate
from cmdb.models import User, UserGroup, Asset, AssetGroup, IDC, AssetType
from cmdb_api.utils import encrypt_pwd
from .utils import require_login, get_username, Pager, clean_data
from cmdb_api.serializers import ServerAssetCreateUpdateSerializer, NetDeviceAssetCreateUpdateSerializer
from .forms import UserForm, AssetForm, ServerForm, NetworkDeviceForm
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

    username, realname = get_username(request.session['uid'])
    page_total_item_num = 30
    if page_num is None:
        page_num = 1

    keyword = request.GET.get('keyword', None)

    if keyword is not None:
        queryset = Asset.objects.filter(Q(server__hostname__contains=keyword) |
                                        Q(server__lan_ip=keyword) |
                                        Q(networkdevice__name__contains=keyword))
        d, m = divmod(queryset.count(), page_total_item_num)
        total_page = d + (1 if m > 0 else m)
        start, end, page_html = Pager(total_page, int(page_num), '/asset_list',
                                      page_total_item_num, keyword=keyword).page()
        # assets = queryset[start:end]
        # return JsonResponse({'url'})
    else:
        queryset = Asset.objects.all()
        d, m = divmod(queryset.count(), page_total_item_num)
        total_page = d + (1 if m > 0 else m)
        start, end, page_html = Pager(total_page, int(page_num), '/asset_list',
                                      page_total_item_num).page()
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
        data, errors = clean_data(request, Asset)
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

    hidden_failed, hidden_success = 'hidden', 'hidden'
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
        data, errors = clean_data(request, Asset)
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

    hidden_failed, hidden_success = 'hidden', 'hidden'
    return render(request, 'asset_edit_{0}.html'.format(route), locals())


@require_login
def asset_detail(request, asset_id):
    pass


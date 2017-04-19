from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth import authenticate
from cmdb.models import User, UserGroup, Asset, AssetGroup, IDC, AssetType
from cmdb_api.utils import encrypt_pwd
from .utils import require_login, get_username, Pager
# Create your views here.


@require_login
def index(request):
    # return HttpResponse('welcome ' + request.session['user'])
    username, realname = get_username(request.session['uid'])
    vtypes = AssetType.objects.filter(Q(name='虚拟机') | Q(name='云主机'))
    ptypes = AssetType.objects.filter(Q(name='物理机') | Q(name='服务器'))

    user_number = User.objects.count()
    usergroup_number = UserGroup.objects.count()

    assets_number = Asset.objects.count()
    vhosts_number = Asset.objects.filter(Q(asset_type=vtypes[0].id) | Q(asset_type=vtypes[1].id)).count()
    phosts_number = Asset.objects.filter(Q(asset_type=ptypes[0].id) | Q(asset_type=ptypes[1].id)).count()

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
    return HttpResponseRedirect(reverse('cmdb_ui:login'))


@require_login
def asset_list(request, page_num):
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
    else:
        queryset = Asset.objects.all()
        d, m = divmod(queryset.count(), page_total_item_num)
        total_page = d + (1 if m > 0 else m)
        start, end, page_html = Pager(total_page, int(page_num), '/asset_list',
                                      page_total_item_num).page()
    assets = queryset[start:end]
    return render(request, 'asset_list.html', locals())


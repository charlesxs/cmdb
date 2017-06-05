# coding=utf-8
#

from cmdb_api.mixins import IdNameConvertMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from collections import defaultdict
from urllib.parse import urlencode
from cmdb.models import User
from copy import deepcopy


def require_login(fn):
    def inner(request, *args, **kwargs):
        username = request.session.get('username', None)
        if username is None:
            return HttpResponseRedirect(reverse('cmdb_ui:login'))
        return fn(request, *args, **kwargs)
    return inner


def get_username(id_):
    user = User.objects.filter(id=id_).first()
    if user:
        return user.username, user.realname
    return None, None


class CacheServerData:
    # 设置每个资源的唯一标识 ，后面判断如果唯一标识是None, 则删除这条记录.
    IdentityMap = {
        'memory': 'serialnum',
        'disk': 'locator',
        'cpu': 'socket',
        'hw_system': 'serialnum',
        'networkinterface': 'mac'
    }

    def __init__(self):
        self.networkinterface = defaultdict(dict)
        self.memory = defaultdict(dict)
        self.cpu = defaultdict(dict)
        self.disk = defaultdict(dict)
        self.hw_system = defaultdict(dict)

    def cache_networkinterface(self, identity, k, v):
        if k == 'state':
            v = int(v)
        self.networkinterface[identity].update({k: v})

    def get_networkinterface(self):
        values = list(self.networkinterface.values())
        result = deepcopy(values)
        [result.remove(v) for v in values if v[CacheServerData.IdentityMap['networkinterface']] is None]
        return result

    def cache_memory(self, identity, k, v):
        self.memory[identity].update({k: v})

    def get_memory(self):
        values = list(self.memory.values())
        result = deepcopy(values)
        [result.remove(v) for v in values if v[CacheServerData.IdentityMap['memory']] is None]
        return result

    def cache_cpu(self, identity, k, v):
        self.cpu[identity].update({k: v})

    def get_cpu(self):
        values = list(self.cpu.values())
        result = deepcopy(values)
        [result.remove(v) for v in values if v[CacheServerData.IdentityMap['cpu']] is None]
        return result

    def cache_disk(self, identity, k, v):
        self.disk[identity].update({k: v})

    def get_disk(self):
        values = list(self.disk.values())
        result = deepcopy(values)
        [result.remove(v) for v in values if v[CacheServerData.IdentityMap['disk']] is None]
        return result

    def cache_hw_system(self, identity, k, v):
        self.hw_system[identity].update({k: v})

    def get_hw_system(self):
        values = list(self.hw_system.values())
        result = deepcopy(values)
        [result.remove(v) for v in values if v[CacheServerData.IdentityMap['hw_system']] is None]
        return result


def clean_server_form_data(request, model):
    cache = CacheServerData()
    business_line = request.POST.getlist('business_line')
    business_line = business_line if business_line else []
    print(business_line)

    data = {
        'server': {},
        'business_line': business_line
    }

    for k, v in request.POST.items():
        if k.startswith('server'):
            data['server'][k.split('-')[-1]] = v if v else None
        elif (k.startswith('networkinterface') or k.startswith('memory') or
              k.startswith('cpu') or k.startswith('hw_system') or k.startswith('disk')):
            _type, identity, field_name = k.split('-')
            getattr(cache, 'cache_{0}'.format(_type))(identity, field_name, v if v else None)
        elif k != 'business_line':
            data[k] = v if v else None

    try:
        data = IdNameConvertMixin().to_id(data, model)
        data['server']['networkinterface'] = cache.get_networkinterface()
        data['server']['cpu'] = cache.get_cpu()
        data['server']['memory'] = cache.get_memory()
        data['server']['hw_system'] = cache.get_hw_system()
        data['server']['disk'] = cache.get_disk()
    except (ValueError, TypeError) as e:
        return data, str(e)
    print(data)
    return data, None


def clean_form_data(request, model, multikey=()):
    data = {}
    for k, v in request.POST.items():
        if k in multikey:
            data[k] = request.POST.getlist(k)
        else:
            data[k] = v if v else None
    try:
        data = IdNameConvertMixin().to_id(data, model)
    except ValueError as e:
        return data, str(e)
    return data, None


class Pager:
    num_html = '<li><a href="%s">%d</a></li>'
    more_html = '<li><a href="%s">...</a></li>'
    pre_button = '<li><a href="%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
    next_button = '<li> <a href="%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'

    def __init__(self, total_page, page_num, uri, page_total_item_num=10, **searchargs):
        self.total_page = total_page
        self.page_num = page_num
        self.uri = uri
        self.page_total_item_num = page_total_item_num
        self.searchargs = searchargs

    def url(self, num):
        page_url = '/'.join([self.uri, str(num), ""])
        if self.searchargs['keyword'] is not None:
            return page_url + '?' + urlencode(self.searchargs)
        return page_url

    def _page(self):
        total_html = []
        if self.total_page > 7:
            if self.page_num <= 4:
                [total_html.append(Pager.num_html % (self.url(i), i)) for i in range(1, 6)]
                total_html.append(Pager.more_html % self.url(6))
                total_html.append(Pager.num_html % (self.url(self.total_page), self.total_page))

            elif self.total_page - self.page_num + 1 <= 4:
                total_html.append(Pager.num_html % (self.url(1), 1))
                total_html.append(Pager.more_html % self.url(self.total_page - 5))
                for i in range(self.total_page - 5 + 1, self.total_page + 1):
                    total_html.append(Pager.num_html % (self.url(i), i))

            else:
                total_html.append(Pager.num_html % (self.url(1), 1))
                total_html.append(Pager.more_html % self.url(self.page_num - 2))
                for i in range(3):
                    total_html.append(Pager.num_html % (self.url(self.page_num - 1 + i), self.page_num - 1 + i))
                total_html.append(Pager.more_html % self.url(self.page_num + 2))
                total_html.append(Pager.num_html % (self.url(self.total_page), self.total_page))
        else:
            [total_html.append(Pager.num_html % (self.url(i), i)) for i in range(1, self.total_page + 1)]

        # add pre, next button
        if self.page_num == 1:
            total_html.insert(0, Pager.pre_button % self.url(1))
        else:
            total_html.insert(0, Pager.pre_button % self.url(self.page_num - 1))

        if self.page_num == self.total_page:
            total_html.append(Pager.next_button % self.url(self.page_num))
        else:
            total_html.append(Pager.next_button % self.url(self.page_num + 1))
        return total_html

    def page(self):
        html = mark_safe(' '.join(self._page()))
        start = (self.page_num - 1) * self.page_total_item_num
        end = start + self.page_total_item_num
        return start, end, html


def pages(queryset, page_num, uri, page_total_item_num, keyword=None):
    d, m = divmod(queryset.count(), page_total_item_num)
    total_page = d + (1 if m > 0 else m)
    start, end, page_html = Pager(total_page, int(page_num), uri,
                                  page_total_item_num, keyword=keyword).page()
    return start, end, page_html

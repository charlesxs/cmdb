# coding=utf-8
#

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
from cmdb.models import User


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
        if self.searchargs:
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




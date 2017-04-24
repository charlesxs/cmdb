from django.conf.urls import url
from .views import login, index, logout, asset_list, asset_add, asset_edit, asset_detail


urlpatterns = {
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^asset_list/(?P<page_num>[0-9]+)?/?$', asset_list, name='asset_list'),
    url(r'^asset_add/$', asset_add, name='asset_add'),
    url(r'^asset_edit/(?P<asset_id>[0-9]+)/$', asset_edit, name='asset_edit'),
    url(r'^asset_detail/(?P<asset_id>[0-9]+)/$', asset_detail, name='asset_detail')
}
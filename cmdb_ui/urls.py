from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^asset_list/(?P<page_num>[0-9]+)?/?$', asset_list, name='asset_list'),
    url(r'^asset_add_server/$', asset_add_server, name='asset_add_server'),
    url(r'^asset_add_networkdevice/$', asset_add_networkdevice, name='asset_add_networkdevice'),
    url(r'^asset_edit_server/(?P<asset_id>[0-9]+)/$', asset_edit_server, name='asset_edit_server'),
    url(r'^asset_edit_networkdevice/(?P<asset_id>[0-9]+)/$', asset_edit_networkdevice, name='asset_edit_networkdevice'),
    url(r'^asset_detail/(?P<asset_id>[0-9]+)/$', asset_detail, name='asset_detail'),

    url(r'^idc_list/(?P<page_num>[0-9]+)?/?$', idc_list, name='idc_list'),
    url(r'^idc_add/$', idc_add, name='idc_add'),
    url(r'^idc_edit/(?P<idc_id>[0-9]+)/$', idc_edit, name='idc_edit'),

    url(r'^user_list/(?P<page_num>[0-9]+)?/?$', user_list, name='user_list'),
    url(r'^user_add/$', user_add, name='user_add'),
    url(r'^user_edit/(?P<user_id>[0-9]+)/$', user_edit, name='user_edit'),
    url(r'^user_detail/(?P<user_id>[0-9]+)/$', user_detail, name='user_detail'),

    url(r'^usergroup_list/(?P<page_num>[0-9]+)?/?$', usergroup_list, name='usergroup_list'),
    url(r'^usergroup_add/$', usergroup_add, name='usergroup_add'),
    url(r'^usergroup_edit/(?P<usergroup_id>[0-9]+)/$', usergroup_edit, name='usergroup_edit'),
    url(r'^usergroup_detail/(?P<usergroup_id>[0-9]+)/$', usergroup_detail, name='usergroup_detail'),

]

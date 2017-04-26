from django.conf.urls import url
from .views import (login, index, logout, asset_list,
                    asset_add, asset_edit, asset_detail, assetgroup_list,
                    assetgroup_add, assetgroup_edit, idc_list, idc_add, idc_edit,
                    user_list)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^asset_list/(?P<page_num>[0-9]+)?/?$', asset_list, name='asset_list'),
    url(r'^asset_add/$', asset_add, name='asset_add'),
    url(r'^asset_edit/(?P<asset_id>[0-9]+)/$', asset_edit, name='asset_edit'),
    url(r'^asset_detail/(?P<asset_id>[0-9]+)/$', asset_detail, name='asset_detail'),

    url(r'^assetgroup_list/(?P<page_num>[0-9]+)?/?$', assetgroup_list, name='assetgroup_List'),
    url(r'^assetgroup_add/$', assetgroup_add, name='assetgroup_add'),
    url(r'^assetgroup_edit/(?P<assetgroup_id>[0-9]+)/$', assetgroup_edit, name='assetgroup_edit'),

    url(r'^idc_list/(?P<page_num>[0-9]+)?/?$', idc_list, name='idc_list'),
    url(r'^idc_add/$', idc_add, name='idc_add'),
    url(r'^idc_edit/(?P<idc_id>[0-9]+)/$', idc_edit, name='idc_edit'),

    url(r'^user_list/(?P<page_num>[0-9]+)?/?$', user_list, name='user_list'),

]

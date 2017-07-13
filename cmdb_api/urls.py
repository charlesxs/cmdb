from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (AssetListCreate, AssetListAll, AssetDetail, Search,
                    UserViewSet, IDCViewSet, BusinessLineViewSet)

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

idc_list = IDCViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

idc_detail = IDCViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

business_line_list = BusinessLineViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

business_line_detail = BusinessLineViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'idc', IDCViewSet)
router.register(r'business_line', BusinessLineViewSet)

urlpatterns = [
    url(r'^asset/$', AssetListCreate.as_view(), name='asset_list_create'),
    url(r'^asset/_all/$', AssetListAll.as_view(), name='asset_list_all'),
    url(r'^asset/(?P<pk>[0-9]+)/$', AssetDetail.as_view(), name='asset_detail'),
    url(r'^search/', Search.as_view(), name="search"),
    url(r'^', include(router.urls))
]

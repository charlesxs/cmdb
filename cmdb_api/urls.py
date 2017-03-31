from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (AssetListCreate, AssetListAll, AssetDetail,
                    AssetGroupViewSet, AssetTypeViewSet, UserViewSet,
                    UserGroupViewSet, IDCViewSet)

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

usergroup_list = UserGroupViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

usergroup_detail = UserGroupViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

assetgroup_list = AssetGroupViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

assetgroup_detail = AssetGroupViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

assettype_list = AssetTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

assettype_detail = AssetTypeViewSet.as_view({
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


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'usergroup', UserGroupViewSet)
router.register(r'assetgroup', AssetGroupViewSet)
router.register(r'assettype', AssetTypeViewSet)
router.register(r'idc', IDCViewSet)

urlpatterns = [
    url(r'^asset/$', AssetListCreate.as_view(), name='asset_list_create'),
    url(r'^asset/_all/$', AssetListAll.as_view(), name='asset_list_all'),
    url(r'^asset/(?P<pk>[0-9]+)/$', AssetDetail.as_view(), name='asset_detail'),
    url(r'^', include(router.urls))
]

# from django.shortcuts import render
from django.http import Http404
# from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import detail_route, list_route
# from rest_framework import mixins, generics
from rest_framework import status
from cmdb.models import Asset, IDC, User, BusinessLine
from .mixins import IdNameConvertMixin, AssetListMixin
from .utils import encrypt_pwd
from .serializers import (ServerAssetCreateUpdateSerializer, NetDeviceAssetCreateUpdateSerializer,
                          UserSerializer, UserListSerializer, IDCSerializer, BusinessLineSerializer)


class AssetListAll(AssetListMixin, APIView):
    def get(self, request):
        return self.list(request)


class AssetListCreate(AssetListMixin, IdNameConvertMixin, APIView):
    def get(self, request):
        return self.list(request, num=10)

    def post(self, request):
        # modify request.data for populate serializer class
        route = 'server'
        data = self.name_to_id(request.data, Asset)
        if data.get('route'):
            route = data.pop('route')

        if route == 'server':
            serial = ServerAssetCreateUpdateSerializer(data=data)
        else:
            serial = NetDeviceAssetCreateUpdateSerializer(data=data)
        if serial.is_valid():
            serial.save()
            return Response(self.id_to_name(serial.data, Asset), status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetDetail(IdNameConvertMixin, APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        asset = self.get_object(pk)
        if asset.asset_type in ('服务器', '虚拟机', '云主机'):
            serial = ServerAssetCreateUpdateSerializer(asset)
        else:
            serial = NetDeviceAssetCreateUpdateSerializer(asset)
        return Response(self.id_to_name(serial.data, Asset))

    def put(self, request, pk):
        asset = self.get_object(pk)
        route = 'server'
        data = self.name_to_id(request.data, Asset)
        if data.get('route'):
            route = data.pop('route')
        if route == 'server':
            s = ServerAssetCreateUpdateSerializer(asset, data=data, partial=True)
        else:
            s = NetDeviceAssetCreateUpdateSerializer(asset, data=data, partial=True)
        if s.is_valid():
            s.save()
            return Response(self.id_to_name(s.data, Asset), status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        return Response({
            'code': 403,
            'reason': 'Can not delete asset, you can mark it as offline'
        }, status=status.HTTP_403_FORBIDDEN)
        # asset = self.get_object(pk)
        # asset.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(IdNameConvertMixin, ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def _convert_post_data(self, request):
        if request.data.get('password'):
            request.data['password'] = encrypt_pwd(request.data.get('password'))
        if request.data.get('usergroup'):
            data = self.name_to_id(request.data, User)
            request.data['usergroup'] = data['usergroup']
        return request

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return Response(self.id_to_name(resp.data, User))

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return Response([self.id_to_name(r, User) for r in resp.data])

    def create(self, request, *args, **kwargs):
        return super().create(self._convert_post_data(request), *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self._convert_post_data(request), *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if kwargs.get('pk') == '1':
            return Response({'detail': 'admin can not be deleted.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class IDCViewSet(IdNameConvertMixin, ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer


class BusinessLineViewSet(ModelViewSet):
    queryset = BusinessLine.objects.all()
    serializer_class = BusinessLineSerializer


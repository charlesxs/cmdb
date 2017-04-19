# coding=utf-8
#

from rest_framework import serializers
from rest_framework.fields import empty
from django.db import transaction
from cmdb.models import (Asset, Server, NetworkDevice, AssetGroup,
                         AssetType, User, UserGroup, Auth, IDC)


class DynamicModelSerializer(serializers.ModelSerializer):
    """
    自定义 Serializer 基类, 动态修改嵌套 serializer, 手动实例化子serializer传入相对应的ORM instance,
    解決了嵌套 serializer 更新问题.

    官方文档:
      http://www.django-rest-framework.org/api-guide/validators/#updating-nested-serializers

    具体类参考:
      rest_framework.serializer.BaseSerializer
      rest_framework.serializer.SerializerMetaclass
      rest_framework.serializer.Serializer

      rest_framework.validators.UniqueValidator --> self.__call__ --> self.exclude_current_instance --> self.set_context
    """
    def __init__(self, instance=None, data=empty, dynamic=False, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.dynamic = dynamic
        if instance and data is not empty:
            for key, serial in self._declared_fields.items():
                if not serial.dynamic:
                    continue
                self._declared_fields[key] = serial.__class__(instance=getattr(instance, key),
                                                              data=data.get(key), **kwargs)


class ServerSerializer(DynamicModelSerializer):
    """
    Server serializer class for list, update server and nested to ServerAssetCreateSerializer class.
    """
    class Meta:
        model = Server
        exclude = ('id', 'asset')


class NetworkDeviceSerializer(DynamicModelSerializer):
    """
    NetworkDevice serializer for list, update Networkdevice and nested to NetDeviceAssetCreateSerializer class.
    """
    class Meta:
        model = NetworkDevice
        exclude = ('id', 'asset')


class ServerAssetCreateUpdateSerializer(DynamicModelSerializer):
    """
    This serializer used for create/update asset with server attribute. overwrite the create method to
    control transaction at create time.
    """
    server = ServerSerializer(read_only=False, dynamic=True, partial=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ('id', )
        # validators = []

    def create(self, validated_data):
        usergroup = {1}
        with transaction.atomic():
            server = validated_data.pop('server')
            if validated_data.get('usergroup'):
                usergroup.update(set(validated_data.pop('usergroup')))
            asset = Asset.objects.create(**validated_data)
            asset.usergroup.add(*usergroup)
            server['asset'] = asset
            Server.objects.create(**server)
            asset.save()
        return asset

    def update(self, instance, validated_data):
        with transaction.atomic():
            usergroup = set()
            if validated_data.get('server'):
                s = validated_data.pop('server')
                [setattr(instance.server, k, v) for k, v in s.items()]
                instance.server.save()
            if validated_data.get('usergroup'):
                usergroup.update(set(validated_data.pop('usergroup')))
            instance.usergroup.add(*usergroup)
            [setattr(instance, k, v) for k, v in validated_data.items()]
            instance.save()
        return instance


class NetDeviceAssetCreateUpdateSerializer(DynamicModelSerializer):
    """
    This is similar to ServerAssetCreateSerializer class.
    """
    networkdevice = NetworkDeviceSerializer(read_only=False, dynamic=True, partial=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ('id', )

    def create(self, validated_data):
        usergroup = {1}
        with transaction.atomic():
            networkdevice = validated_data.pop('networkdevice')
            if validated_data.get('usergroup'):
                usergroup.update(set(validated_data.pop('usergroup')))
            asset = Asset.objects.create(**validated_data)
            asset.usergroup.add(*usergroup)
            networkdevice['asset'] = asset
            NetworkDevice.objects.create(**networkdevice)
            asset.save()
        return asset

    def update(self, instance, validated_data):
        with transaction.atomic():
            usergroup = set()
            if validated_data.get('networkdevice'):
                n = validated_data.pop('networkdevice')
                [setattr(instance.networkdevice, k, v) for k, v in n.items()]
                instance.networkdevice.save()
            if validated_data.get('usergroup'):
                usergroup.update(set(validated_data.pop('usergroup')))
            instance.usergroup.add(*usergroup)
            [setattr(instance, k, v) for k, v in validated_data.items()]
            instance.save()
        return instance


class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        # exclude = ('password', )
        fields = '__all__'


class UserListSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )


class UserGroupSerializer(DynamicModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class AssetGroupSerializer(DynamicModelSerializer):
    class Meta:
        model = AssetGroup
        fields = '__all__'


class IDCSerializer(DynamicModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'


class AssetTypeSerializer(DynamicModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'



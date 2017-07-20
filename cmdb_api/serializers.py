# coding=utf-8
#

import json
from rest_framework import serializers
from rest_framework.fields import empty
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from .utils import is_empty
from cmdb.models import (Asset, Server, NetworkDevice, History, BusinessLine,
                         User, IDC, NetworkInterface, CPU, Memory, Disk, HWSystem)


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
                if not getattr(serial, 'dynamic', None) and getattr(serial, 'many', None):
                    continue
                self._declared_fields[key] = serial.__class__(instance=getattr(instance, key),
                                                              data=data.get(key), **kwargs)


class NetworkInterfaceSerializer(DynamicModelSerializer):
    class Meta:
        model = NetworkInterface
        exclude = ('id', 'server')


class CPUSerializer(DynamicModelSerializer):
    class Meta:
        model = CPU
        exclude = ('id', 'server')


class MemorySerializer(DynamicModelSerializer):
    class Meta:
        model = Memory
        exclude = ('id', 'server')


class DiskSerializer(DynamicModelSerializer):
    class Meta:
        model = Disk
        exclude = ('id', 'server')


class HWSystemSerializer(DynamicModelSerializer):
    class Meta:
        model = HWSystem
        fields = ['serialnum', 'manufacturer', 'product_name', 'uuid']
        # exclude = ('id', 'server')


class ServerSerializer(DynamicModelSerializer):
    """
    Server serializer class for list, update server and nested to ServerAssetCreateSerializer class.
    """
    networkinterface = NetworkInterfaceSerializer(many=True, read_only=False, dynamic=True, partial=True)
    cpu = CPUSerializer(many=True, read_only=False, dynamic=True, partial=True)
    memory = MemorySerializer(many=True, read_only=False, dynamic=True, partial=True)
    disk = DiskSerializer(many=True, read_only=False, dynamic=True, partial=True)
    hw_system = HWSystemSerializer(many=True, read_only=False, dynamic=True, partial=True)

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


def update_current_instance(current_instance, data, instance, model):
    for k, v in data.items():
        old_value = getattr(current_instance, k)
        if old_value != v and not is_empty(v):
            setattr(current_instance, k, v)
            History.objects.create(asset=instance, model=model.__name__, field=model.get_help_text(k),
                                   old=old_value, new=v, operate='u')
    current_instance.save()


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
        with transaction.atomic():
            business_line = set()
            if validated_data.get('business_line', None):
                business_line.update(set(validated_data.pop('business_line')))

            server = validated_data.pop('server')
            asset = Asset.objects.create(**validated_data)
            asset.business_line.add(*business_line)

            networkinterface = server.pop('networkinterface')
            cpu = server.pop('cpu')
            memory = server.pop('memory')
            disk = server.pop('disk')
            hw_system = server.pop('hw_system')

            server['asset'] = asset
            sobj = Server.objects.create(**server)
            # create network interface
            for nt in networkinterface:
                nt['server'] = sobj
                NetworkInterface.objects.create(**nt)

            # create memory
            for m in memory:
                m['server'] = sobj
                Memory.objects.create(**m)

            # create cpu
            for c in cpu:
                c['server'] = sobj
                CPU.objects.create(**c)

            # create disk
            for d in disk:
                d['server'] = sobj
                Disk.objects.create(**d)

            # create hardware system
            for hw in hw_system:
                hw['server'] = sobj
                HWSystem.objects.create(**hw)

            asset.save()
        return asset

    def update(self, instance, validated_data):
        with transaction.atomic():
            if validated_data.get('server'):
                s = validated_data.pop('server')
                if s.get('networkinterface'):
                    self.update_subset(instance, s.pop('networkinterface'), model=NetworkInterface,
                                       serializer_class=NetworkInterfaceSerializer, identity='name')

                if s.get('memory'):
                    self.update_subset(instance, s.pop('memory'), model=Memory,
                                       serializer_class=MemorySerializer, identity='locator')

                if s.get('disk'):
                    self.update_subset(instance, s.pop('disk'), model=Disk,
                                       serializer_class=DiskSerializer, identity='locator')
                if s.get('cpu'):
                    self.update_subset(instance, s.pop('cpu'), model=CPU,
                                       serializer_class=CPUSerializer, identity='socket')

                if s.get('hw_system'):
                    self.update_subset(instance, s.pop('hw_system'), model=HWSystem,
                                       serializer_class=HWSystemSerializer, identity='serialnum')

                # update server
                update_current_instance(instance.server, s, instance, Server)

            if validated_data.get('business_line'):
                business_line = validated_data.pop('business_line')
                old = '、'.join(i.name for i in instance.business_line.all())
                new = '、'.join(b.name for b in business_line)

                if old != new and not is_empty(business_line):
                    History.objects.create(asset=instance, model='BusinessLine', field='业务线',
                                           old=old, new=new)
                    instance.business_line.clear()
                    instance.business_line.add(*business_line)

            update_current_instance(instance, validated_data, instance, Asset)
        return instance

    @staticmethod
    def update_subset(instance, data, model, serializer_class, identity):
        identitys = []
        queryset = model.objects.filter(server=instance.server)
        for d in data:
            identitys.append(d[identity])
            try:
                query_keyword = {identity: d[identity]}
                q = queryset.get(**query_keyword)
                for k, v in d.items():
                    old_value = getattr(q, k)
                    if old_value != v and not is_empty(v):
                        setattr(q, k, v)
                        History.objects.create(asset=instance, model=model.__name__, field=model.get_help_text(k),
                                               old=old_value, new=v, operate='u')
                q.save()
            except ObjectDoesNotExist:
                History.objects.create(asset=instance, model=model.__name__, field='all',
                                       new=json.dumps(d), operate='a')
                d['server'] = instance.server
                model.objects.create(**d)

        # delete
        for q in queryset:
            if getattr(q, identity) not in identitys:
                serial = serializer_class(q)
                History.objects.create(asset=instance, model=model.__name__, field='all',
                                       old=json.dumps(serial.data), operate='d')
                q.delete()


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
        with transaction.atomic():
            business_line = set()
            networkdevice = validated_data.pop('networkdevice')
            if validated_data.get('business_line'):
                business_line.update(set(validated_data.pop('business_line')))
            asset = Asset.objects.create(**validated_data)
            asset.business_line.add(*business_line)
            networkdevice['asset'] = asset
            NetworkDevice.objects.create(**networkdevice)
            asset.save()
        return asset

    def update(self, instance, validated_data):
        with transaction.atomic():
            business_line = set()
            if validated_data.get('networkdevice'):
                n = validated_data.pop('networkdevice')
                update_current_instance(instance.networkdevice, n, instance, NetworkDevice)
            if validated_data.get('business_line'):
                business_line.update(set(validated_data.pop('business_line')))
            instance.business_line.add(*business_line)
            update_current_instance(instance, validated_data, instance, Asset)
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


class IDCSerializer(DynamicModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'
        read_only_fields = ('id',)


class BusinessLineSerializer(DynamicModelSerializer):
    class Meta:
        model = BusinessLine
        fields = '__all__'
        read_only_fields = ('id',)


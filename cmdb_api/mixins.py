# coding = utf-8
from django.http import Http404
from copy import deepcopy
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_models_field_name, fetch_related_field
from .serializers import ServerAssetCreateUpdateSerializer, NetDeviceAssetCreateUpdateSerializer
from .models import Asset


class IdNameConvertMixin:
    @staticmethod
    def search_by_name(model, value):
        name = get_models_field_name(model)
        ret = model.objects.filter(**{name: value}).first()
        if not ret:
            raise Http404(value + 'not found')
        return ret

    @staticmethod
    def search_by_id(model, id_):
        ret = model.objects.filter(id=id_).first()
        if not ret:
            raise Http404
        return ret

    def name_to_id(self, dictdata, model):
        data = deepcopy(dictdata)
        model_map = fetch_related_field(model)
        fields = {k: v for k, v in data.items() if k in model_map.keys()}
        for k, v in fields.items():
            if not isinstance(v, (int, list)) and v is not None:
                query = self.search_by_name(model_map[k], v)
                data[k] = query.id
            elif isinstance(v, list):
                ng = list(map(lambda i: self.search_by_name(model_map[k], i).id,
                          [i for i in v if isinstance(i, str)]))
                [ng.append(i) for i in v if isinstance(i, int)]
                data[k] = ng
        return data

    def id_to_name(self, dictdata, model):
        data = deepcopy(dictdata)
        model_map = fetch_related_field(model)
        fields = {k: v for k, v in data.items() if k in model_map.keys()}
        for k, v in fields.items():
            if not isinstance(v, (str, list)) and v is not None:
                query = self.search_by_id(model_map[k], v)
                name = get_models_field_name(model_map[k])
                data[k] = getattr(query, name)
            elif isinstance(v, list):
                ng = list(map(lambda i: getattr(self.search_by_id(model_map[k], i),
                                                get_models_field_name(model_map[k])),
                              [i for i in v if isinstance(i, int)]))
                [ng.append(i) for i in v if isinstance(i, str)]
                data[k] = ng
        return data


class AssetListMixin(IdNameConvertMixin):
    def list(self, request, num=None):
        assets = (Asset.objects.all() if num is None else
                  Asset.objects.order_by('-id')[:num])
        serials = []
        for asset in assets:
            if asset.asset_type.name in ['服务器', '云主机', '虚拟机', '容器', 'docker']:
                serials.append(ServerAssetCreateUpdateSerializer(instance=asset).data)
            else:
                serials.append(NetDeviceAssetCreateUpdateSerializer(instance=asset).data)
        return Response([self.id_to_name(data, Asset) for data in serials])

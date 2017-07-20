# coding = utf-8
#
from hashlib import sha256
from django.db import models
from cmdb.models import Asset
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField


def get_models_field_name(model):
        if not issubclass(model, models.Model) and model is Asset:
            raise TypeError('except type model and not Asset model')
        return [field.name for field in model._meta.fields
                if 'name' in field.name][0]


def fetch_related_field(model):
    model_map = {}
    for field in model._meta.get_fields():
        if isinstance(field, (ForeignKey, ManyToManyField)):
            model_map[field.name] = field.related_model
    return model_map


def fetch_integer_field(model):
    model_map = {}
    for field in model._meta.get_fields():
        if isinstance(field, IntegerField):
            model_map[field.name] = field.model
    return model_map


def encrypt_pwd(pwd):
    return sha256(pwd.encode('utf-8')).hexdigest()


def get_help_text(model, field_name):
    return {f.name: f.help_text for f in model._meta.fields}



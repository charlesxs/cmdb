from django import template

register = template.Library()


@register.filter(name='fetch_groups_name')
def fetch_groups_name(assetobj):
    return [group.groupname for group in assetobj.usergroup.all()]


@register.filter(name='fetch_groups_id')
def fetch_groups_id(assetobj):
    return [group.id for group in assetobj.usergroup.all()]


@register.filter(name='to_null')
def to_null(v):
    if v is None:
        return ""
    return v


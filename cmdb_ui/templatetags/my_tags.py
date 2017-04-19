from django import template

register = template.Library()


@register.filter(name='fetch_groups_name')
def fetch_groups_name(assetobj):
    return [group.groupname for group in assetobj.usergroup.all()]


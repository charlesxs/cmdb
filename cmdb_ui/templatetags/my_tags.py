# coding=utf-8

from django import template
# from cmdb.models import *

register = template.Library()


@register.filter(name='get_business_line')
def get_business_line(obj):
    return [bs.name for bs in obj.business_line.all()]


@register.filter(name='get_business_line_id')
def get_business_line_id(obj):
    return [bs.id for bs in obj.business_line.all()]


@register.filter(name="seconds_to_hours")
def seconds_to_hours(t):
    return round(t / 3600, 2)


@register.filter(name="days_to_years")
def days_to_years(d, to=None):
    """
    days_to_years(days, to) -> N years M days
    or
    days_to_years(days) -> N.M years
    
    example:
        days_to_years(115419) -> 316 years 79 days
                           to='years' -> return 316 [years]
                           to='days'  -> return 79 [days]
                           to=None    -> return 316.22 [years]
    """
    if d <= 365:
        return 0
    years = d / 365
    if to == 'years':
        return int(years)
    elif to == 'days':
        return round((years - int(years)) * 365)
    return round(years, 2)


@register.filter(name='servers_count')
def servers_count(obj):
    return obj.asset_set.count()


@register.assignment_tag(name='cabinet_map')
def cabinet_map(position, asset_queryset):
    for asset in asset_queryset:
        if asset.cabinet_position != position:
            continue
        if asset.asset_type in ('服务器', '虚拟机', '云主机'):
            return {'asset_id': asset.id, 'name': asset.server.lan_ip}
        return {'asset_id': asset.id, 'name': asset.networkdevice.product_name}
    return {'asset_id': None, 'name': ''}


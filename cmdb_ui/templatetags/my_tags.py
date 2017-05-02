# coding=utf-8

from django import template

register = template.Library()


@register.filter(name='fetch_groups_name')
def fetch_groups_name(obj):
    return [group.groupname for group in obj.usergroup.all()]


@register.filter(name='fetch_groups_id')
def fetch_groups_id(obj):
    return [group.id for group in obj.usergroup.all()]


@register.filter(name='to_null')
def to_null(v):
    if v is None:
        return ""
    return v


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


@register.filter(name="fetch_aggroup_name")
def fetch_aggroup_name(assetgroup):
    return [group.groupname for group in assetgroup.usergroup_set.all()]


@register.filter(name='servers_count')
def servers_count(obj):
    return obj.asset_set.count()


@register.filter(name='fetch_assetgroup_names')
def fetch_assetgroup_names(usergroup):
    return [group.groupname for group in usergroup.assetgroup.all()]


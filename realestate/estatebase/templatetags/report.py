# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from estatebase.wrapper import get_wrapper
from collections import OrderedDict
from copy import deepcopy

register = template.Library()

def distance_helper(value):
    if value:
        return u' - %s м' % intcomma(value) 
    return ''

@register.inclusion_tag('inclusion/communication.html')
def communication(estate):
    comms = []
    if estate.electricity:
        comms.append('%s: %s%s' %  (u'свет', estate.electricity.name.lower(), distance_helper(estate.electricity_distance)))            
    if estate.watersupply:
        comms.append('%s: %s%s' %  (u'вода', estate.watersupply.name.lower(), distance_helper(estate.watersupply_distance)))
    if estate.gassupply:
        comms.append('%s: %s%s' %  (u'газ', estate.gassupply.name.lower(), distance_helper(estate.gassupply_distance)))    
    if estate.sewerage:
        comms.append('%s: %s%s' %  (u'канализация', estate.sewerage.name.lower(), distance_helper(estate.sewerage_distance)))        
    if estate.telephony:
        comms.append('%s: %s' %  (u'тел.', estate.telephony.name.lower()))    
    if estate.internet:
        comms.append('%s: %s' %  (u'интернет', estate.internet.name.lower()))    
    if estate.driveway:
        comms.append('%s: %s%s' %  (u'подъезд', estate.driveway.name.lower(), distance_helper(estate.driveway_distance)))    
    return {'comms': comms}

@register.inclusion_tag('inclusion/comma_from_details.html')
def wrapper_fieldset_comma(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

@register.inclusion_tag('inclusion/tr_from_details.html')
def wrapper_fieldset_tr(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

def wrapper_fieldset(obj, fieldset_name):
    details = OrderedDict()
    wrapper = get_wrapper(obj)
    field_list = getattr(wrapper, fieldset_name)
    for field in field_list:
        obj_field = obj._meta.get_field(field)
        value = getattr(obj,field)
        if obj_field.get_internal_type() == 'BooleanField' and value:
            value = u'Есть'
        if value:
            details[wrapper.get_label(field) or obj_field.verbose_name] = value            
    return {'details': details}

@register.inclusion_tag('inclusion/simple_layout.html')
def bidg_layout(level):
    layout_fieldset = OrderedDict([
                       ('area', u'площадь кв.м.'), 
                       ('furniture', u'мебель'), 
                       ('layout_feature', 'расположение'), 
                       ('interior', 'внутр. отделка'),
                       ('note', 'коммент')
                       ])   
    layout_dict = OrderedDict()       
    for layout in level.layout_set.all():
        layout_row = OrderedDict()
        for field, label in layout_fieldset.items():
            value = getattr(layout, field)
            if value:
                layout_row[label] = value
        layout_dict[layout.layout_type] = deepcopy(layout_row)         
    return {'layouts': layout_dict}            
            
                
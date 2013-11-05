from django import template
import datetime
import calendar

register = template.Library()

@register.filter(name='toString')
def toString(value):
	return str(value)

@register.filter()
def monthName(monthNumber):
	return calendar.month_name[int(monthNumber)]

@register.filter()
def jsonify(value):
	from django.utils import simplejson

	return simplejson.dumps(value)
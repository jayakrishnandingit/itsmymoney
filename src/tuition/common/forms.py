from django import forms as djangoSimpleForm

class StrippedCharField(djangoSimpleForm.CharField):
    def clean(self, value):
        if value is not None:
            value = value.strip()

        return super(StrippedCharField, self).clean(value)

class FormUtils(object):
	import datetime

	def createYearTuple(self, start=datetime.date.today().year, end=datetime.date.today().year):
		return map(lambda x,y: (unicode(x), unicode(y)), xrange(start, end+1), xrange(start, end+1))
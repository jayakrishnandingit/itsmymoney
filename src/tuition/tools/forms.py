'''
Created on Feb 6, 2013

@author: jayakrishnan
'''
from django.utils.datastructures import SortedDict
from django import forms as djangoSimpleForm
from tuition.common.forms import StrippedCharField
from django.core.exceptions import ValidationError

class ExpenseForm(djangoSimpleForm.Form):
    type = StrippedCharField(widget = djangoSimpleForm.TextInput(attrs = {'placeholder' : 'For example LIC'}), required = True)
    amount = djangoSimpleForm.FloatField(widget = djangoSimpleForm.TextInput(), required = True)
    dateOfExpense = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = True)
    comments = StrippedCharField(widget = djangoSimpleForm.Textarea(), required = False)

class DebtForm(djangoSimpleForm.Form):
	type = StrippedCharField(widget = djangoSimpleForm.TextInput(attrs = {'placeholder' : 'For Medical Emergency'}), required = True)
	amount = djangoSimpleForm.FloatField(widget = djangoSimpleForm.TextInput(), required = True)
	incurredDate = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = True)
	returnDate = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = True)
	hasReturned = djangoSimpleForm.BooleanField(required=False)
	expenseOfMonth = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = False)
	comments = StrippedCharField(widget = djangoSimpleForm.Textarea(), required = False)

	def clean_expenseOfMonth(self):
		import datetime
		
		markedDate = self.cleaned_data['expenseOfMonth']
		debtIncurredDate = self.cleaned_data['incurredDate']
		markedAsReturned = self.cleaned_data['hasReturned']
		if markedAsReturned and not markedDate:
			raise ValidationError('This field is required.')
		if markedDate and markedDate < debtIncurredDate:
			raise ValidationError('Date must be greater than %s.' % datetime.datetime.strftime(debtIncurredDate, '%d/%m/%Y'))
		return markedDate

class DebtReturnForm(djangoSimpleForm.Form):
	debtIncurredDate = None
	markAsExpense = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = True)
	returnComments = StrippedCharField(widget = djangoSimpleForm.Textarea(), required = False)

	def clean_markAsExpense(self):
		import datetime

		markedDate = self.cleaned_data['markAsExpense']
		if markedDate and markedDate < self.debtIncurredDate:
			raise ValidationError('Date must be greater than %s.' % datetime.datetime.strftime(self.debtIncurredDate, '%d/%m/%Y'))
		return markedDate

class ExpenseYearFilter(djangoSimpleForm.Form):
	import datetime
	from tuition.common.forms import FormUtils

	choices = FormUtils().createYearTuple(start=2000)
	yearSelect = djangoSimpleForm.ChoiceField(choices=choices, initial=unicode(datetime.date.today().year), widget=djangoSimpleForm.Select())
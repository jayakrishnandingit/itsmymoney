from django import forms as djangoSimpleForm
from django.core.exceptions import ValidationError
from tuition.common.forms import StrippedCharField

class UserRegistrationForm(djangoSimpleForm.Form):
	loggedInEmployeeKey = None
	keyHidden = None
	firstName = StrippedCharField(widget = djangoSimpleForm.TextInput(attrs = {'placeholder' : 'Paul'}), required = True)
	lastName = StrippedCharField(widget = djangoSimpleForm.TextInput(attrs = {'placeholder' : 'Samuel'}), required = True)
	alternateEmail = djangoSimpleForm.EmailField(widget = djangoSimpleForm.TextInput(attrs = {'placeholder' : 'paulsamuel@example.com'}), required = True)
	dob = djangoSimpleForm.DateField(input_formats = ["%d/%m/%Y"], widget = djangoSimpleForm.DateInput(attrs = {'placeholder' : 'DD/MM/YYYY'}), required = True)
	about = StrippedCharField(widget = djangoSimpleForm.Textarea(), required = False)

	def clean_firstName(self):
		from google.appengine.ext import db

		if self.keyHidden:
			self.keyHidden = db.Key(self.keyHidden)
			self.loggedInEmployeeKey = db.Key(self.loggedInEmployeeKey)
			if self.loggedInEmployeeKey != self.keyHidden:
				raise ValidationError('Invalid User')
		return self.cleaned_data['firstName']
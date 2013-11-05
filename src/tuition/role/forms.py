'''
Created on Jan 7, 2013

@author: jayakrishnan
'''
from django import forms

class RoleAddForm(forms.Form):
    from views import PERMISSIONS

    choices = [('All', 'Select All')] + [(perm, perm) for perm in PERMISSIONS]
    roleName = forms.CharField(widget = forms.TextInput())
    privileges = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple(), choices = choices)

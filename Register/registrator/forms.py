from django import forms
from .models import Section, SubService, AssignedService

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'description']

class SubServiceForm(forms.ModelForm):
    class Meta:
        model = SubService
        fields = ['section', 'name', 'description', 'online_available']

class AssignedServiceForm(forms.ModelForm):
    class Meta:
        model = AssignedService
        fields = ['user', 'service']

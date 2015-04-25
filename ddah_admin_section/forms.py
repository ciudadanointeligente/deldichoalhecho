from django import forms
from ddah_web.models import DDAHInstanceWeb


class DDAHInstanceNonSuperUserForm(forms.ModelForm):
    class Meta:
        model = DDAHInstanceWeb
        exclude = ('users', 'created_by', )

from django import forms
from ddah_web.models import DDAHInstanceWeb
from django.conf import settings

class DDAHInstanceForm(forms.ModelForm):
    header_img = forms.URLField(required=False)
    twitter_text = forms.CharField(required=False)
    og_img = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super(DDAHInstanceForm, self).__init__(*args, **kwargs)

        style = getattr(settings, 'DEFAULT_STYLE', {})
        style.update(self.instance.style)
        self.fields['header_img'].initial = style['header_img']
        social_networks = getattr(settings, 'DEFAULT_SOCIAL_NETWORKS', {})
        social_networks.update(self.instance.social_networks)
        self.fields['twitter_text'].initial = social_networks['twitter_text']
        self.fields['og_img'].initial = social_networks['og_img']

    def save(self, *args, **kwargs):
        self.instance.style['header_img'] = self['header_img'].value()
        self.instance.social_networks['twitter_text'] = self['twitter_text'].value()
        self.instance.social_networks['og_img'] = self['og_img'].value()
        return super(DDAHInstanceForm, self).save(*args, **kwargs)



    class Meta:
        model = DDAHInstanceWeb
        exclude = ( )

class DDAHInstanceNonSuperUserForm(DDAHInstanceForm):
    class Meta:
        model = DDAHInstanceWeb
        exclude = ('users', 'created_by', )

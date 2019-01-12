from django import forms
from .models import Follow, Profile
from django.contrib.auth.models import User


class FollowForm(forms.ModelForm):

    class Meta:
        exclude = set()
        model = Follow

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'body', 'www', 'facebook', 'phonenumber',)
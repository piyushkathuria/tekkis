from django import forms
from django.contrib.auth.models import User


class UserForm(forms.Form):
    class Meta:
        # specify model to be used
        model = User
        fields=['username','email','password']
        





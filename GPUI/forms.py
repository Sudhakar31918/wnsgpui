from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):
   # add required fields here
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput

from home.models import UserProfile

class UserUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name')
        widgets ={
            'username': TextInput(attrs={'class':'form-control','placeholder':'username'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('address','phone','city','country','image')

        widgets={
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
        }

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
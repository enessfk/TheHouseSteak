from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class SearchForm(forms.Form):
    query=forms.CharField(label='Search',max_length=100)

class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=30,label='Username :',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(max_length=200,label='Email :',widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,label='First Name :',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100,label='Last Name :',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=30,help_text=mark_safe('''Your password can’t be too similar to your other personal information.<br>
                                                    Your password must contain at least 8 characters.<br>
                                                    Your password can’t be a commonly used password.<br />
                                                    Your password can’t be entirely numeric.''') ,
                                label='Password :',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=30,help_text=' Enter the same password as before, for verification.',
                                label='Password Confirmation:',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','password1','password2')



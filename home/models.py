from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.forms import ModelForm, TextInput, Textarea


class Setting(models.Model):

    Status=(
        ('True','Yes'),
        ('False','No')
    )

    title=models.CharField(max_length=70)
    keywords=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    company=models.CharField(max_length=70)
    address=models.CharField(blank=True,max_length=150)
    phone=models.CharField(blank=True,max_length=20)
    fax=models.CharField(blank=True,max_length=20)
    email=models.CharField(blank=True,max_length=70)
    smtpserver=models.CharField(max_length=20)
    smtpemail=models.CharField(max_length=70)
    smtppassword=models.CharField(max_length=20)
    smtpport=models.CharField(blank=True,max_length=5)
    icon=models.ImageField(blank=True,upload_to='Favicon/')
    facebook=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    twitter=models.CharField(blank=True,max_length=50)
    aboutus=RichTextUploadingField(blank=True)
    contact=RichTextUploadingField(blank=True)
    references=RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=Status)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def icon_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.icon.url))

class ContactFormMessage(models.Model):
    Status=(
        ('New','New'),
        ('Read','Read'),
        ('Completed','Completed')
    )
    name=models.CharField(blank=True, max_length=20)
    email=models.CharField(blank=True, max_length=70)
    subject=models.CharField(blank=True, max_length=100)
    message=models.TextField(blank=True, max_length=255)
    status=models.CharField(max_length=10, choices=Status, default='New')
    ip=models.CharField(blank=True,max_length=20)
    note=models.CharField(blank=True,max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model=ContactFormMessage
        fields=['name','email','subject','message']
        widgets={
            'name' : TextInput(attrs={'class':'form-control','placeholder':'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Message','rows':'5'}),
        }
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.CharField(blank=True,max_length=150)
    phone=models.CharField(blank=True,max_length=20)
    city=models.CharField(blank=True,max_length=30)
    country=models.CharField(blank=True,max_length=30)
    image=models.ImageField(blank=True,upload_to='images/Users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.username

    def name_surname(self):
        return self.user.first_name+' '+self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone','address','city','country','image']


class FAQ(models.Model):
    Status=(
        ('True','Yes'),
        ('False','No')
    )
    ordernumber=models.IntegerField()
    question=models.CharField(max_length=150)
    answer=models.TextField(max_length=255)
    status=models.CharField(max_length=10,choices=Status)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

from django.contrib import admin
from home.models import Setting, ContactFormMessage, UserProfile, FAQ


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title','company','smtpserver','icon_tag','created_at']
    readonly_fields = ('icon_tag',)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','message','note','status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','name_surname','image_tag','phone','city','country','address']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber','question','answer','status']
    list_filter = ['status']


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(FAQ,FAQAdmin)
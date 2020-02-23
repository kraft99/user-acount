from django.contrib import admin

from .models import Activation,AccountDeleteActivation

admin.site.register(Activation,list_display=['token','user','expire_on'])
admin.site.register(AccountDeleteActivation,list_display=['token','email','expire_on'])
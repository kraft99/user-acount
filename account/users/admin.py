from django.contrib import admin
from .models import User

admin.site.register(User, list_display=['username','email','phone_number','join_on','join_ip'])

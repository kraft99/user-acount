from __future__ import unicode_literals
import logging

# from django.contrib.auth.middleware import AuthenticationMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse




class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if not hasattr(request,'user'):
            raise ImproperlyConfigured(
                "django.contrib.auth.middleware.AuthenticationMiddleware middleware must come "
                "before account.middlewares.ActiveUserMiddleware."
            )
        
        if request.user.is_authenticated:
        	# do sth if user is authenticated
        	print('user is authenticated')
        else:
        	print('user not authenticated')



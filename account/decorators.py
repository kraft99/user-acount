from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse



def unauthenticated(f):
	'''
	@ decorator - redirects authenticated users to index route on page load 
	or login rout for un-auth users
	'''
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated and request.user.is_active:
			return redirect(reverse('index'))
		else:
			return f(request,*args,**kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap


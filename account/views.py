import json
import urllib
import logging
import datetime

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,Http404
from django.utils.http import is_safe_url
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.contrib import auth
from django.urls import reverse


# from account import HttpResponseNotFound
from .forms import RegisterForm,LoginForm,email_account_form_class
from .models import Activation,AccountDeleteActivation
from .decorators import unauthenticated
from .exceptions import *



def backend_auth():
	"""
	@case study
	In situations where multiple authentication backends exists in
	project eg. facebook, twitter, github and project based authentication.
	django requires user to set additional authentication backend in auth.login(request,user)

	@require
	`django.contrib.auth.backends.ModelBackend`

	auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')

	or

	user.backend = "django.contrib.auth.backends.ModelBackend"
	auth.login(request,user)

	"""
	if hasattr(settings,'BACKEND_AUTH'):
		return settings.BACKEND_AUTH
	return 'django.contrib.auth.backends.ModelBackend'

backend_auth = backend_auth()


def register(request):
	# call_import_func() # 
	form = RegisterForm(request)
	if request.method == 'POST':
		form = RegisterForm(request,data = request.POST)
		if form.is_valid():
			form.save()
			# NOTE: ideally user should be redirected to a page with a message.
			mssg = 'Email has been sent to the registered email to activate account .'
			messages.add_message(request,messages.INFO,mssg)
			# print('valid')
			return redirect('account:register')
		else:
			# invalid form is been handled by bootstrap packages
			# no need for django messages.
			pass
	template = 'account/register.html'
	return TemplateResponse(request,template,{'form':form})


# login view
@never_cache
@unauthenticated
def login(request):
	# print(type(settings))
	if request.method == 'POST':
		next = request.GET.get('next')
		form = LoginForm(data = request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = None
			try:
				user = auth.authenticate(username=username,password=password)
			except:
				pass
			if not user is None and user.is_active:
				# security check complete - successful.
				auth.login(request,user)
				# make sure redirect_to or next path isn't garbage.
				if request.session.test_cookie_worked():
					request.session.delete_test_cookie()

				if next:
					redirect_path = next
					is_a_safe_url = is_safe_url(url=redirect_path,
						allowed_hosts=request.get_host(),
						require_https=request.is_secure(),)
					# next path exists and its safe.
					if is_a_safe_url and redirect_path:
						# redirect to next path.
						return redirect(redirect_path)
				# next path is none then redirect to home route.
				return redirect(reverse('index'))
			else:
				# pass error messages for failure to logn wit wrong credentials.
				logging.error('invalid user credentials')
				messages.add_message(request,messages.WARNING,'invalid user credentials.')
				return redirect('account:login')
		else:
			messages.add_message(request,messages.WARNING,'invalid user credentials.')
			return redirect('account:login')
	form = LoginForm()

	request.session.set_test_cookie()

	template = 'account/login.html'
	return TemplateResponse(request,template,{'form':form})


@csrf_exempt
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
	messages.add_message(request,messages.SUCCESS,'You have been successfully logged out.')
	return redirect('account:login')


@login_required
def delete_account(request,username):
	form = email_account_form_class(request)
	if request.method == 'POST':
		form = email_account_form_class(request,data=request.POST)
		mssg = ''
		if form.is_valid():
			form.save(commit=True)
			mssg = 'Check your email to confirm account deletion.'
			messages.add_message(request,messages.INFO,mssg)
		else:
			# logging.error('error validation user email')
			mssg = 'Error validation email, try again.'
			messages.add_message(request,messages.WARNING,mssg)
		return redirect(reverse('account:delete-account',kwargs={'username':request.user.username}))
	ctx = dict(form = form)
	return TemplateResponse(request,'account/send_delete_account.html',ctx)


@login_required
def delete_account_confirmation(request,template = 'account/delete_account.html',ctx = dict(),**kwargs):
	token = get_object_or_404(AccountDeleteActivation,token__iexact=kwargs.get('token'))
	print(token)
	ctx['token'] = token
	ctx.update(email = token.email)
	return TemplateResponse(request,template,ctx)


@login_required
@require_http_methods(["POST"])
def remove(request,**kwargs):
	token = request.POST.get('token')
	token = get_object_or_404(AccountDeleteActivation,token__iexact=token)
	if not request.user.email == token.email:
		raise PermissionDenied('You don\'t have permission to delete account for {}'.format(token.email))
	request.user.delete() # delete user account
	token.delete() # remove token from db
	messages.add_message(request,messages.SUCCESS,'Account has been deleted.')
	return redirect('account:login')



def activate_account(request,**kwargs):
	# activation get object - runs in its own operations.

	activation = get_object_or_404(Activation,token__iexact=kwargs.get('token'))

	with transaction.atomic():
		'''
		@transaction.atomic
		failure in any one of the operations, should roll back all other operations.
		None of the operations gets commited in db.
		'''
		try:
			if activation.has_expired:
				raise ActivationCodeExpired('Activation token has expired.')
			activation.user.is_active = True
			activation.user.join_on = datetime.datetime.now()
			activation.user.save(update_fields=['join_on','is_active'])
			auth.login(request,activation.user,backend=backend_auth)
			activation.delete()
			#NOTE: redirect to login page
			return redirect('account:login')
		except ActivationCodeExpired as e:
			logging.exception(e)
			return HttpResponse(e)


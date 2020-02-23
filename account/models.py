
import datetime
from django.conf import settings
from dateutil.relativedelta import relativedelta


from django.urls import reverse
from urllib.parse import urljoin
from django.utils.encoding import iri_to_uri

from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail 
from django.db import models


# from .email import send_mail
from .users.models import User
from .utils import activation_token
from .exceptions import ActivationCodeExpired
from .app_settings import ACTIVATION_DURATION_IN_DAYS





class Activation(models.Model):
	''' Activation Model for user account creation.'''

	token 		= models.CharField(max_length=250,blank=True,null=True,unique=True,editable=False)
	user 		= models.OneToOneField(to=User,on_delete=models.CASCADE) 
	expire_on  	= models.DateTimeField(blank=True,null=True)
	is_sent 	= models.BooleanField(default=False)

	created 	= models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering 		= ('-created',)
		verbose_name 	= 'Activation Code'
		verbose_name_plural = 'Activation Codes'


	def __str__(self):
		return 'activation code created for ({0})'.format(self.user.username)

	def save(self,*args,**kwargs):
		super(Activation,self).save(*args,**kwargs)


	@classmethod	
	def create_activation(cls,user_obj):
		''' @method - create instance of activation model.'''
		now = timezone.now()
		activation_duration = now + relativedelta(days = ACTIVATION_DURATION_IN_DAYS)
		# activation_duration = datetime.datetime.now() +\
		# 						 datetime.timedelta(days=ACTIVATION_DURATION_IN_DAYS)
		is_sent = True
		if user_obj:
			kwargs = dict(
				token = activation_token(),
				user  = user_obj,
				expire_on = activation_duration,
				is_sent = is_sent
			)
			return cls.objects.create(**kwargs)


	def has_expired(self):
		# if `True` it has expired else `False` not expired yet.
		return bool(self.expire_on <= timezone.now())
	has_expired = property(has_expired)



	def mail(self,request =None):
		'''@method - send activation email'''
		if request is not None:
			domain = get_current_site(request).domain

			# get activation route full path.
			full_activation_url = build_absolute_uri(
				reverse(
					'account:account-activation',
					kwargs={'token':self.token}
				),
				request
			)
			
			# print(full_activation_url)

			subject = 'Account Activation'
			message = "To activate {0} account for user {1} click on this {2} link.".format(domain,
				self.user.username,
				full_activation_url)
			from_email = settings.DEFAULT_FROM_EMAIL
			to_email = self.user.email

			try:
				send_mail(subject,message,from_email,[to_email],fail_silently=True)
				# print('mail sent')
			except BadHeaderError:
				pass






class AccountDeleteActivation(models.Model):
	''' Activation Model for user account delete.'''

	token 		= models.CharField(max_length=250,blank=True,null=True,unique=True,editable=False)
	email		= models.EmailField(max_length=250)
	expire_on  	= models.DateTimeField(blank=True,null=True)
	is_sent 	= models.BooleanField(default=False)

	created 	= models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering 		= ('-created',)
		verbose_name 	= 'Activation Code for Account Delete'
		verbose_name_plural = 'Activation Codes for Account Delete'


	def __str__(self):
		return 'delete account activation code created for ({0})'.format(self.email)

	def save(self,*args,**kwargs):
		super(AccountDeleteActivation,self).save(*args,**kwargs)


	@classmethod	
	def create_activation(cls,email):
		''' @method - create instance of activation model.'''
		now = timezone.now()
		activation_duration = now + relativedelta(days = 2)
		# activation_duration = datetime.datetime.now() +\
		# 						 datetime.timedelta(days=ACTIVATION_DURATION_IN_DAYS)
		is_sent = True
		if email:
			kwargs = dict(
				token = activation_token(),
				email  = email,
				expire_on = activation_duration,
				is_sent = is_sent
			)
			return cls.objects.create(**kwargs)


	def has_expired(self):
		# if `True` it has expired else `False` not expired yet.
		return bool(self.expire_on <= timezone.now())
	has_expired = property(has_expired)



	def mail(self,request = None):
		'''@method - send activation email'''
		if request is not None:
			domain = get_current_site(request).domain

			# get activation route full path.
			full_activation_url = build_absolute_uri(
				reverse(
					'account:account-delete-confirmation',
					kwargs={'token':self.token}
				),
				request
			)
			
			# print(full_activation_url)

			subject = 'Account Delete Confirmation.'
			message = "To delete {0} account for email {1} click on this link {2} ".format(domain,
				self.email,
				full_activation_url)
			from_email = settings.DEFAULT_FROM_EMAIL
			to_email = self.email

			try:
				send_mail(subject,message,from_email,[to_email],fail_silently=True)
				# print('mail sent')
			except BadHeaderError:
				pass



def build_absolute_uri(location,request):
    # type: (str) -> str
    host = get_current_site(request).domain
    protocol = "https" if settings.ENABLE_SSL else "http"
    current_uri = "%s://%s" % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)




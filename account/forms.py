import logging

from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.contrib import auth
from django import forms

from .users.models import User 
from .utils import visitor_ip_address,is_valid_ip_address
from .models import Activation,AccountDeleteActivation
from .validators import (validate_phone_number_in_db,
						validate_username_in_db,
						validate_email_in_db)




class RegisterForm(UserCreationForm):
	email 	   	 	= forms.EmailField(label='email',
										validators=[validate_email_in_db],
										required=True,
										widget=forms.EmailInput())

	phone_number 	= forms.CharField(label="phone Number",
										validators=[validate_phone_number_in_db],
										required=True
										,widget=forms.TextInput())

	username     	= forms.CharField(label="username",
												validators=[validate_username_in_db],
												required=True,
												widget=forms.TextInput())


	join_ip 		= forms.CharField(label="",required=False,widget=forms.HiddenInput())

	honey_pot 		= forms.CharField(label="",required=False,widget=forms.HiddenInput())

	def __init__(self,request= None,*args,**kwargs):
		self.request = request
		super(RegisterForm,self).__init__(*args,**kwargs)

		# validate and assign clients ip on form initialization.
		if is_valid_ip_address(visitor_ip_address(self.request)):
			self.fields['join_ip'].initial = visitor_ip_address(self.request)
		else:
			pass

		# self.fields['country'].choices = self.fields['country'].choices[1:] # test
		self.fields['email'].widget.attrs.update({'placeholder':'Your Email'})
		self.fields['phone_number'].widget.attrs.update({'placeholder':'Your Phone Number'})
		self.fields['username'].widget.attrs.update({'placeholder':'Your Username'})
		self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})

		self.fields['password1'].label = 'password'
		# self.fields['password1'].widget.attrs.update({'value':'password'}) # test
		# self.fields['password1'].widget.attrs.update({'disabled':'True'}) # test
		self.fields['password2'].label = 'password comfirmation'


	class Meta:
		model  = User
		# fields = ('phone_number','email','username','join_ip','country',)
		fields = ('phone_number','email','username','join_ip',)




	def clean_username(self):
		cd = self.cleaned_data
		username = cd.get('username').lower() # save username in lowercase
		return username



	def clean_email(self): 
		cd = self.cleaned_data
		email = cd.get('email').lower() # save email in lowercase
		return email


	def clean_honey_pot(self):
		cd = self.cleaned_data
		value 	= cd.get('honey_pot')
		# print(value)
		if value:
			message = 'Do not fill this form field'
			raise forms.ValidationError(message)
		return value



	def clean_password(self):
		cd = self.cleaned_data
		password1 = cd.get('password1')
		password2 = cd.get('password2')

		if password2 and password1:
			if not (password2 == password1):
				raise forms.ValidationError('Your password\'s do not match.')
			return password2

	@transaction.atomic
	def save(self,force_insert=False,force_update=False,commit=True,**kwargs):
		'''
		override save method to perform activation on user account.
		- deacivate user
		- generate activation objects
		- send email with token 
		'''
		request = self.request
		user = super().save(commit=False)
		if commit:
			user.is_active = False
			user.save()
			# create activation code
			Activation.create_activation(user).mail(request)
			
		return user


class LoginForm(forms.Form):
	username     	= forms.CharField(label="username",required=True,widget=forms.TextInput())
	password 	    = forms.CharField(label="password",widget=forms.PasswordInput())
	

	def __init__(self,*args,**kwargs):
		super(LoginForm,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs.update({'placeholder':'Your email or username or phone number'})
		self.fields['password'].widget.attrs.update({'placeholder':'Your password'})


	# def clean(self):
	# 	self.cleaned_data = super().clean()
	# 	cd = self.cleaned_data
	# 	username = cd.get('username')
	# 	password = cd.get('password')
	# 	user = auth.authenticate(username=username,password=password)
	# 	if user:
	# 		print('user is authenticated')
	# 	else:
	# 		print('user is not authenticated')
	# 	return cd



class EmailAccountForm(forms.ModelForm):

	email 		= forms.EmailField(label='Email Account',
									required=True,
									widget=forms.EmailInput())

	class Meta:
		model 	= User
		fields  = ('email',)


	def __init__(self,request = None,*args,**kwargs):
		self.request = request
		super(EmailAccountForm,self).__init__(*args,**kwargs)


	def clean_email(self):
		cd = self.cleaned_data
		email = cd.get('email')
		if email:
			return email
		else:
			return


	def get_email(self):
		return self.clean_email()

	email = property(get_email)


	@transaction.atomic
	def save(self,force_insert=False,force_update=False,commit=True,**kwargs):
		user 	= super().save(commit=False)
		if commit:
			user.save()
			# create activation and send token
			AccountDeleteActivation.create_activation(self.email).mail(self.request)
		return user


email_account_form_class = EmailAccountForm
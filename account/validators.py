# validate inputs unique
# ban inputs
from .users.models import User 
from django.core.exceptions import ValidationError


errors = {
	'username':'user with email already exists.',
	'email':'user with username already exists.',
	'phone_number':'user with phone number already exists.'
}

def validate_email_unique(email):
# checks email does not exists in db.
	qry = User._default_manager.filter(email__iexact=email)
	if not qry.exists():
		return True
	raise ValidationError(errors['username'])


def validate_username_unique(username):
# checks username unique and does not exist in db.
	if username:
		try:
			user = User._default_manager.get(username__iexact=username)
		except User.DoesNotExist:
			return True # successful
		raise ValidationError(errors['email'])


def validate_phone_number_in_db(phone_number):
# checks phonenumber does not exists in db.
	qry = User.objects.filter(phone_number__iexact=phone_number)
	if not qry.exists():
		return True
	raise ValidationError(errors['phone_number'])



unavailable = {
	'username': 'This username is not available. Please try another.',
	'email': 'This email is not available. Please try another.'
}

''' validate and check ban username '''
def validate_username_in_db(username):
	# NOTE : populate with more items in production.
	invalid_usernames = [
			'django',
			'account',
			'test',
			'admin',
			'superuser',
			'error',
			'support',
			'info',
			'warning',
			'success',
			'danger',
			'debug',
			'logout',
			'login',
			'register',
			'activate',
			'password',
			'authenticate',
			'user',
			'users',
			'superuser',
	]
	validate_username_unique(username) # checks unique username validation.
	if username in invalid_usernames: # checks username ban. 
		raise ValidationError(unavailable['username'])



def validate_email_in_db(email):
	# NOTE : populate with more items in production.
	invalid_email = [
			'django',
			'account',
			'test',
			'admin',
			'user_account',
			'error',
			'support',
			'info',
			'warning',
			'superuser',
			'success',
			'danger',
			'debug',
			'logout',
			'login',
			'register',
			'activate',
			'password',
			'authenticate',
			'user',
			'users',
			'superuser',
	]

	validate_email_unique(email)

	'''
	eg. email = 'edward.moody@yahoo.com'
	* email.split('@',1)[0] -> edward.moody

	'''
	b4_domain = email.split('@',1)[0]
	if b4_domain in invalid_email:
		raise ValidationError(unavailable['email'])





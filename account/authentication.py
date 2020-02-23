# from django.contrib.auth.models import User

import re

from django.contrib.auth.backends import ModelBackend
from .users.models import User


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)'
    # domain
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE
)   # literal form, ipv4 address (SMTP 4.1.3)



class User_Account_Backend(ModelBackend):
    """
    Custom backend for project User account
    NOTE : You can do whatever you want here.
    """
    def get_user(self,user_id):
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None




class EmailAuthBackend(User_Account_Backend):
    """
    Authenticate using an e-mail account.
    """
    # def authenticate(self,request,username=None,password=None,**kwargs):
    #     # func allows for both username or email & password authentication.
    #     is_email = email_re.match(username)
    #     if is_email:
    #         # print('is email')
    #         qry = User._default_manager.filter(email=username)
    #     else:
    #         # print('is username')
    #         qry = User._default_manager.filter(username=username)
    #     try:
    #         user = qry.get()
    #     except User.DoesNotExist:
    #         return None
    #     if user.check_password(password):
    #         return user
    #     return None


    def authenticate(self, request, username=None, password=None,**kwargs):
        # func allows for both username or email & password authentication.
        try:
            user = User._default_manager.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None



class CaseInsensitiveModelBackend(ModelBackend):
    """
    Custom authentication backend to enable authenticating with case insensitive usernames.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            username = username.lower()
        return super().authenticate(request, username, password, **kwargs)



# class EmailUsernamePhonenumberModelBackend(ModelBackend):

#     def authenticate(self, username = None, password = None):
#         #If username is an email address, then try to pull it up
#         if '@' in username:
#             try:
#                 user = User.objects.get(email = username)
#             except User.DoesNotExist:
#                 return None

#         #We have a non-email address username we should try username
#         elif re.match(r'^[\w-]+$',username):
#             try:
#                 user = User.objects.get(username = username)
#             except User.DoesNotExist:
#                 return None

#         # perhaps user try to log in with phone-number
#         else:
#             pass

#         if user.check_password(password):
#             return user

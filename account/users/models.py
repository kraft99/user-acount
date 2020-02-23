import os

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db import models


# COUNRTY = (
# (1,'A'),
# (2,'B'),
# (3,'C'),

# )

# Create your models here.
class User(AbstractUser):
	phone_number 	= 		models.CharField(max_length=10,unique=True,blank=True,null=True)
	# NOTE : redundant but required to save() activation code for account delete - raise integrity error
	# as other fields are blank=False adn needs to be populated.
	username 		= 		models.CharField(max_length=255,unique=True,blank=True,null=True) 
	join_ip 		= 		models.GenericIPAddressField(blank=True,null=True)
	join_on 		= 		models.DateTimeField(blank=True,null=True) # populate after activation.
	# country 		= 		models.CharField(max_length=125,blank=True,null=True,choices=COUNRTY) # test
	created 		= 		models.DateTimeField(auto_now_add=True)
	updated			= 		models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.username
		




# from django.contrib.auth.models import Group


# group = Group(name = "Editor")
# group.save()                    # save this new group for this example
# user = User.objects.get(pk = 1) # assuming, there is one initial user 
# user.groups.add(group)          # user is now in the "Editor" group
# then user.groups.all() returns [<Group: Editor>].

# Alternatively, and more directly, you can check if a a user is in a group by:

# if django_user.groups.filter(name = groupname).exists():

#     ...

# class Upload(models.Model):
#     """
#     Model for uploads of file in topic.
#     - **parameters**:
#         :param user: User relation.
#         :param attachment: File upload.
#     """
#     def generate_path(instance, filename):
#         """
#         Generate path to field attachment
#         """
#         extension = os.path.splitext(filename)[1]
#         name_random = get_random_string(length=32)
#         filename = name_random + extension
#         return os.path.join("uploads", filename)

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name='users_uploads',
#         verbose_name=_('User'), on_delete=models.CASCADE
#     )
#     dp	 = models.FileField(
#         _('File'), blank=False, null=False, upload_to=generate_path,
#         validators=[]
#     )

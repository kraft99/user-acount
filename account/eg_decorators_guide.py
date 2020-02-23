'''

Group Required

Sometimes we need to protect some views, to allow a certain group of users to access it. 
Instead of checking within it if the user belongs to that group/s, we can use the following decorator

def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated():
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)


# The way to use this decorator is:
@group_required(‘admins’, ‘seller’)
def my_view(request, pk)
    ...




Anonymous required

This decorator is based on the decorator login_required of Django, but looks 
for the opposite case, that the user is anonymous, 
otherwise the user is redirected to the website defined in our settings.py 
 can be useful when we want to protect logged user views, such as the login or registration view

 def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous(),
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


# The way to use this decorator is:
@anonymous_required
def my_view(request, pk)
    ...





Superuser required


from django.core.exceptions import PermissionDenied


def superuser_only(function):
  """Limit view to superusers only."""

   def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied           
       return function(request, *args, **kwargs)
   return _inner


# The way to use this decorator is:
@superuser_only
def my_view(request):
    ...



Ajax required


from django.http import HttpResponseBadRequest


def ajax_required(f):
   """
   AJAX request required decorator
   use it in your views:

   @ajax_required
   def my_view(request):
       ....

   """   

   def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return HttpResponseBadRequest()
       return f(request, *args, **kwargs)

   wrap.__doc__=f.__doc__
   wrap.__name__=f.__name__
   return wrap


# The way to use this decorator is:
@ajax_required
def my_view(request):
    ...






Custom Functionality


from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


def user_can_write_a_review(func):
   """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

   @functools.wraps(func)
   def wrapper(request, *args, **kwargs):
       if request.user.is_authenticated() and request.user.points < 10:
           logger.warning('The {} user has tried to write a review, but does not have enough points to do so'.format( request.user.pk))
           return HttpResponseForbidden()

       return func(request, *args, **kwargs)

   return wrapper

'''
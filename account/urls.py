from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
	# account auth routes
	path('register/',views.register,name='register'),
	path('login/',views.login,name='login'),
	path('logout/',views.logout,name='logout'),
	# activation routes
	path('activation/<str:token>/',views.activate_account,name='account-activation'),

	# delete account
	path('delete/<str:username>/',views.delete_account,name='delete-account'),
	path('delete/confirmation/<str:token>/',views.delete_account_confirmation,name='account-delete-confirmation'),
	path('remove/',views.remove,name='remove'),
]

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
	user = request.user
	ctx = dict(username=user)
	ctx.update(email=user.email)
	return TemplateResponse(request,'index.html',ctx)
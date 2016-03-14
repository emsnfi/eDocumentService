﻿# coding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from ebookSystem.models import *
from ebookSystem.forms import *

def register(request, template_name='registration/register.html'):
	if request.method == 'POST':
		registerUserForm = RegisterUserForm(request.POST)
		newUser = registerUserForm.save(commit=False)
		newUser.username = request.POST.get('username')
		newUser.set_password(request.POST.get('password'))
		newUser.is_active = False
		newUser.save()
		newEditor = Editor(user=newUser, service_hours=0)
		newEditor.save()
		redirect_to = '/auth/login/'
		return HttpResponseRedirect(redirect_to)
#		return render(request, template_name, locals())
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return render(request, template_name, locals())

def login_user(request, template_name='registration/login.html'):
	if request.method == 'GET':
		loginForm = LoginForm()
	if request.method == 'POST':
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			password = loginForm.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					redirect_to = redirect_user(user)
					return HttpResponseRedirect(redirect_to)
				else:
					error_message = u'您的帳號非啟用'
			else:
				error_message = u'您的帳號或密碼錯誤'
	return render(request, template_name, locals())

def logout_user(request, template_name='registration/logged_out.html'):
	logout(request)
	return render(request, template_name, locals())

def redirect_user(user):
	if user.is_editor():
		return reverse('account:profile')
	if user.is_guest():
		return reverse('account:profile')
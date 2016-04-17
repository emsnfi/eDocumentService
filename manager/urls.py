from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<template_name>\w+)/readme/$', views.readme, name='readme'),
	url(r'^review_document_list/$', views.review_document_list, name='review_document_list'),
	url(r'^review_user_list/$', views.review_user_list, name='review_user_list'),
	url(r'^(?P<template_name>\w+)/$', views.static, name='static'),
]

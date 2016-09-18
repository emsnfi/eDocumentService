﻿# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory


from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
from account.views import *
from ebookSystem.views import *
from genericUser.views import *
from mysite.views import register
from mysite.settings import BASE_DIR
import shutil

class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, status=User.STATUS['active'])
		root.set_password('root')
		root.save()
		rootEditor = Editor.objects.create(user=root)
		rootGuest = Guest.objects.create(user=root)
		factory = RequestFactory()
		request = factory.post(reverse('register'), {'username':'demo-editor', 'password':'demo-editor', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo editor firstname', 'last_name':'demo editor lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'editor':'Editor', 'professional_field':u'資訊工程學'})
		response = register(request)
		with open('temp/dcf.jpg') as dcf_file:
			with open('temp/dcb.jpg') as dcb_file:
				request = factory.post(reverse('register'), {'username':'demo-guest', 'password':'demo-guest', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo guest firstname', 'last_name':'demo guest lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'guest':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file})
				response = register(request)
				request = factory.post(reverse('register'), {'username':'demo-manager', 'password':'demo-manager', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo manager firstname', 'last_name':'demo manager lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'editor':'Editor', 'guest':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file, 'professional_field':u'資訊工程學'})
				response = register(request)
		manager = User.objects.get(username='demo-manager')
		manager.status = manager.STATUS['active']
		manager.is_editor=True
		manager.is_guest=True
		manager.is_manager=True
		manager.save()
		with open(u'temp/藍色駭客.zip') as fileObject:
			request = factory.post(reverse('genericUser:create_document'), {'bookname':u'藍色駭客', 'author':u'傑佛瑞．迪佛', 'house':u'皇冠', 'ISBN':u'9789573321569', 'date':u'2013-07-11', 'fileObject':fileObject})
		request.user = manager
		response = create_document(request)
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==1, 'create book fail'
		assert len(EBook.objects.all()) == 10, 'create part fail'
		book = Book.objects.get(ISBN=u'9789573321569')
		assert os.path.exists(book.path), 'book resource folder not exist'
		book.status = book.STATUS['active']
#		request = factory.post(reverse('account:profile'), {'getPart':''})
#		request.user = root
#		response = profileView.get(request)
		ebook = EBook.objects.get(book=book, part=1)
		ebook.status = ebook.STATUS['sc_edit']
		ebook.editor = rootEditor
		ebook.sc_editor = rootEditor
		ebook.save()
		from zipfile import ZipFile
		src = BASE_DIR +'/temp/part1.zip'
		dst = ebook.book.path +u'/OCR'
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)
		ebook.create_SpecialContent()
		request = factory.post(reverse('genericUser:apply_document'), {u'ISBN':u'9789865829810', u'bookname':u'遠山的回音', u'author':u'卡勒德.胡賽尼(Khaled Hosseini)著; 李靜宜譯', u'house':u'木馬文化', u'date':u'2014-02-01'})
		request.user = manager
		response = apply_document(request)
		assert len(ApplyDocumentAction.objects.all()) == 1, 'create ApplyDocumentAction fail'
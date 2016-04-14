﻿# coding: utf-8
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError 
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from zipfile import ZipFile
from ebookSystem.models import *
from account.models import *
from .models import *
from .forms import *
from utils.decorator import *
from utils.validate import *
from utils.zip import *
import mysite
import json
import shutil

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

@user_category_check('guest')
def create_document(request, template_name='guest/create_document.html'):
	readmeUrl = reverse('guest:create_document') +'readme/'
	if request.method == 'POST':
		response = {}
		redirect_to = None
		bookForm = BookForm(request.POST, request.FILES)
		if bookForm.is_valid():
			uploadPath = u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['ISBN'])
			if not os.path.exists(uploadPath):
				uploadFilePath = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
				with ZipFile(uploadFilePath, 'r') as uploadFile:
					ZipFile.testzip(uploadFile)
				unzip_file(uploadFilePath, uploadPath)
				if validate_folder(uploadPath+u'/OCR', uploadPath+u'/source', 50)[0]:
					newBook = bookForm.save(commit=False)
					if request.POST.has_key('guest'):
						try:
							user = User.objects.get(username=request.POST['guest'])
						except:
							user = request.user
					else:
						user = request.user
					newBook.is_active = True
					newBook.guest = user.guest
					newBook.save()
					redirect_to = reverse('guest:profile')
					response['status'] = 'success'
					response['message'] = u'成功建立並上傳文件'
					response['redirect_to'] = redirect_to
				else:
					shutil.rmtree(uploadPath)
					response['status'] = 'error'
					response['message'] = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			else:
				response['status'] = 'error'
				response['message'] = u'文件已存在'
		else:
			response['status'] = 'error'
			response['message'] = u'表單驗證失敗'
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
#			if redirect_to:
#				return HttpResponseRedirect(redirect_to)
#			else:
			return render(request, template_name, locals())
	if request.method == 'GET':
		bookForm = BookForm()
	return render(request, template_name, locals())

def upload_progress(request):
	"""
	Return JSON object with information about the progress of an upload.
	"""
	progress_id = ''
	if 'X-Progress-ID' in request.GET:
		progress_id = request.GET['X-Progress-ID']
	elif 'X-Progress-ID' in request.META:
		progress_id = request.META['X-Progress-ID']
	if progress_id:
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		data = cache.get(cache_key)
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def handle_uploaded_file(dirname, file):
	if not os.path.exists(dirname):
		os.makedirs(dirname, 0777)
	fullpath = os.path.join(dirname, file.name)
	if os.path.exists(fullpath):
		return -1
	with open(fullpath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return fullpath

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check('guest'))
	def get(self, request, *args, **kwargs):
		readmeUrl = reverse('guest:profile') +'readme/'
		template_name=self.template_name
		user=request.user
		book_list = Book.objects.filter(guest=user.guest)
		return render(request, template_name, locals())

	@method_decorator(user_category_check('guest'))
	def post(self, request, *args, **kwargs):
		readmeUrl = reverse('guest:profile') +'readme/'
		template_name=self.template_name
		response = {}
		redirect_to = None
		user=request.user
		book_list = Book.objects.filter(guest=user.guest)
		if request.POST.has_key('emailBook'):
			book_ISBN = request.POST.get('emailBook')
			emailBook = Book.objects.get(ISBN = book_ISBN)
			subject = u'[文件] {}'.format(emailBook.bookname)
			body = u'新愛的{0}您好：\n'.format(user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[user.email])
			for part in emailBook.ebook_set.all():
				attach_file_path = emailBook.path +u'/OCR/part{0}.txt'.format(part.part)
				email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			response['status'] = 'success'
			response['message'] = u'已寄送到您的電子信箱'
		if request.POST.has_key('delete'):
			book_ISBN = request.POST.get('delete')
			deleteBook = Book.objects.get(ISBN = book_ISBN)
			deleteBook.delete()
			shutil.rmtree(deleteBook.path)
			response['status'] = 'success'
			response['message'] = u'成功刪除文件'
		book_list = Book.objects.filter(guest=user.guest)
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
#			if redirect_to:
#				return HttpResponseRedirect(redirect_to)
#			else:
			return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'guest/' +template_name +'_readme.html'
	return render(request, template_name, locals())
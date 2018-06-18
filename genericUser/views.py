﻿# coding: utf-8
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, redirect
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from ebookSystem.models import *
from ebookSystem.apis import *
from genericUser.models import *
from utils.decorator import *
from utils.tag import *
from utils.uploadFile import handle_uploaded_file
from .forms import *
from mysite.settings import BASE_DIR, SERVICE, MANAGER, OTP_ACCOUNT, OTP_PASSWORD
from utils.resource import *
from zipfile import ZipFile
import base64
import json
import shutil
import datetime
import requests
import urllib, urllib2

@http_response
def generics(request, name):
	template_name='genericUser/{0}.html'.format(name)
	return locals()

@http_response
def refactor(request, name):
	template_name = 'genericUser/refactor/{0}.html'.format(name)
	model = name.split('-')[0]
	api = '/genericUser/api/{0}'.format(model)
	return locals()

@http_response
def refactor_detail(request, name, pk):
	template_name = 'genericUser/refactor/{0}.html'.format(name)
	model = name.split('-')[0]
	api = '/genericUser/api/{0}'.format(model)
	return locals()

@http_response
def retrieve_password(request, template_name='genericUser/retrieve_password.html'):
	if request.method == 'POST':
		print request.POST['rpw_email']
		if not request.POST['username']=='':
			try:
				birthday = request.POST['rpw_birthday'].split('-')
				birthday = [ int(i) for i in birthday ]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(username=request.POST['username'], email=request.POST['rpw_email'], birthday=birthday)
			except:
				status = 'error'
				message = u'無法取得使用者資料，請確認填寫的資料是否無誤'
				return locals()
			import random
			import string
			reset_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			user.set_password(reset_password)
			try:
				subject = u'重設密碼郵件'
				message = u'您的新密碼為：{0}'.format(reset_password)
				user.email_user(subject=subject, message=message)
			except:
				status = 'error'
				message = u'傳送郵件失敗'
				return locals()
			user.save()
			status = 'success'
			message = u'成功重設密碼，請至信箱取得'
			redirect_to = reverse('login')
			return locals()
		else:
			try:
				birthday = request.POST['rusr_birthday'].split('-')
				birthday = [ int(i) for i in birthday ]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(email=request.POST['rusr_email'], birthday=birthday)
			except:
				status = 'error'
				message = u'無法取得使用者資料，請確認填寫的資料是否無誤'
				return locals()
			try:
				subject = u'取得username郵件'
				message = u'您的username為：{0}'.format(user.username)
				user.email_user(subject=subject, message=message)
			except:
				status = 'error'
				message = u'傳送郵件失敗'
				return locals()
			status = 'success'
			message = u'已將帳號使用者名稱寄至註冊信箱'
			return locals()
	if request.method == 'GET':
		return locals()

def user_guide(request, template_name='genericUser/user_guide.html'):
	return render(request, template_name, locals())

def recruit(request, template_name='genericUser/recruit.html'):
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
		#		cache_key = "%s" % (progress_id)
		#		data = request.session.get('upload_progress_%s' % cache_key, None)
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

@http_response
def apply_document(request, template_name='genericUser/apply_document.html'):
	BookInfoForm = modelform_factory(BookInfo, fields=('bookname', 'author', 'house', 'date', 'bookbinding', 'chinese_book_category', 'order'))
	if request.method == 'POST':
		#book info 設定
		bookInfoForm = BookInfoForm(request.POST)
		if not bookInfoForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' + str(bookInfoForm.errors)
			return locals()
		try:
			newBookInfo = BookInfo.objects.get(ISBN=request.POST['ISBN'])
		except:
			newBookInfo = bookInfoForm.save(commit=False)
			newBookInfo.ISBN = request.POST['ISBN']
			newBookInfo.save()
		applyDocumentAction = ApplyDocumentAction.objects.create(book_info=newBookInfo)
		event = Event.objects.create(creater=request.user, action=applyDocumentAction)
		redirect_to = '/'
		status = 'success'
		message = u'成功申請代掃描辨識，請將書籍寄至所選之中心'
		return locals()
	if request.method == 'GET':
		return locals()

def event_list(request, template_name = 'genericUser/event_list.html'):
	events = Event.objects.filter(creater=request.user)
	return render(request, template_name, locals())

@http_response
def org_info(request, template_name='genericUser/org_info.html'):
	org_list = Organization.objects.filter(is_service_center=True)
	if request.method == 'POST':
		return locals()
	if request.method == 'GET':
		return locals()


def license(request, template_name='genericUser/license.html'):
	if request.method == 'POST':
		if 'is_privacy' in request.POST:
			request.user.is_license = True
			request.user.permission.add(Permission.objects.get(codename='license'))
			request.user.save()
		return redirect('/')
	if request.method == 'GET':
		return render(request, template_name, locals())

def func_desc(request, template_name='genericUser/func_desc.html'):
	return render(request, template_name, locals())

@user_category_check(['manager'])
@http_response
def review_user(request, username, template_name='genericUser/review_user.html'):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404("user does not exist")
	events = Event.objects.filter(content_type__model='user', object_id=user.id, status=Event.STATUS['review'])
	sourcePath = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(user.username)
	DCDir = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(user.username)
	DCDir_url = DCDir.replace(BASE_DIR + '/static/', '')
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		for item in ['active', 'editor', 'guest', 'manager', 'advanced_editor', ]:
			exec("user.is_{0} = True if request.POST.has_key('{0}') else False".format(item))
		if request.POST['review'] == 'success':
			user.status = user.STATUS['active']
			user.save()
			redirect_to = reverse('manager:event_list', kwargs={'action': 'user'})
			status = 'success'
			message = u'完成審核權限開通'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		elif request.POST['review'] == 'error':
			redirect_to = reverse('manager:event_list', kwargs={'action': 'user'})
			status = 'success'
			message = u'資料異常退回'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		return locals()

@http_response
def info(request, template_name):
	user = request.user
	DCDir = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(request.user.username)
	DCDir_url = DCDir.replace(BASE_DIR + '/static/', '')
	facebook_association = request.user.social_auth.filter(provider='facebook')
	google_association = request.user.social_auth.filter(provider='google')
	userForm = UserForm(instance=request.user)
	if request.method == 'POST':
		if request.POST.has_key('email') and (not request.user.email == request.POST['email']):
			request.user.email = request.POST['email']
			request.user.auth_email = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		if request.POST.has_key('phone') and (not request.user.phone == request.POST['phone']):
			request.user.phone = request.POST['phone']
			request.user.auth_phone = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		status = u'success'
		message = u'無資料修改。'
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def change_contact_info(request, template_name):
	DCDir = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(request.user.username)
	DCDir_url = DCDir.replace(BASE_DIR + '/static/', '')
	if request.method == 'POST':
		userForm = UserForm(instance=request.user, data=request.POST)
		if not userForm.is_valid():
			status = u'error'
			message = u'表單驗證失敗 {0}'.format(str(userForm.errors))
			return locals()
		user = User.objects.get(username=request.user.username)
		userForm.save()
		if not user.email == userForm.cleaned_data['email']:
			request.user.auth_email = False
			request.user.save()
			status = u'success'
			message = u'修改通訊資料，請重新驗證。'
		if not user.phone == userForm.cleaned_data['phone']:
			request.user.auth_phone = False
			request.user.save()
			status = u'success'
			message = u'修改通訊資料，請重新驗證。'
		try:
			request.user.editor.professional_field = request.POST['professional_field']
			request.user.editor.save()
		except:
			pass
		try:
			handle_uploaded_file(request.user.disability_card_front, request.FILES['disability_card_front'])
			handle_uploaded_file(request.user.disability_card_back, request.FILES['disability_card_front'])
		except:
			pass
		status = u'success'
		message = u'資料修改完成'
		redirect_to = reverse('genericUser:info')
		return locals()
	if request.method == 'GET':
		userForm = UserForm(instance=request.user)
		return locals()

@http_response
def serviceinfo_list(request, template_name='genericUser/serviceinfo_list.html'):
	if request.method == 'GET':
		return locals()
	'''subject = u'[通知] {0} 申請服務時數'.format(request.user.username)
	t = get_template('email/serviceinfo_list.txt')
	body = t.render(Context(locals()))
	email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[exchange_serviceInfo.org.email])
	email.send(fail_silently=False)'''

@http_response
def serviceinfo_list_search(request, username, template_name='genericUser/serviceinfo_list_search.html'):
	search_user = User.objects.get(username=username)
	if request.method == 'GET':
		return locals()

@http_response
def serviceinfo_list_check(request, template_name='genericUser/serviceinfo_list_check.html'):
	return locals()

@http_response
def verify_contact_info(request, template='genericUser/verify_contact_info.html'):
	if not request.is_ajax():
		status = u'error'
		message = u'非ajax請求'
	if request.POST.has_key('generate'):
		if request.POST['generate'] == 'email':
			if not cache.has_key(request.user.email):
				import random
				import string
				vcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				cache.set(request.user.email, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(request.user.email)['vcode']
			subject = u'[驗證] {0} 信箱驗證碼'.format(request.user.username)
			t = get_template('email/email_validate.txt')
			body = t.render(Context(locals()))
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
		elif request.POST['generate'] == 'phone':
			if not cache.has_key(request.user.phone):
				import random
				import string
				vcode = ''.join(random.choice(string.digits) for _ in range(6))
				cache.set(request.user.phone, {'vcode': vcode}, 600)
			else:
				vcode = cache.get(request.user.phone)['vcode']
			data = u'親愛的{0}您的信箱驗證碼為：{1}，請在10分鐘內輸入。\n'.format(request.user.username, vcode)
			url = 'https://api2.kotsms.com.tw/kotsmsapi-1.php?username={0}&password={1}&dstaddr={2}&smbody={3}'.format(
				OTP_ACCOUNT, OTP_PASSWORD, request.user.phone, urllib.quote(data.encode('big5'))
			)
			session = requests.Session()
			response = session.get(url)
			if response.text.split('=')[1] > 0:
				status = 'success'
				message = u'已寄送到您的手機'
			else:
				status = 'error'
				message = u'請確認手機號碼是否正確或聯絡系統管理員'
		return locals()
	if request.POST.has_key('verification_code') and request.POST.has_key('type'):
		if request.POST['type'] == 'email':
			if not cache.has_key(request.user.email):
				status = u'error'
				message = u'驗證碼已過期，請重新產生驗證碼'
				return locals()
			input_vcode = request.POST['verification_code']
			vcode = cache.get(request.user.email)['vcode']
			if input_vcode == vcode:
				status = u'success'
				message = u'信箱驗證通過'
				request.user.auth_email = True
				request.user.save()
			else:
				status = u'error'
				message = u'信箱驗證碼不符'
		if request.POST['type'] == 'phone':
			if not cache.has_key(request.user.phone):
				status = u'error'
				message = u'驗證碼已過期，請重新產生驗證碼'
				return locals()
			input_vcode = request.POST['verification_code']
			vcode = cache.get(request.user.phone)['vcode']
			if input_vcode == vcode:
				status = u'success'
				message = u'手機驗證通過'
				request.user.auth_phone = True
				request.user.save()
			else:
				status = u'error'
				message = u'手機驗證碼不符'
		return locals()

#=====new=====

@http_response
def user_update(request, ID, ):
	if request.method == 'POST' and request.is_ajax():
		user = User.objects.get(id=ID)
		if request.POST['action'] == 'info':
			try:
				userForm = UserForm(data=request.POST, instance=user)
				if not userForm.is_valid():
					raise SystemError(u'資訊輸入錯誤')
				userForm.save()
			except BaseException as e:
				status = 'error'
				message = u'使用者資訊更新失敗：{0}'.format(unicode(e))
				return locals()
			status = 'success'
			message = u'使用者資訊更新成功'
			return locals()
		elif request.POST['action'] == 'info_auth':
			try:
				infoAuthForm = InfoAuthForm(data=request.POST, instance=user)
				if not infoAuthForm.is_valid():
					raise SystemError(u'資訊輸入錯誤')
				user = infoAuthForm.save()
			except BaseException as e:
				status = 'error'
				message = u'使用者資訊更新失敗：{0}'.format(unicode(e))
				return locals()
			status = 'success'
			message = u'使用者資訊更新成功'
			return locals()
		elif request.POST['action'] == 'password':
			try:
				form = PasswordChangeForm(user=user, data=request.POST)
				if not form.is_valid():
					raise SystemError(u'密碼輸入錯誤')
				form.save()
			except BaseException as e:
				status = 'error'
				message = u'使用者密碼更新失敗：{0}'.format(unicode(e))
				return locals()
			status = 'success'
			message = u'使用者密碼更新成功'
			return locals()
		elif request.POST['action'] == 'role':
			try:
				form = RoleForm(instance=user, data=request.POST)
				if not form.is_valid():
					raise SystemError(u'角色權限設定失敗')
				form.save()
			except BaseException as e:
				status = 'error'
				message = u'角色權限設定失敗：{0}'.format(unicode(e))
				return locals()
			status = 'success'
			message = u'角色權限設定成功'
			return locals()

		elif request.POST['action'] == 'disability_card':
			try:
				print user.disability_card_front
				if not os.path.exists(os.path.dirname(user.disability_card_back)):
					os.makedirs(os.path.dirname(user.disability_card_back))
				with open(user.disability_card_back, 'wb') as f:
					image_content = base64.b64decode(request.POST['back'])
					f.write(image_content)
				if not os.path.exists(os.path.dirname(user.disability_card_front)):
					os.makedirs(os.path.dirname(user.disability_card_front))
				with open(user.disability_card_front, 'wb') as f:
					image_content = base64.b64decode(request.POST['front'])
					f.write(image_content)
			except BaseException as e:
				status = 'error'
				message = u'身障手冊上傳失敗：{0}'.format(unicode(e))
				return locals()
			status = 'success'
			message = u'身障手冊上傳成功'
			return locals()

@http_response
def user_view(request, ID):
	if request.method == 'GET' and request.is_ajax():
		user = User.objects.get(id=ID)
		content = user.serialized(request.GET['action'])
		status = 'success'
		message = u''
		return locals()

@http_response
def user_list(request):
	if request.method == 'GET' and request.is_ajax():
		if request.GET['query_field'] == 'all':
			user_list = User.objects.all().order_by('username')
		else:
			user_list = User.objects.filter(**{request.GET['query_field']: request.GET['query_value']}).order_by('username')
		content = [ user.serialized(request.GET['action']) for user in user_list ]
		status = 'success'
		message = u''
		return locals()

@http_response
def user_manager(request, template_name='genericUser/user_manager.html'):
	if request.method == 'GET':
		user_list = User.objects.filter(is_book=True)
		return locals()

@http_response
def announcement_list(request, template_name='genericUser/announcement_list.html'):
	API_list = [reverse('genericUser:api:announcement-list')]
	announcement_lists = [
		(i[0], Announcement.objects.filter(category=i[0]))
		for i in Announcement.CATEGORY
	]
	if request.method == 'GET':
		status = 'success'
		message = u''
		return locals()

@http_response
def announcement(request, ID, template_name='genericUser/announcement.html'):
	API_list = [reverse('genericUser:api:announcement-detail', kwargs={'pk': ID})]
	try:
		announcement = Announcement.objects.get(id=ID)
	except:
		raise Http404("announcement does not exist")
	AnnouncementForm = modelform_factory(Announcement, fields=['category', 'title', 'content', ])
	if request.method == 'POST':
		form = AnnouncementForm(request.POST, instance=announcement)
		if not form.is_valid():
			status = 'error'
			message = u'表單驗證失敗' + unicode(form.errors)
			return locals()
		form.save()
		status = 'success'
		message = u'成功修改公告'
		return locals()
	elif request.method == 'GET':
		status = 'success'
		message = u''
		return locals()

@http_response
def announcement_create(request, template_name='genericUser/announcement_create.html'):
	API_list = [reverse('genericUser:api:announcement-list')]
	announcement_category = Announcement.CATEGORY
	AnnouncementForm = modelform_factory(Announcement, fields=['category', 'title', 'content', ])
	if request.method == 'POST':
		form = AnnouncementForm(request.POST)
		if not form.is_valid():
			status = 'error'
			message = u'表單驗證失敗' + unicode(form.errors)
			return locals()
		form.save()
		status = 'success'
		message = u'成功新增公告'
		return locals()
	elif request.method == 'GET':
		status = 'success'
		message = u''
		return locals()

@http_response
def announcement_update(request, pk, ):
	AnnouncementForm = modelform_factory(Announcement, fields=['category', 'title', 'content', ])
	if request.method == 'POST':
		announcement = Announcement.objects.get(id=pk)
		form = AnnouncementForm(request.POST, instance=announcement)
		if not form.is_valid():
			status = 'error'
			message = u'表單驗證失敗' + unicode(form.errors)
			return locals()
		form.save()
		status = 'success'
		message = u'成功修改公告'
		return locals()
	elif request.method == 'GET':
		status = 'success'
		message = u''
		return locals()

@http_response
def announcement_delete(request, pk):
	if request.method == 'POST' and request.is_ajax():
		announcement = Announcement.objects.get(id=id)
		announcement.delete()
		status = 'success'
		message = u'成功刪除Q&A'
		return locals()

@http_response
def getbookrecord_view(request, username, template_name='genericUser/getbookrecord_view.html'):
	return locals()

from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from genericUser.premissions import IsManager
#@permission_classes((IsManager, ))

class UserResource(Resource):
	resourceClass = User

	def get_fullpath(self, obj, dir, resource):
		fullpath = None
		if dir == 'disability_card':
			if resource == 'front':
				fullpath = obj.disability_card_front
			if resource == 'back':
				fullpath = obj.disability_card_back
		return fullpath

	def get(self, request, pk, dir, resource):
		obj = self.get_object(pk)
		fullpath = self.get_fullpath(obj, dir, resource)
		return self.get_resource(fullpath)

	def post(self, request, pk, dir, resource):
		obj = self.get_object(pk)
		fullpath = self.get_fullpath(obj, dir, resource)
		return self.post_resource(fullpath, request.FILES['object'])

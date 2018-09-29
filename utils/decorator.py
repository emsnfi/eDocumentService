﻿# coding: utf-8
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse,HttpResponseRedirect, FileResponse
from django.shortcuts import render
import json
import mimetypes
import os

def user_category_check(category):
	def user_category_out(view):
		def user_category_in(request, *args, **kwargs):
			response = {}
			if not request.user.is_authenticated():
				template_name = 'user_category_check.html'
				redirect_to = reverse('login')
				status = 'error'
				message = u'您尚未登錄'
				response['redirect_to'] = redirect_to
				response['status'] = status
				response['message'] = message
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			if 'user' in category and request.user.authentication():
				return view(request, *args, **kwargs)
			for permission in [
				'editor',
				'guest',
				'manager',
				'advanced_editor',
				'staff',
				'superuser',
			]:
				if permission in category and getattr(request.user, 'is_' +permission):
					return view(request, *args, **kwargs)

			#無權限
			template_name = 'user_category_check.html'
			redirect_to = reverse('login')
			status = 'error'
			message = u'帳號無權限'
			response['redirect_to'] = redirect_to
			response['status'] = status
			response['message'] = message
			if request.is_ajax():
				return HttpResponse(json.dumps(response), content_type="application/json")
			else:
				return render(request, template_name, locals())

		return user_category_in
	return user_category_out

def get_file(fullpath):
	if not os.path.exists(fullpath):
		raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
	# Respect the If-Modified-Since header.
	statobj = os.stat(fullpath)
	content_type, encoding = mimetypes.guess_type(fullpath)
	content_type = content_type or 'application/octet-stream'
	response = FileResponse(open(fullpath, 'rb'), content_type='application/octet-stream')
	response['Content-Disposition'] = u'attachment; filename="{0}"'.format(os.path.basename(fullpath)).encode('utf-8')
#	response["Last-Modified"] = http_date(statobj.st_mtime)
#	if stat.S_ISREG(statobj.st_mode):
#		response["Content-Length"] = statobj.st_size
	if encoding:
		response["Content-Encoding"] = encoding
	return response

def http_response(view):
	def decorator(request, *args, **kwargs):
		rend_dict = {}
		rend_dict = view(request, *args, **kwargs)
		if request.is_ajax():
			if 'extra_list' not in rend_dict:
				rend_dict['extra_list'] = []
			response = {}
			if 'redirect_to' in rend_dict:
				response['redirect_to'] = rend_dict['redirect_to']
			elif 'content' in rend_dict:
				response['content'] = rend_dict['content']
			elif 'permission_denied' in rend_dict:
				response['permission_denied'] = rend_dict['permission_denied']
			elif 'download_path' in rend_dict:
				fullpath = rend_dict['download_path']
				response = FileResponse(open(fullpath, 'rb'), content_type='application/octet-stream')
				response['Content-Disposition'] = u'attachment; filename="{0}"'.format(rend_dict['download_filename']).encode('utf-8')
				return response
			response['status'] = rend_dict['status']
			response['message'] = rend_dict['message']
			for key in rend_dict['extra_list']:
				response[key] = rend_dict[key]
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			if 'permission_denied' in rend_dict:
				template_name = 'user_category_check.html'
				return render(request, template_name, {})
			elif 'redirect_to' in rend_dict:
				return HttpResponseRedirect(rend_dict['redirect_to'])
			elif 'download_path' in rend_dict:
				fullpath = rend_dict['download_path']
				response = FileResponse(open(fullpath, 'rb'), content_type='application/octet-stream')
				response['Content-Disposition'] = u'attachment; filename="{0}"'.format(rend_dict['download_filename']).encode('utf-8')
				return response
			else:
				return render(request, rend_dict['template_name'], rend_dict)
	return decorator

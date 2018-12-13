from django.conf.urls import include, url

from . import views
from . import apis
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'announcements', apis.AnnouncementViewSet)
router.register(r'organizations', apis.OrganizationViewSet)
router.register(r'businesscontents', apis.BusinessContentViewSet)
router.register(r'qandas', apis.QAndAViewSet)
router.register(r'bannercontents', apis.BannerContentViewSet)
router.register(r'serviceinfos', apis.ServiceInfoViewSet)
router.register(r'users', apis.UserViewSet)
router.register(r'disabilitycards', apis.DisabilityCardViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

import rest_framework

urlpatterns = [
	url(r'^org_info$', views.org_info, name='org_info'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

from django.urls import path
from django.conf.urls import include, url

from . import apis
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'booksimples', apis.BookSimpleViewSet)
router.register(r'books', apis.BookViewSet)
router.register(r'bookadds', apis.BookAddViewSet)
router.register(r'ebooks', apis.EBookViewSet)
router.register(r'bookinfos', apis.BookInfoViewSet)
router.register(r'editrecords', apis.EditRecordViewSet)
router.register(r'libraryrecords', apis.LibraryRecordViewSet)
router.register(r'categorys', apis.CategoryViewSet)
router.register(r'indexcategorys', apis.IndexCategoryViewSet)
router.register(r'bookorders', apis.BookOrderViewSet)

urlpatterns = [path(
	'api/',
	include((router.urls, 'ebookSystem'), 'api'),
)]

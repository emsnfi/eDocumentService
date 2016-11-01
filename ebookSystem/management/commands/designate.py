# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import Book, EBook
import datetime

class Command(BaseCommand):
	help = 'designate ebook'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		for part in EBook.objects.all():
			if part.status == EBook.STATUS['edit'] and part.deadline < datetime.date.today():
				part.editor=None
				part.get_date = None
				part.deadline = None
				part.status = part.STATUS['active']
				part.save()
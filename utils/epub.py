﻿# coding=utf-8
import io
import os
import shutil
import sys
from bs4 import BeautifulSoup, NavigableString
import ebooklib
from ebooklib import epub

def through(src, dst):

	book = epub.read_epub(src)
	epub.write_epub(dst, book, {})
	return book

def add_bookinfo(epubBook, **kwargs):

	for k in epubBook.metadata[epub.NAMESPACES['DC']].keys():
		if k in kwargs.keys():
			del epubBook.metadata[epub.NAMESPACES['DC']][k]

	epubBook.set_title(kwargs['bookname'])
	epubBook.set_language(kwargs['language'])
	epubBook.add_metadata('DC', 'creator', kwargs['author'])
	epubBook.add_metadata('DC', 'source', kwargs['ISBN'])
	epubBook.add_metadata('DC', 'date', kwargs['date'])
	epubBook.add_metadata('DC', 'publisher', kwargs['house'])

	return epubBook

def html2epub(part_list, dst, **kwargs):

	book = epub.EpubBook()
	book = add_bookinfo(book, **kwargs)

	c_list = []
	toc = []
	for i in range(len(part_list)):
		c_soup = BeautifulSoup(open(part_list[i]), 'html5lib')
		c = epub.EpubHtml(
			title=u'{0}-part{1}'.format(kwargs['bookname'], i+1),
			file_name='Text/part{0}.xhtml'.format(i+1),
		)
		c.content = unicode(c_soup)
		book.add_item(c)
		c_list.append(c)
		toc.append(
			epub.Link(
				'Text/part{0}.xhtml'.format(i+1),
				'part{0}'.format(i+1),
				'part{0}'.format(i+1),
			)
		)

	book.toc = toc

	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav(file_name='Text/nav.xhtml'))
	book.spine = ['nav'] +c_list

	epub.write_epub(dst, book, {})

	return book

def txt2epub(src, dst, line_per_chapter=100, **kwargs):

	temp_folder = os.path.join(os.path.dirname(src), 'epub_temp')
	if not os.path.exists(temp_folder):
		os.makedirs(temp_folder)
	part_list = []
	with io.open(src, 'r', encoding='utf-8') as fr:
		for index, line in enumerate(fr.readlines()):
			if index % line_per_chapter == 0:
				part = index/line_per_chapter + 1
				try:
					fw.close()
				except BaseException as e:
					pass
				temp_file = temp_folder +'/part{0}.txt'.format(part)
				fw = io.open(temp_file, 'w', encoding='utf-8')
				part_list.append(temp_file)
			fw.write(line)
		fw.close()

	from tag import add_tag, add_template_tag
	for f in part_list:
		add_tag(f, f,)
		add_template_tag(f, f, )

	book = html2epub(part_list, dst, **kwargs)

	shutil.rmtree(temp_folder)
	return book

def epub2txt(src, dst):
	content = ''
	book = epub.read_epub(src)

	for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
		soup = BeautifulSoup(item.content, 'html5lib')
		content = content +soup.get_text()

	content = content.replace('\n', '\r\n')
	with io.open(dst, 'w', encoding='utf-8') as f:
		f.write(content)

def remove_blankline(src, dst):
	with io.open(src, 'r', encoding='utf-8') as f:
		content = f.readlines()

	with io.open(dst, 'w', encoding='utf-8') as f:
		for l in content:
			if not l.strip() == '':
				f.write(l.replace('\n', '\r\n'))

def remove_multiple_blankline(src, dst):
	blank_flag = False
	with io.open(src, 'r', encoding='utf-8') as f:
		content = f.readlines()

	with io.open(dst, 'w', encoding='utf-8') as f:
		for l in content:
			if not l.strip() == '':
				f.write(l.replace('\n', '\r\n'))
				blank_flag = False
			else:
				if not blank_flag:
					f.write(l.replace('\n', '\r\n'))
					blank_flag = True

if __name__ == '__main__':
	pass
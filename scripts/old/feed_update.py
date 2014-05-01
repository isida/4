#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Feeds updater for iSida Jabber Bot                                       #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

import os,urllib2,sys,re,chardet,hashlib

def smart_encode(text,enc):
	tx,splitter = '','|'
	while text.count(splitter): splitter += '|'
	ttext = text.replace('</','<%s/' % splitter).split(splitter)
	for tmp in ttext:
		try: tx += unicode(tmp,enc)
		except: pass
	return tx

def html_encode(body):
	encidx = body.find('encoding=')
	if encidx >= 0:
		enc = body[encidx+10:encidx+30]
		if enc.count('"'): enc = enc[:enc.find('"')]
		elif enc.count('\''): enc = enc[:enc.find('\'')]
		elif enc.count('&'): enc = enc[:enc.find('&')]
	else:
		encidx = body.find('charset=')
		if encidx >= 0:
			enc = body[encidx+8:encidx+30]
			if enc.count('"'): enc = enc[:enc.find('"')]
			elif enc.count('\''): enc = enc[:enc.find('\'')]
			elif enc.count('&'): enc = enc[:enc.find('&')]
		else: enc = chardet.detect(body)['encoding']
	if body == None: body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while body.count(splitter): splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'): ttext+=tmp2
					else: ttext+='?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try: return smart_encode(body,enc)
		except: return 'Encoding error!'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def getFile(filename,default):
	if os.path.isfile(filename):
		try: filebody = eval(readfile(filename))
		except:
			if os.path.isfile(filename+'.back'):
				while True:
					try:
						filebody = eval(readfile(filename+'.back'))
						break
					except: pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(filename+'.back',str(filebody))
	return filebody

def get_tag(body,tag):
	T = re.findall('<%s.*?>(.*?)</%s>' % (tag,tag),body,re.S)
	if T: return T[0]
	else: return ''

# --------- Settings ----------
set_folder 	= 'settings/'
feeds = set_folder+'feed'
user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'
# -----------------------------

feedbase = getFile(feeds,[])
newfeed = []
for fdd in feedbase:
	link = fdd[0]
	print link,
	if not link[:10].count('://'): link = 'http://'+link
	try:
		if float(sys.version[:3]) >= 2.6: # python 2.6 and higher
			req = urllib2.Request(link.encode('utf-8'))
			req.add_header('User-Agent','user_agent')
			feed = urllib2.urlopen(url=req,timeout=30).read(262144)
		else: feed = urllib.urlopen(link).read()
	except: feed = 'Unable to access server!'
	is_rss_aton,fc = 0,feed[:256]
	if fc.count('<?xml version='):
		if fc.count('<feed'):
			is_rss_aton = 2
			t_feed = feed.split('<title>')
			feed = t_feed[0]
			for tmp in t_feed[1:]:
				tm = tmp.split('</title>',1)
				if ord(tm[0][-1]) == 208: tm[0] = tm[0][:-1] + '...'
				feed += '<title>%s</title>%s' % tuple(tm)
		elif fc.count('<rss') or fc.count('<rdf'): is_rss_aton = 1
		feed = html_encode(feed)
		feed = re.sub(u'(<span.*?>.*?</span>)','',feed)
		feed = re.sub(u'(<div.*?>)','',feed)
		feed = re.sub(u'(</div>)','',feed)
		if is_rss_aton and feed != 'Encoding error!' and feed != 'Unable to access server!':
			print '... readed',
			if is_rss_aton == 1:
				if feed.count('<item>'): fd = feed.split('<item>')
				else: fd = feed.split('<item ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</item>')[0])
			else:
				if feed.count('<entry>'): fd = feed.split('<entry>')
				else: fd = feed.split('<entry ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</entry>')[0])
			break_point = []
			for tmp in feed[1:]:
				ttitle = get_tag(tmp,'title').replace('&lt;br&gt;','\n')
				break_point.append(hashlib.md5(ttitle.encode('utf-8')).hexdigest())
			newfeed.append([link,fdd[1],fdd[2],fdd[3],fdd[4],break_point])
			print '... generated'
		else: print '... fault!'
writefile(feeds,str(newfeed))
print 'done!'

# The end is near!
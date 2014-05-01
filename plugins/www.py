#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) Vit@liy <vitaliy@root.ua>                                  #
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

filename_chars_limit = 48
last_url_watch = ''
url_watch_ignore = ['pdf','sig','spl','class','ps','torrent','dvi','gz','pac','swf','tar','tgz','tar','zip','mp3','m3u','wma',\
					'wax','ogg','wav','gif','jar','jpg','jpeg','png','xbm','xpm','xwd','css','asc','c','cpp','log','conf','text',\
					'txt','dtd','xml','mpeg','mpg','mov','qt','avi','asf','asx','wmv','bz2','tbz','tar','so','dll','exe','bin',\
					'img','usbimg','rar','deb','rpm','iso','ico','apk','patch','svg','7z','tcl']

def rss_search(type, jid, nick, text):
	if text:
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		text = enidna(text)
		msg, result = get_opener(text)
		if result:
			msg = L('Bad url or rss/atom not found!','%s/%s'%(jid,nick))
			page = remove_sub_space(html_encode(load_page(text)))
			page = get_tag(page,'head')
			l = []
			while '<link' in page:
				lnk = get_tag_full(page,'link')
				page = page.replace(lnk,'')
				l.append(lnk)
			if l:
				m = []
				for t in l:
					rss_type = get_subtag(t,'type')
					if rss_type in ['application/rss+xml','application/atom+xml']:
						if rss_type == 'application/rss+xml': rss_type = 'RSS'
						else: rss_type = 'ATOM'
						rss_title = get_subtag(t,'title')
						rss_href = get_subtag(t,'href')
						if rss_href == '/': rss_href = '/'.join(text.split('/',3)[:3]) + rss_href
						m.append('[%s] %s - %s' % (rss_type,rss_href,rss_title))
				if m:
					m = '\n'.join(m)
					msg = L('Found feed(s):%s%s','%s/%s'%(jid,nick)) % ([' ','\n']['\n' in m],unescape(m))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def www_isdown(type, jid, nick, text):
	text = text.strip().lower()
	if text:
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		_,result = get_opener(enidna(text))
		if result: msg = L('It\'s just you. %s is up.','%s/%s'%(jid,nick)) % text
		else: msg = L('It\'s not just you! %s looks down from here.','%s/%s'%(jid,nick)) % text
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def netheader(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		body, result = get_opener(enidna(text))
		if result:
			k = body.headers.keys()
			res = []
			for t in k:
				for tt in body.headers.getheaders(t): res.append('%s: %s' % (t,''.join([[r,'?'][r>'~'] for r in str(tt)])))
			body = '%s\n%s' % (text,'\n'.join(res))
			if regex:
				try:
					mt = re.findall(regex, body, re.S|re.I|re.U)
					if mt != []: body = ''.join(mt[0])
					else: body = L('RegExp not found!','%s/%s'%(jid,nick))
				except: body = L('Error in RegExp!','%s/%s'%(jid,nick))
			body = deidna(body)
	else: body = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, body)

def netwww(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			tmp = regex.split(' ', 1)
			if tmp[0].strip().isdigit():
				n = int(tmp[0])
				regex = tmp[1]
			else:
				n = 1
			text = text.split('\n')[1]
		except: regex = None
		if not re.findall('^http(s?)://',text[:10]): text = 'http://%s' % text
		text = enidna(text)
		msg, result = get_opener(text)
		if result:
			page = remove_sub_space(html_encode(load_page(text)))
			if regex:
				try:
					mt = re.findall(regex, page, re.S|re.I|re.U)
					if mt != []:
						if n:
							msg = unhtml_hard('\n'.join([''.join(t) for t in mt[:n]]))
						else:
							msg = unhtml_hard('\n'.join([''.join(t) for t in mt]))
					else: msg = L('RegExp not found!','%s/%s'%(jid,nick))
				except: msg = L('Error in RegExp!','%s/%s'%(jid,nick))
			else:
				msg = urllib.unquote(unhtml_hard(page).encode('utf8')).decode('utf8', 'ignore')
				if '<title' in page: msg = '%s\n%s' % (rss_replace(get_tag(page,'title')), msg)
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg[:msg_limit])

def get_content_title(link):
	try:
		ll = link.lower()
		for t in url_watch_ignore:
			if ll.endswith('.%s' % t): raise
		link = enidna(link)
		original_page = load_page_size(urllib2.Request(link),8192)
		page = html_encode(original_page)
		if '<title' in page: tag = 'title'
		elif '<TITLE' in page: tag = 'TITLE'
		else: raise
		text = remove_sub_space(get_tag(page,tag).replace('\n',' ').replace('\r',' ').replace('\t',' '))
		while '  ' in text: text = text.replace('  ',' ')
		if text:
			cnt = 0
			for tmp in text: cnt += int(ord(tmp) in [1056,1057])
			if cnt >= len(text)/3: text = remove_sub_space(html_encode(get_tag(original_page,tag)).replace('\n',' ').replace('\r',' ').replace('\t',' '))	
	except: text = ''
	return text.strip()

def parse_url_in_message(room,jid,nick,type,text):
	global last_url_watch
	if type != 'groupchat' or text == 'None' or nick == '' or getRoom(jid) == getRoom(selfjid): return
	if get_level(room,nick)[0] < 4: return
	content_title = None
	if get_config(getRoom(room),'store_users_url'):
		rjid = getRoom(jid)
		for t in text.split():
			link = re.findall(r'(http[s]?://.*)',t)
			if link:
				link = link[0].split(' ')[0].split('"')[0].split('\'')[0]
				if not cur_execute_fetchone('select * from url where room=%s and jid=%s and url=%s',(room,rjid,link)):
					ttext = get_content_title(link)
					if ttext:
						ttext = to_censore(rss_del_html(rss_replace(ttext)),room)
						content_title = [link,ttext]
					else:						
						is_file,ttext = False,''
						ll = link.lower()
						for t in url_watch_ignore:
							if ll.endswith('.%s' % t):
								is_file = True
								break
						if is_file:
							body, result = get_opener(enidna(link))
							if result:
								mt = float(body.headers.get('Content-Length',0))
								if mt: ttext = L('Content length %s','%s/%s'%(jid,nick)) % get_size_human(mt)
								else: ttext = ''
					pprint('Store url: %s in %s/%s' % (link,room,nick),'white')
					cur_execute('insert into url values (%s,%s,%s,%s,%s,%s);',(room,rjid,nick,int(time.time()),link,ttext))
	was_shown = False
	if get_config(getRoom(room),'url_title'):
		try:
			link = re.findall(r'(http[s]?://.*)',text)[0].split(' ')[0].split('"')[0].split('\'')[0]
			if link and last_url_watch != link and pasteurl not in link:
				if content_title and content_title[0] == link: ttext = content_title[1]
				else: ttext = get_content_title(link)
				if ttext:
					pprint('Show url-title: %s in %s' % (link,room),'white')
					was_shown = True
					send_msg(type, room, '', L('Title: %s','%s/%s'%(jid,nick)) % to_censore(rss_del_html(rss_replace(ttext)),room))
					last_url_watch = link
		except: pass
	if not was_shown and get_config(getRoom(room),'content_length'):
		try:
			link = re.findall(u'(http[s]?://[-0-9a-zа-я.]+\/[-a-zа-я0-9._?#=@%/]+\.[a-z0-9]{2,7})',text,re.I+re.U+re.S)[0]
			if link and last_url_watch != link and pasteurl not in link:
				is_file = False
				ll = link.lower()
				for t in url_watch_ignore:
					if ll.endswith('.%s' % t):
						is_file = True
						break
				if is_file:
					last_url_watch = enidna(link)
					body, result = get_opener(last_url_watch)
					pprint('Show content length: %s in %s' % (link,room),'white')
					if result:
						mt = float(body.headers.get('Content-Length',0))
						if mt:
							link_end = urllib2.unquote(last_url_watch.rsplit('/',1)[-1]).decode('utf-8')
							link_end = u'…%s%s' % (['/',''][len(link_end)>filename_chars_limit], link_end[-filename_chars_limit:])
							send_msg(type, room, '', L('Length of %s is %s','%s/%s'%(jid,nick)) % (to_censore(link_end,room),get_size_human(mt)))
		except: pass

global execute

message_act_control = [parse_url_in_message]

execute = [(3, 'www', netwww, 2, 'Show web page.\nwww [count (0 for all)] regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags'),
		   (3, 'header', netheader, 2, 'Show net header'),
		   (3, 'isdown', www_isdown, 2, 'Check works site'),
		   (4, 'rss_search', rss_search, 2, 'Search RSS/ATOM feeds')]

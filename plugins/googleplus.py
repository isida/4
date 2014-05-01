#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
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

# translate: verb,noun,preposition,adverb,adjective,phrase,conjunction,abbreviation,Google URL Shortener/Unshortener,Google QR-code generator

def gcalc(type, jid, nick, text):
	if not text.strip(): msg = L('What?','%s/%s'%(jid,nick))
	else:
		try:
			data = load_page('http://www.google.ru/search?', {'q': '%s=' % text.replace('=','').strip().encode('utf-8'), 'hl': GT('youtube_default_lang')}).decode('utf-8', 'ignore')
			msg = ' '.join([t.strip() for t in re.findall('<span class="cwclet" id="cwles">(.*?)</span> </div> </div>.*?<span class="cwcot" id="cwos">(.*?)</span> <script>',data)[0]])
			msg = msg.replace('<sup>2</sup>',u'²').replace('<sup>3</sup>',u'³') 
		except:
			try: msg = reduce_spaces_all(' '.join(re.findall('<div class="vk_gy vk_sh">(.*?)</div><div class="vk_ans vk_bk">(.*?)</div>',data,re.S)[0])).strip()
			except: msg = L('Google Calculator results not found','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def define(type, jid, nick, text):
	text = text.strip()
	target, define_silent = '', False
	if not text: msg = L('What?','%s/%s'%(jid,nick))
	else:
		if re.search('\A\d+?(-\d+?)? ', text): target, text = text.split(' ', 1)
		data = load_page('http://www.google.com.ua/search?', {'hl': 'ru', 'q': text.encode('utf-8'), 'tbs': 'dfn:1'}).decode('utf-8')
		result = re.findall('<li style="list-style:none">(.+?)</li></ul><div style="color:#551a8b"><cite><span class=bc><a href="/url\?url=(.+?)&amp', data)
		if target:
			try: n1 = n2 = int(target)
			except: n1, n2 = map(int, target.split('-'))
			if n1 + n2 == 0: define_silent, n1, n2 = True, 1, 1
		if not result: msg = [L('I don\'t know!','%s/%s'%(jid,nick)), ''][define_silent]
		else:
			if target and target != '0':
				msg = ''
				if 0 < n1 <= n2 <= len(result):
					for k in xrange(n1 - 1, n2): msg += '%s\n%s\n\n' % (result[k][0], urllib.unquote(result[k][1].replace('%25', '%').encode('utf8')).decode('utf8'))
				else: msg = [L('I don\'t know!','%s/%s'%(jid,nick)), ''][define_silent]
			else:
				result = random.choice(result)
				msg = result[0] + '\n' + urllib.unquote(result[1].replace('%25', '%').encode('utf8')).decode('utf8')
			if '<' in msg and '>' in msg: msg = unhtml_hard(msg)
	if msg: send_msg(type, jid, nick, msg)

def define_message(room, jid, nick, type, text):
	s = get_config(room, 'parse_define')
	if s != 'off':
		if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(room,'define')): return
		troom = cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%room,))
		if troom:
			nowname = getResourse(troom[0])
			text = re.sub('^%s[,:]\ ' % re.escape(nowname), '', text.strip())
			what = re.search([u'^(?:(?:что такое)|(?:кто такой)|(?:кто такая)) ([^?]+?)\?$', u'(?:(?:что такое)|(?:кто такой)) ([^?]+?)\?'][s == 'partial'], text, re.I + re.U + re.S)
			if what:
				access_mode = get_level(room, nick)[0]
				text = 'define 0 %s' % what.group(1)
				com_parser(access_mode, nowname, type, room, nick, text, jid)
				return True

def gdict(type, jid, nick, text):
	text = reduce_spaces_all(text.encode('utf-8')).split(' ')
	if 2 <= len(text) <= 3:
		try: sl, tl, text = text
		except: sl, tl, text = [''] + text
		data = html_encode(load_page('http://translate.google.ru/translate_a/t?', {'client': 'x', 'text': text, 'hl': 'en', 'sl': sl, 'tl': tl}))
		try:
			data = json.loads(data)
			if 'dict' in data: msg = '\n%s' % '\n'.join(['%s: %s' % (L(i['pos']).upper(), ', '.join(i['terms'])) for i in data['dict'] if i['pos']])
			else: msg = L('I can\'t translate it!','%s/%s'%(jid,nick))
		except: msg = L('Command execution error.','%s/%s'%(jid,nick))
	else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def goo_gl_raw(text, is_qr):
	url = text.strip().encode('utf-8')
	if not re.findall('^http(s?)://',url[:10]) and not is_qr: url = 'http://' + url
	if is_qr: regex = 'http://goo\.gl/[a-zA-Z0-9]+?\.qr\Z'
	else: regex = 'http://goo\.gl/[a-zA-Z0-9]+?\Z'
	if not url: msg = L('What?','%s/%s'%(jid,nick))
	elif re.match(regex, url):
		if is_qr: url = url[:-3]
		f = get_opener(url)[0]
		if L('Error! %s','%s/%s'%(jid,nick)) % '' in f: msg = f
		else: msg = urllib.unquote(f.geturl().encode('utf8')).decode('utf8')
	else:
		data = load_page(urllib2.Request('http://goo.gl/api/url', 'url=%s' % urllib.quote(url)))
		if L('Error! %s','%s/%s'%(jid,nick)) % '' in data: msg = data
		else:
			msg = json.loads(data)['short_url']
			if is_qr: msg += '.qr'
	return msg

def goo_gl_qr(type, jid, nick, text): send_msg(type, jid, nick, goo_gl_raw(text, True))

def goo_gl(type, jid, nick, text): send_msg(type, jid, nick, goo_gl_raw(text, False))

global execute, message_control

message_act_control = [define_message]

execute = [(3, 'gcalc', gcalc, 2, 'Google Calculator'),
	(3, 'define', define, 2, 'Definition for a word or phrase.\ndefine word - random define of word or phrase\ndefine N word - N-th define of word or phrase\ndefine a-b word - from a to b defines of word or phrase'),
	#(3, 'ggl', goo_gl, 2, 'Google URL Shortener/Unshortener'),
	#(3, 'qr', goo_gl_qr, 2, 'Google QR-code generator'),
	(3, 'gdict', gdict, 2, 'Google Dictionary\ngdict [from_language] to_language word')]

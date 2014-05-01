#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
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

def bash_org_ru(type, jid, nick, text):
	text = text.strip()
	if not text: url = 'http://bash.org.ru/random'
	elif re.match('\d+$', text): url = 'http://bash.org.ru/quote/%s' % text
	else: url = 'http://bash.org.ru/?text=%s' % urllib.quote(text.encode('cp1251'))
	body = html_encode(load_page(url))
	body = re.findall('<span class="date">(.*?)</span>.*?class="id">(.*?)</a>.*?<div class="text">(.*?)</div>',body,re.S|re.I|re.U)
	try: msg = rss_del_nn(rss_replace('%s %s\n%s' % body[0]))
	except: msg = L('Quote not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def ibash_org_ru(type, jid, nick, text):
	reg_title = '<div class="quothead">.*?<b>#(.*?)</b>'
	reg_body = '<div class="quotbody">(.*?)</div>'
	url_id = 'http://ibash.org.ru/quote.php?id='
	try: url = url_id+str(int(text))
	except: url = 'http://ibash.org.ru/random.php'
	body = html_encode(load_page(url))
	msg = url_id + re.findall(reg_title, body, re.S)[0]
	if msg[-3:] == '???': msg = L('Quote not found!','%s/%s'%(jid,nick))
	else: msg += '\n'+rss_replace(re.findall(reg_body, body, re.S)[0])
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'bash', bash_org_ru, 2, 'Quote from bash.org.ru\nbash [number]'),
		   (3, 'ibash', ibash_org_ru, 2, 'Quote from ibash.org.ru\nibash [number]')]


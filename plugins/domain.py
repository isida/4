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

def domaininfo_raw(type, jid, nick, text):
	text = text.strip().lower()
	while ' \n' in text: text = text.replace(' \n','\n')
	if ''.join(re.findall(u'[-0-9a-zа-я. ]+',text,re.U+re.I)) == text and text.count('.') >= 1 and len(text) > 4:
		if text.startswith('sites '): t, text, regex = 2, text.split(' ')[1], '<h3>(.*?)<br></font><br><br>'
		else: t, regex = 1, '</a><br /><h3>(.*?)<br /></font></blockquote>'
		url = 'http://1whois.ru/index.php?url=%s&t=%s' % (text.encode('idna'),t)
		body = deidna(html_encode(load_page(url).replace('&nbsp;', ' ')))
		try:
			body = re.findall(regex, body, re.S)
			if body: msg = unhtml_hard(''.join(body[0]))
			else: msg = L('No data!','%s/%s'%(jid,nick))
		except: msg = L('Unexpected error','%s/%s'%(jid,nick))
	else: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def domaininfo(type, jid, nick, text):
	text = text.strip().lower()
	while ' \n' in text: text = text.replace(' \n','\n')
	if ''.join(re.findall(u'[-0-9a-zа-я. ]+',text,re.U+re.I)) == text and text.count('.') >= 1 and len(text) > 4:
		if 'sites' in text: t, text, regex, msg = 2, text.split(' ')[1], '<font color="black" size="2">(.*?)</font>', L('Sites at Domain/IP address: %s','%s/%s'%(jid,nick)) % text.split(' ')[1]
		else: t, regex, msg = 1, '<blockquote><font.*?>(.*?)</font></blockquote>', L('Domain/IP address info:','%s/%s'%(jid,nick))
		url = 'http://1whois.ru/index.php?url=%s&t=%s' % (text.encode('idna'),t)
		body = deidna(html_encode(load_page(url).replace('&nbsp;', ' ')))
		try:
			body = re.findall(regex, body, re.S)[0]
			if u'Нет данных!' in body: msg += ' '+ L('No data!','%s/%s'%(jid,nick))
			else:
				tmp_body = {}
				body = replacer(body).split('\n')
				newbody = []
				for tmp in body:
					if ':' in tmp:
						if len(tmp.split(':')[0].split()) <= 2 and len(tmp.split(':')[1]) >= 2:
							if not tmp_body.has_key(tmp.split(':')[1]):
								tmp_body[tmp.split(':')[1]]=tmp.split(':')[0]
								newbody.append(tmp)
					elif tmp.count(' ') <= 4 and not tmp_body.has_key(tmp):
							tmp_body[tmp] = tmp
							newbody.append(tmp)
				msg += '\n'+'\n'.join(newbody)
		except: msg = L('Unexpected error','%s/%s'%(jid,nick))
	else: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'domain_info_raw', domaininfo_raw, 2, 'Domain/IP address whois info.'),
		   (3, 'domain_info', domaininfo, 2, 'Domain/IP address whois info.')]

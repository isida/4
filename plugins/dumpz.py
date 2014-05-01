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

dumpz_var = {'sh':'bash', 'bash':'bash', 'c':'c', 'h':'c', 'html':'html', 'htm':'html', 'python':'python', 'py':'python', 'php':'php', 'css':'css', 'sql':'sql', 'cpp':'cpp', 'hpp':'cpp'}

def dumpz(type, jid, nick, text):
	try:
		p = text.split(' ',1)
		if p[0].lower() in dumpz_var.keys():
			highlighting = dumpz_var[p[0].lower()]
			code = p[1]
		else:
			highlighting = 'text'
			code = text
		values = {'lexer': highlighting, 'code': code.encode('utf-8'),}
		data = urllib.urlencode(values)
		req = urllib2.Request('http://dumpz.org/' ,data,{'Content-type':'application/x-www-form-urlencoded'})
		res = urllib2.urlopen(req)
		link = res.url
		msg = L('Posting by URL: %s','%s/%s'%(jid,nick)) % link
	except:
		msg = L('Unexpected error','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'dumpz', dumpz, 2, 'Posting text&code on dedicated server for easy sharing.\ndumpz text - posting plain text,\ndumpz [sh|c|html|py|php|css|sql|cpp] - posting text with highlighting')]


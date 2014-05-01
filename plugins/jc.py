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

def jc(type, jid, nick, text):
	if not len(text): text = getName(jid)
	try:
		body = json.loads(html_encode(load_page('http://jc.jabber.ru/search.html?%s'.encode("utf-8") % (urllib.urlencode({'json':'1', 'search':text.encode("utf-8")})))))
		if body['result']: msg = L('Found:','%s/%s'%(jid,nick)) + ''.join(['\n%s. %s [%s] %s' % ([t['raiting'],'-'][t['raiting']==''],t['description'],t['jid'],t['current']) for t in body['result']])
		else: msg = L('Not found.','%s/%s'%(jid,nick))
	except: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'jc', jc, 2, 'Show information about conference from jc.jabber.ru.\njc [address]')]

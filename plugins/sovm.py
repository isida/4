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

def sovm(type, jid, nick, text):
	text = text.lower().strip().replace('.',' ').split()
	if text:
		text = '.'.join(text)
		znaki = getFile(data_folder % 'sovmestimosti.txt',{})
		znak = znaki.get(text.encode('utf-8'),None)
		if znak:
			body = html_encode(load_page('http://astro-goroskop.ru/sovmestimosti/%s.html' % znak)).replace('\n',' ')
			if '-' in znak: regexp = 'class="float_img" alt="(.*?)" />(.*?)<script'
			else: regexp = 'class="float_img" alt="(.*?)" />(.*?)<br /><br />'
			body = re.findall(regexp,body,re.S|re.I|re.U)
			if body and len(body[0]) == 2: msg ='\n'.join(t.strip().replace('<br /> <br />','') for t in body[0])
			else: msg = L('Error!','%s/%s'%(jid,nick))
		else: msg = L('Sign not found!','%s/%s'%(jid,nick))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)
global execute
 
execute = [(3, 'sovm', sovm, 2, 'Reconcilability between zodiac signs')]
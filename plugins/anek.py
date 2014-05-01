#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) ferym <ferym@jabbim.org.ru>                                #
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

def anek(type, jid, nick):
	try:
		target = load_page('http://anekdot.odessa.ua/rand-anekdot.php')
		od = re.search('background-color:#FFFFFF\'>',target)
		message = target[od.end():]
		message = message[:re.search('<br>',message).start()]
		message = message.replace('<br />','')
		message = message.strip()
		message = rss_replace(unicode(message,'windows-1251'))
		if type=='groupchat':
			if len(message) < GT('anek_private_limit'): send_msg(type, jid, nick, message)
			else:
				send_msg(type, jid, nick, L('Send for you in private','%s/%s'%(jid,nick)))
				send_msg('chat', jid, nick, message)
				return
		else: send_msg(type, jid, nick, message)
	except: send_msg(type, jid, nick, L('Something broken.','%s/%s'%(jid,nick)))

global execute

execute = [(3, 'anek', anek, 1, 'Show random anecdote | Author: ferym')]

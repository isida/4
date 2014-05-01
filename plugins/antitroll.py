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

def troll(type, jid, nick, text):
	text = text.split('\n')
	r = unicode(text[0])
	try: count = int(text[2])
	except: count = GT('troll_default_limit')
	if count > GT('troll_max_limit'): count = GT('troll_max_limit')
	otake = xmpp.JID(node=getName(jid), domain=getServer(jid), resource=r)
	otake = unicode(otake)
	if len(text)>1: message = text[1]
	else: message = L('You troll!','%s/%s'%(jid,nick))
	tst = GT('troll_sleep_time')
	while count != 0:
		sender(xmpp.Message(otake, message, "chat"))
		time.sleep(tst)
		count -= 1
	send_msg(type, jid, nick, L('Done','%s/%s'%(jid,nick)))

global execute, timer

timer = []

execute = [(9, 'troll', troll, 2, 'Repeat message to private.\ntroll nick\n[text]\n[number]')]

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

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = GT('clear_default_count')
	if cntr > GT('clear_max_count'): cntr = GT('clear_max_count')
	elif cntr < 2: cntr = 2
	cdel,cmode = GT('clear_delay'),get_config(getRoom(jid),'clear_answer') == 'presence'
	clear_msg = L('Clean by %s messages in approximately %s sec.','%s/%s'%(jid,nick)) % (cntr,int(cntr*cdel))
	if cmode: caps_and_send(xmpp.Presence(jid,show=Settings['status'], status=clear_msg, priority=Settings['priority']))
	else: send_msg(type, jid, nick, clear_msg)
	time.sleep(cdel)
	for tmp in range(0,cntr):
		msg = xmpp.Message(jid, '', "groupchat")
		msg.setTag('body')
		sender(msg)
		time.sleep(cdel)
	if cmode: caps_and_send(xmpp.Presence(jid,show=Settings['status'], status=Settings['message'], priority=Settings['priority']))
	else: send_msg(type, jid, nick, L('Cleaned!','%s/%s'%(jid,nick)))

global execute

execute = [(7, 'clear', hidden_clear, 2, 'Hidden cleaning of conference history.')]

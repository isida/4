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

def call_body(type, jid, nick, text):
	skip = 1
	if len(text):
		try:
			reason = text.split('\n')[1]
			text = text.split('\n')[0]
		except: reason = None
		fnd = cur_execute_fetchall('select jid from age where room=%s and (nick=%s or jid=%s) group by jid',(jid,text,text))
		if len(fnd) == 1:
			whojid = getRoom(unicode(fnd[0][0]))
			is_found = 0
			for tmp in megabase:
				if tmp[0] == jid and getRoom(tmp[4]) == whojid:
					is_found = 1
					break
			if is_found: msg = L('%s ishere!','%s/%s'%(jid,nick)) % text
			else:
				msg = L('Invited','%s/%s'%(jid,nick))
				skip = 0
		elif len(fnd) > 1: msg = L('I seen some peoples with this nick. Get more info!','%s/%s'%(jid,nick))
		else: msg = L('I don\'n know %s','%s/%s'%(jid,nick)) % text
	else: msg = L('What?','%s/%s'%(jid,nick))

	if skip: send_msg(type, jid, nick, msg)
	else:
		inv_msg = L('%s invite you to %s','%s/%s'%(jid,nick)) % (nick, jid)
		if reason: inv_msg += ' ' + L('because: %s','%s/%s'%(jid,nick)) % reason
		send_msg('chat',whojid, '',inv_msg)

		inv = xmpp.Message(jid)
		inv.setTag('x', namespace=xmpp.NS_MUC_USER).addChild('invite', {'to':whojid})
		sender(inv)

		send_msg(type, jid, nick, msg)

global execute

execute = [(4, 'invite', call_body, 2, 'Invite to conference.\ninvite nick|jid\n[reason]')]

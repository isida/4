#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) dr.Schmurge <dr.schmurge@isida-bot.com>                    #
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

def adminmail(type, jid, nick, text):
	if len(text):
		if len(text) > GT('amsg_limit_size'): text = text[:GT('amsg_limit_size')]+u'[…]'
		ga = get_level(jid, nick)
		fjid = getRoom(ga[1])
		tmp_lim = GT('amsg_limit')[ga[0]]
		am = cur_execute_fetchone('select time from saytoowner where jid=%s;',(fjid,))
		if am:
			wt = int(am[0]-time.time())
			if wt >= 0:
				send_msg(type, jid, nick, L('Time limit exceeded. Wait: %s','%s/%s'%(jid,nick)) % un_unix(wt,'%s/%s'%(jid,nick)))
				return None
			else: cur_execute('delete from saytoowner where jid=%s;',(fjid,))
		cur_execute('insert into saytoowner values (%s,%s)',(fjid,int(time.time())+tmp_lim))
		msg = L('User %s (%s) from %s at %s send massage to you: %s','%s/%s'%(jid,nick)) % (nick,fjid,jid,time.strftime("%H:%M %d.%m.%y", time.localtime (time.time())),text)
		own = cur_execute_fetchall('select * from bot_owner;')
		if own:
			for ajid in own: send_msg('chat', ajid[0], '', msg)
			send_msg(type, jid, nick, L('Sent','%s/%s'%(jid,nick)))
		else: send_msg(type, jid, nick, L('Owner list is empty!','%s/%s'%(jid,nick)))
	else: send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))

global execute

execute = [(4, 'msgtoadmin', adminmail, 2, 'Send message to bot\'s owner\nmsgtoadmin text')]

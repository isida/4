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

def hide_room(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!','%s/%s'%(jid,nick))
	else:
		hmode = text.split(' ')[0]
		try: hroom = text.split(' ')[1]
		except: hroom = jid
		if hmode == 'show':
			hr = cur_execute_fetchall('select * from hiden_rooms;')
			if len(hr): msg = '%s\n%s' % (L('Hidden conferences:','%s/%s'%(jid,nick)),'\n'.join([t[0] for t in hr]))
			else: msg = L('No hidden conferences.','%s/%s'%(jid,nick))
		elif hmode == 'add':
			if not cur_execute_fetchone('select * from conference where room ilike %s;', ('%s/%%'%getRoom(hroom),)): msg = L('I am not in the %s','%s/%s'%(jid,nick)) % hroom
			elif cur_execute_fetchone('select * from hiden_rooms where room=%s',(hroom,)): msg = L('I\'m already hide a %s','%s/%s'%(jid,nick)) % hroom
			else:
				cur_execute('insert into hiden_rooms values (%s)',(hroom,))
				msg = L('%s has been hidden','%s/%s'%(jid,nick)) % hroom
		elif hmode == 'del':
			if hroom in hr:
				cur_execute('delete from hiden_rooms where room=%s',(hroom,))
				msg = L('%s will be shown','%s/%s'%(jid,nick)) % hroom
			else: msg = L('I\'m not hide room %s','%s/%s'%(jid,nick)) % hroom
		else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'hide', hide_room, 2, 'Hide conference.\nhide [add|del|show] [room@conference.server.tld]')]

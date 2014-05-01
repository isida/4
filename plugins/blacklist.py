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

def leave_room(rjid, reason):
	msg = ''
	cnf = cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%rjid,))
	if cnf:
		cur_execute('delete from conference where room ilike %s;', ('%s/%%'%rjid,))
		leave(rjid, reason)
		msg = L('Leave conference %s\n') % rjid
	return msg

def blacklist(type, jid, nick, text):
	text, msg = unicode(text.lower()), ''
	reason = L('Conference was added in blacklist','%s/%s'%(jid,nick))

	try: cmd,room = text.split(' ',1)
	except: cmd,room = text,''
	if room and '@' not in room: room = '%s@%s' % (room,lastserver)

	if cmd == 'show':
		bl = cur_execute_fetchall('select room from blacklist;')
		if not bl: msg = L('List is empty.','%s/%s'%(jid,nick))
		else: msg = '%s%s' % (L('List of conferences:\n','%s/%s'%(jid,nick)),'\n'.join(['%s. %s' % (t[0]+1,t[1][0]) for t in enumerate(bl)]))
	elif cmd == 'clear':
		msg = L('Cleared.','%s/%s'%(jid,nick))
		cur_execute('delete from blacklist;')
	elif room and cmd == 'add':
		if cur_execute_fetchone('select * from blacklist where room=%s', (room,)): msg = L('This conference already exist in blacklist.','%s/%s'%(jid,nick))
		elif cur_execute_fetchone('select count(*) from conference;')[0]==1 and getRoom(cur_execute_fetchone('select room from conference;')[0]) == room:
			msg =L('You can\'t add last conference in blacklist.','%s/%s'%(jid,nick))
		else:
			msg = leave_room(room, reason)
			cur_execute('insert into blacklist values (%s)', (room,))
			msg += L('Add to blacklist: %s','%s/%s'%(jid,nick)) % room
	elif room and cmd == 'del':
		if cur_execute_fetchone('select * from blacklist where room=%s', (room,)):
			cur_execute('delete from blacklist where room=%s', (room,))
			msg = L('Removed from blacklist: %s','%s/%s'%(jid,nick)) % room
		else: msg = L('Address not in blacklist.','%s/%s'%(jid,nick))
	else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))

	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'blacklist', blacklist, 2, 'Manage of conferences blacklist.\nblacklist add|del|show|clear\nblacklist add|del room@conference.server.tld - add|remove address from blacklist\nblacklist show - show blacklist\nblacklist clear - clear blacklist')]
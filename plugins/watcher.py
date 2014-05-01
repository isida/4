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

watch_time = time.time()
watch_count = 0
watch_reset = True
watch_last_activity = {}
watch_activity = {}

def connect_watch():
	global iq_request, watch_time, game_over, watch_count, bot_exit_type, watch_reset, plugins_reload
	if GT('watcher_self_ping') and (time.time() - watch_time) > GT('watch_size'):
		watch_time = time.time()
		watch_count += 1
		watch_reset = True
		iqid = get_id()
		i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':selfjid}, payload = [xmpp.Node('ping', {'xmlns': xmpp.NS_URN_PING},[])])
		iq_request[iqid]=(time.time(),watcher_reset,['chat',god,'',''],xmpp.NS_URN_PING)
		sender(i)
		to = GT('timeout') - 10
		if to <= 10: to = 600
		while to > 0 and not game_over and not plugins_reload:
			to -= 1
			time.sleep(1)
		if game_over or plugins_reload: return
		if watch_reset:
			pprint('Restart by watcher\'s timeout!','red')
			bot_exit_type, game_over = 'restart', True
			time.sleep(2)

def watch_room_activity():
	if not GT('watcher_room_activity'): return
	global watch_last_activity
	to = int(time.time())-GT('watch_activity_timeout')
	cnf = cur_execute_fetchall('select room from conference;')
	if cnf:
		for t in cnf:
			tmp = t[0]
			try: cw = watch_last_activity[getRoom(tmp)]
			except: cw = to
			if cw < to:
				watch_last_activity[getRoom(tmp)] = int(time.time())
				text = tmp
				if '\n' in text: text,passwd = text.split('\n',2)
				else: passwd = ''
				zz = join(text, passwd)
				while unicode(zz)[:3] == '409':
					time.sleep(1)
					text += '_'
					zz = join(text, passwd)
				time.sleep(1)
				pprint('Low activity! Try rejoin into %s' % text,'white')

def watcher_reset(a,b,c,d,e):
	global watch_reset
	watch_reset = None

def c_watcher(type, jid, nick): send_msg(type, jid, nick, L('Timeout for ask: %s | Timeout for answer: %s | Last ask: %s | Total checks: %s','%s/%s'%(jid,nick)) % (GT('watch_size'),GT('timeout'),un_unix(int(time.time() - watch_time),'%s/%s'%(jid,nick)),watch_count))

def activity_watch(type, jid, nick):
	rooms = cur_execute_fetchall("select split_part(room,'/',1) from conference;")
	cnf = [[watch_activity[t],t] for t in watch_activity.keys()]
	cnf.sort(reverse=1)
	tt = int(time.time())
	msg = '\n'.join(['%s - %s' % (t[1],un_unix(tt-t[0],'%s/%s'%(jid,nick))) for t in cnf])
	rooms = ['%s - %s' % (t[0],L('Unknown','%s/%s'%(jid,nick))) for t in rooms if t[0] not in watch_activity.keys()]
	if rooms: msg = '%s\n%s' % (msg,'\n'.join(rooms))
	msg = L('Last activity in room(s):\n%s','%s/%s'%(jid,nick)) % msg
	if type == 'groupchat':
		send_msg('chat', jid, nick, msg)
		msg = L('Send for you in private','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def connect_watch_uni(room,jid,nick,type,mass):
	global watch_last_activity
	if jid != 'None':
		gr = getRoom(room)
		watch_last_activity[gr] = int(time.time())
		if jid != Settings['jid']: watch_activity[gr] = int(time.time())

global execute, timer

if GT('iq_version_enable'): timer = [connect_watch,watch_room_activity]
presence_control = [connect_watch_uni]
message_control = [connect_watch_uni]

execute = [(6,'watcher',c_watcher,1,'Connection activity control.'),
		   (9,'activity',activity_watch,1,'Show activity of conferences.')]

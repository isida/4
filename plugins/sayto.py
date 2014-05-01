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

last_cleanup_sayto_base = 0

def sayto(type, jid, nick, text):
	while len(text) and text[0] == '\n': text=text[1:]
	while len(text) and (text[-1] == '\n' or text[-1] == ' '): text=text[:-1]

	if text.split(' ')[0] == 'show':
		try: text = text.split(' ',1)[1]
		except: text = ''
		ga = get_level(jid, nick)
		if ga[0] != 9: msg = L('You access level is to low!','%s/%s'%(jid,nick))
		else:
			cm = cur_execute_fetchall('select * from sayto')
			if len(cm):
				msg = ''
				for cc in cm:
					zz = cc[0].split('\n')
					tmsg = '\n' + cc[1] +'/'+ zz[0] +' ('+un_unix(time.time()-int(zz[1]),'%s/%s'%(jid,nick))+'|'+un_unix(GT('sayto_timeout')-(time.time()-int(zz[1])),'%s/%s'%(jid,nick))+') '+L('for','%s/%s'%(jid,nick))+' '+cc[2]+' - '+cc[3]
					if len(text) and text.lower() in tmsg.lower(): msg += tmsg
					elif not len(text): msg += tmsg
				if len(msg): msg = L('Not transfered messages: %s','%s/%s'%(jid,nick)) % msg
				else: msg = L('Not found!','%s/%s'%(jid,nick))
				if type == 'groupchat':
					send_msg('chat', jid, nick, msg)
					msg = L('Sent in private message','%s/%s'%(jid,nick))
			else: msg = L('List is empty.','%s/%s'%(jid,nick))
	elif ' ' in text or '\n' in text:
		if '\n' in text: splitter = '\n'
		else: splitter = ' '
		to,what = text.split(splitter,1)[0],text.split(splitter,1)[1]
		frm = '%s\n%s' % (nick,int(time.time()))
		fnd = cur_execute_fetchall('select jid, status from age where room=%s and nick=%s group by jid, status',(jid,to))
		if len(fnd) == 1:
			if fnd[0][1]:
				msg = L('I will convey your message.','%s/%s'%(jid,nick))
				cur_execute('insert into sayto values (%s,%s,%s,%s)', (frm, jid, fnd[0][0], what))
			else: msg = L('Or am I a fool or %s is here.','%s/%s'%(jid,nick)) % to
		elif len(fnd) > 1:
			off_count = 0
			for tmp in fnd:
				if tmp[1]:
					cur_execute('insert into sayto values (%s,%s,%s,%s)', (frm, jid, tmp[0], what))
					off_count += 1
			if off_count: msg = L('I seen some people with this nick, and I can convey is incorrect. Coincidence: %s, and count convey messages: %s','%s/%s'%(jid,nick)) % (str(len(fnd)), str(off_count))
			else: msg = L('All people with this nickname are here!','%s/%s'%(jid,nick))
		else:
			if '@' in to:
				fnd = cur_execute_fetchall('select jid, status from age where room=%s and jid=%s group by jid,status',(jid,to))
				if fnd:
					off_count = 0
					for tmp in fnd:
						if tmp[1]:
							cur_execute('insert into sayto values (%s,%s,%s,%s)', (frm, jid, tmp[0], what))
							off_count += 1
					if off_count: msg = L('I will convey your message.','%s/%s'%(jid,nick))
					else: msg = L('This jid is here!','%s/%s'%(jid,nick))
				else:
					msg = L('I didn\'t seen user with jid %s, but if he join here I convey your message.','%s/%s'%(jid,nick)) % to
					cur_execute('insert into sayto values (%s,%s,%s,%s)', (frm, jid, to, what))
			else: msg = L('I didn\'t see user with nick %s. You can use jid.','%s/%s'%(jid,nick)) % to
	else: msg = L('What convey to?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def say_memo(type, jid, nick, text):
	while len(text) and text[0] == '\n': text=text[1:]
	while len(text) and (text[-1] == '\n' or text[-1] == ' '): text=text[:-1]
	gj = getRoom(get_level(jid, nick)[1])
	if text.split(' ')[0] == 'show':
		try: text = text.split(' ',1)[1]
		except: text = ''
		t = cur_execute_fetchall('select message,jid from sayto where room=%s and jid ilike %s', (jid,gj))
		if t: msg = '\n%s' % '\n'.join([u'• %s' % tmp[0] for tmp in t])
		else: msg = L('There is no memo for you!','%s/%s'%(jid,nick))
	elif text:
		cur_execute('insert into sayto values (%s,%s,%s,%s)', ('\n%s' % int(time.time()), jid, gj, text))
		msg = L('I\'ll remember it to you.','%s/%s'%(jid,nick))
	else: msg = L('What remember to you?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def sayto_presence(room,jid,nick,type,text):
	global conn
	if nick != '' and type != 'unavailable':
		cm = cur_execute_fetchall('select * from sayto where room=%s and (jid=%s or jid=%s)',(room, getRoom(jid), nick))
		if cm:
			cur_execute('delete from sayto where room=%s and (jid=%s or jid=%s)',(room, getRoom(jid), nick))
			for cc in cm:
				if '\n' in cc[0]:
					zz = cc[0].split('\n')
					if zz[0]: msg = L('%s (%s ago) convey for you: %s','%s/%s'%(room,nick)) % (zz[0], un_unix(time.time()-int(zz[1]),'%s/%s'%(room,nick)), cc[3])
					else: msg = L('You ask remember: %s','%s/%s'%(room,nick)) % cc[3]
				else: msg = L('%s convey for you: %s','%s/%s'%(room,nick)) % (cc[3], cc[0])
				send_msg('chat', room, nick, msg)

def cleanup_sayto_base():
	global last_cleanup_sayto_base
	ctime = int(time.time())
	if ctime-last_cleanup_sayto_base > GT('sayto_cleanup_time'):
		last_cleanup_sayto_base = ctime
		cm = cur_execute_fetchall('select who, room, jid from sayto')
		if len(cm):
			for cc in cm:
				if '\n' in cc[0]:
					tim = int(cc[0].split('\n')[1])
					if ctime-tim > GT('sayto_timeout'): cur_execute('delete from sayto where room=%s and jid=%s',(cc[1], cc[2]))
				else: cur_execute('delete from sayto where room=%s and jid=%s',(cc[1], cc[2]))

def sayjid(type, jid, nick, text):
	try:
		text = text.split(' ',1)
		if len(text) != 2: msg = L('Error!','%s/%s'%(jid,nick))
		elif '@' not in text[0] and '@' not in text[0]: msg = L('Error!','%s/%s'%(jid,nick))
		elif not len(text[1]): msg = L('Error!','%s/%s'%(jid,nick))
		else:
			send_msg(type, jid, nick, L('Sent','%s/%s'%(jid,nick)))
			msg = L('%s from conference %s convey message for you: %s','%s/%s'%(jid,nick)) % (nick, jid, text[1])
			type, nick, jid = 'chat', '', text[0]
	except: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute, timer, presence_control

timer = [cleanup_sayto_base]
presence_control = [sayto_presence]
execute = [(3, 'sayto', sayto, 2, '"Say to" command.\nsayto jid|nick message - if jid or nick join in conference, bot send "message". Messages saves 14 days, after if message didn\'t be send this message remove.'),
			(7, 'sayjid', sayjid, 2, 'Send message to jid\n sayjid jid message.'),
			(3, 'memo', say_memo, 2, 'Send a message to yourself at next join')]

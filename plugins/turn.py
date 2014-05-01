#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) Vit@liy <vitaliy@root.ua>                                  #
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

turn_base = []

def turner_raw(text,jid,nick):
	global turn_base
	rtab = L('qwertyuiop[]asdfghjkl;\'zxcvbnm,.`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~','%s/%s'%(jid,nick))
	ltab = L('QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~qwertyuiop[]asdfghjkl;\'zxcvbnm,.`','%s/%s'%(jid,nick))
	to_turn = text
	if not text:
		for tmp in turn_base:
			if tmp[0] == jid and tmp[1] == nick:
				turn_base.remove(tmp)
				to_turn = tmp[2]
				break
	if to_turn:
		if to_turn[:3] == '/me': msg, to_turn = '*%s' % nick, to_turn[3:]
		elif ': ' in to_turn: msg, to_turn = '%s:' % to_turn.split(': ',1)[0], to_turn.split(': ',1)[1]
		else: msg = ''
		for tt in re.findall('\s+[^\s]*', ' ' + to_turn,re.I+re.U):
			if re.findall('\s+(((svn|http[s]?|ftp)(://))|(magnet:\?))',tt,re.S|re.I|re.U): msg += tt
			else: msg += ''.join([ltab[rtab.find(x)] if x in rtab else x for x in tt])
		msg = msg.strip()
		if get_config(getRoom(jid),'censor'): msg = to_censore(msg,jid)
		return msg
	else: return None

def turner(type, jid, nick, text):
	if not text and type != 'groupchat':
		send_msg(type, jid, nick, L('Not allowed in private!','%s/%s'%(jid,nick)))
		return
	to_turn = turner_raw(text,jid,nick)
	if to_turn: send_msg(type, jid, [nick,''][type=='groupchat'], to_turn)
	else: send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))

def append_to_turner(room,jid,nick,type,text):
	global turn_base
	for tmp in turn_base:
		if tmp[0] == room and tmp[1] == nick:
			try: turn_base.remove(tmp)
			except: pass
			break
	turn_base.append((room,nick,text))

def remove_from_turner(room,jid,nick,type,text):
	global turn_base
	if type == 'unavailable':
		for tmp in turn_base:
			if tmp[0] == room and tmp[1] == nick:
				try: turn_base.remove(tmp)
				except: pass
				break

def autoturn(room,jid,nick,type,text):
	if get_config(room,'autoturn') and type == 'groupchat':
		if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(room,'turn')): return
		nowname = get_xnick(room)
		if nick == nowname: return
		text = re.sub('^%s[,:]\ ' % re.escape(nowname), '', text.strip())
		tmp = text.lower()
		if ': ' in tmp: tmp = tmp.split(': ',1)[1]
		count_two = 0
		if not sum([int(ord(t)>127) for t in tmp]):
			for tt in re.findall('\s+[^\s]*', ' ' + tmp):
				if not re.findall('(svn|http[s]?|ftp)(://)',tt,re.S|re.U) and not re.findall(u'\s+[A-ZА-Я\d\']{2,}$',tt,re.U): count_two += sum([1 for k in two_en if k in tt])
			if len(tmp.split()) < count_two - 1:
				to_turn = turner_raw(text,room,nick)
				if to_turn and to_turn != text:
					pprint('Autoturn text: %s/%s [%s] %s > %s' % (room,nick,jid,text,to_turn),'dark_gray')
					send_msg(type, room, '', to_turn)
				return True

global execute, message_act_control

message_control = [append_to_turner]
presence_control = [remove_from_turner]
message_act_control = [autoturn]

execute = [(3, 'turn', turner, 2, 'Turn text from one layout to another.')]
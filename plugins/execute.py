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

calc_last_res = {}

def exec_ute(type, jid, nick, text):
	try: text = remove_sub_space(unicode(eval(text)))
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		text = L('I can\'t execute it! Error: %s','%s/%s'%(jid,nick)) % SM[:int(msg_limit/2)]
	send_msg(type, jid, nick, text)

def calc(type, jid, nick, text):
	global calc_last_res
	if 'Ans' in text and calc_last_res.has_key(jid) and calc_last_res[jid].has_key(nick) and calc_last_res[jid][nick]:
		text = text.replace('Ans', calc_last_res[jid][nick])
	legal = string.digits + string.letters + '*/+-()=^!<>. '
	ppc = 1
	if '**' in text or 'pow' in text or 'factorial' in text: ppc = 0
	else:
		for tt in text:
			if tt not in legal:
				ppc = 0
				break
	if ppc:
		text = re.sub('([^.0-9]\d+)(?=([^.0-9]|$))', r'\1.0', text)
		try:
			text = remove_sub_space(str(eval(re.sub('([^a-zA-Z]|\A)([a-zA-Z])', r'\1math.\2', text))))
			if text[-2:] == '.0': text = text[:-2]
			if calc_last_res.has_key(jid): calc_last_res[jid][nick] = text
			else: calc_last_res[jid] = {nick: text}
		except:
			text = L('I can\'t calculate it','%s/%s'%(jid,nick))
			if calc_last_res.has_key(jid): calc_last_res[jid][nick] = None
			else: calc_last_res[jid] = {nick: None}
	else:
		text = L('Expression unacceptable!','%s/%s'%(jid,nick))
		if calc_last_res.has_key(jid): calc_last_res[jid][nick] = None
		else: calc_last_res[jid] = {nick: None}
	send_msg(type, jid, nick, text)

def dpi_calc(type, jid, nick, text):
	text = text.strip().replace(',','.')
	if text:
		tupl = re.findall('([0-9.]+)',text)[:3]
		if len(tupl) == 3:
			if '.' in tupl[0] or '.' in tupl[1]: msg = L('Width and height must be integer!','%s/%s'%(jid,nick))
			elif not float(tupl[2]): msg = L('Incorrect diagonal value!','%s/%s'%(jid,nick))
			else:
				dpi_type = [0,'L'],[160,'M'],[240,'H'],[320,'XH']
				dpi = int((math.sqrt(int(tupl[0])**2+int(tupl[1])**2))/float(tupl[2]))
				dpi_name = 'unknown'
				for t in dpi_type:
					if dpi > t[0]: dpi_name = '%sDPI' % t[1]
				msg = u'%s %s×%s×%s\" - %sdpi [%s]' % (L('Screen','%s/%s'%(jid,nick)),tupl[0],tupl[1],tupl[2],dpi,dpi_name)
		else: msg = L('Not enough parameters!','%s/%s'%(jid,nick))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def calc_clear(room,jid,nick,type,arr):
	if type == 'unavailable' and calc_last_res.has_key(room) and calc_last_res[room].has_key(nick): del calc_last_res[room][nick]

global execute, presence_control

presence_control = [calc_clear]

if not GT('paranoia_mode'): execute = [(3, 'calc', calc, 2, 'Calculator.'),
	(9, 'exec', exec_ute, 2, 'Execution of external code.')]
else: execute = []

execute.append((3, 'dpi', dpi_calc, 2, 'DPI calculator.\ndpi <width height size>'))

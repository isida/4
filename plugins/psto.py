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

PSTO_JID = 'psto@psto.net/Psto'
PSTO_ERROR = '\nYou cannot read this psto.'
psto_msg_trunc = 64
psto_id = {}

def psto(type, jid, nick, text):
	global psto_id
	if not len(text) or len(text) == text.count(' '):
		send_msg(type, jid, nick, L('What message do you want to find?','%s/%s'%(jid,nick)))
		return
	try:
		psto_idn,psto_comm = re.findall('#?([a-z]{5,})\/?([0-9]*\-*[0-9]*)?',text)[0]
		if psto_idn:
			psto_id[psto_idn] = '%s\n%s\n%s\n%s' % (type,jid,nick,psto_comm)
			send_msg('chat', PSTO_JID, '', '#%s+' % psto_idn)
		else: send_msg(type, jid, nick, L('Smoke help about command!','%s/%s'%(jid,nick)))
	except: send_msg(type, jid, nick, L('Smoke help about command!','%s/%s'%(jid,nick)))

def psto_catch(room,jid,nick,type,text):
	global psto_id
	if '%s/%s' % (room,nick) != PSTO_JID: return
	if text == PSTO_ERROR:
		(type,jid,nick,psto_comm) = psto_id.popitem()[1].split('\n')
		send_msg(type, jid, nick, text[1:])
	else:
		try:
			psto_idn, text = text.split(' ',1)[0][2:],text[1:]
			(type,jid,nick,psto_comm) = psto_id.pop(psto_idn).split('\n')
			splitter = re.findall('http\:\/\/[-a-z0-9]+?\.psto\.net\/%s' % psto_idn, text, re.S|re.I|re.U)[0]
			while '\n\n' in text: text = text.replace('\n\n','\n')
			while '\n ' in text: text = text.replace('\n ','\n')
			if psto_comm:
				new_text = text.split(splitter)[0][:-1]
				comment = new_text.split('\n')[-1]
				new_text = '\n'.join(new_text.split('\n')[:-1])
				if len(new_text) > psto_msg_trunc: new_text = new_text[:psto_msg_trunc] + u'…'
				new_text += '\n%s | %s' % (comment,splitter)
				if '-' in psto_comm: psto_comm = psto_comm.split('-',1)
				else: psto_comm = [psto_comm,psto_comm]
				if not psto_comm[0]: psto_comm[0] = '1'
				if not psto_comm[1]: psto_comm[1] = str(len(text.split(psto_idn)))
				if len(psto_comm[0]) > 3: psto_comm[0] = psto_comm[0][:3]
				if len(psto_comm[1]) > 3: psto_comm[1] = psto_comm[1][:3]
				msg = ''
				for tmp in range(int(psto_comm[0]),int(psto_comm[1])+1):
					try: msg += u'• #%s/%s %s' % (psto_idn,tmp,text.split(splitter)[1].split('#%s/%s' % (psto_idn,tmp))[1].split('#%s/%s' % (psto_idn,tmp+1))[0].replace('\n',' ',1))
					except: pass
				new_text += '\n' + msg
			else: new_text = text.split(splitter)[0][:-1] + ' ' + splitter
			send_msg(type, jid, nick, new_text)
		except: pass

def psto_post(type, jid, nick, text):
	send_msg('chat', PSTO_JID, '', text)
	time.sleep(1.2)
	send_msg(type, jid, nick, L('Message posted to Psto.','%s/%s'%(jid,nick)))

global execute,message_control

message_control = [psto_catch]

execute = [(3, 'psto', psto, 2, 'Miniblogs http://psto.net\npsto [#]post[/[from_comment][-][to_comment]] - show post'),
		   (9, 'psto_post', psto_post, 2, 'Send message to blog at psto.net')]

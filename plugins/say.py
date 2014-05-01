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

def say(type, jid, nick, text):
	text = random.choice(re.split(r'(?<!\\)\|', text)).replace('\\|', '|')
	send_msg('groupchat', jid, '', to_censore(text,jid))

def psay(type, jid, nick, text):
	try:
		if '\n' in text: nnick,ntext = text.split('\n',1)
		else: nnick,ntext = text.split(' ',1)
		send_msg('chat', jid, nnick, to_censore(ntext,jid))
	except: send_msg(type, jid, nick, L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick)))

def gsay(type, jid, nick, text):
	for jjid in [t[0] for t in cur_execute_fetchall('select room from conference;')]: send_msg('groupchat', getRoom(jjid), '', text)

def set_topic(type, jid, nick, text):
	sender(xmpp.Message(jid, subject=text, typ='groupchat'))

global execute

execute = [(6, 'say', say, 2, '"Say" command. Bot say in conference text after command. Example:\nsay text1[|text2[|text3[...]]]'),
	 (6, 'psay', psay, 2, '"Say" command. Bot say in private all text after command.\npsay <nick>\ntext'),
	 (9, 'gsay', gsay, 2, 'Global message in all conferences, where bot is present.'),
	 (7, 'topic', set_topic, 2, 'Set conference topic.')]

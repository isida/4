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

def private_paste(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!','%s/%s'%(jid,nick))
	else: msg = paste_text(text,jid,get_level(jid,nick)[1])
	send_msg(type, jid, nick, msg)

def public_paste(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!','%s/%s'%(jid,nick))
	else: msg,type,nick = L('%s pasted by %s','%s/%s'%(jid,nick)) % (paste_text(text,jid,get_level(jid,nick)[1]),nick),'groupchat',''
	send_msg(type, jid, nick, msg)

global execute

execute = [(4, 'paste', public_paste, 2, 'Paste some text to server'),
		   (5, 'ppaste', private_paste, 2, 'Paste some text to server')]

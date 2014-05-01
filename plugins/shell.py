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

def shell(type, jid, nick, text):
	sysshell(type, jid, nick, text, 1)

def shell_silent(type, jid, nick, text):
	sysshell(type, jid, nick, text, 0)

def sysshell(type, jid, nick, text, mode):
	msg = shell_execute(text,'%s/%s'%(jid,nick))
	if mode: send_msg(type, jid, nick, msg)

global execute

if not GT('paranoia_mode'): execute = [(9, 'sh', shell, 2, 'Execute shell command.'),
	   (9, 'sh_silent', shell_silent, 2, 'Execute shell command without output result.')]

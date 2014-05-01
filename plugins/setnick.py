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

def set_nickname(type, jid, nick, text):
	if get_affiliation(jid,nick) == 'owner' or get_level(jid,nick)[0] == 9:
		msg = None
		nickname = Settings['nickname']
		text = '%s/%s' % (jid, text or nickname)
		bot_join(type, jid, nick, text)
	else:
		msg = L('You can\'t do it!','%s/%s'%(jid,nick))
		send_msg(type, jid, nick, msg)

global execute

execute = [(8, 'setnick', set_nickname, 2, 'Change bot nick. Available only for conference owner.')]

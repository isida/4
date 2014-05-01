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

def to_private(type, room, nick, text): raw_redirect('chat', room, nick, text)

def to_public(type, room, nick, text): raw_redirect('groupchat', room, nick, text)

def raw_redirect(type, room, nick, text):
	access_mode,jid = get_level(room,nick)
	com_parser(access_mode, get_xnick(room), type, room, nick, text, jid)

global execute

execute = [(3, 'private', to_private, 2, 'Redirect command output in private.'),
		   (3, 'public', to_public, 2, 'Redirect command output in groupchat.')]

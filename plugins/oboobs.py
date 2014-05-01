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

def oboobs(type, jid, nick):
	try: msg = 'http://media.oboobs.ru/%s' % json.loads(load_page('http://api.oboobs.ru/noise/1/'))[0]['preview']
	except: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def obutts(type, jid, nick):
	try: msg = 'http://media.obutts.ru/%s' % json.loads(load_page('http://api.obutts.ru/noise/1/'))[0]['preview']
	except: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'oboobs', oboobs, 1, 'Show random picture from oboobs.ru'),
		   (3, 'obutts', obutts, 1, 'Show random picture from obutts.ru')]

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

def md5body(type, jid, nick, text):
	if len(text): msg = hashlib.md5(text.encode('utf-8')).hexdigest()
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def hashbody(type, jid, nick, text):
	text = reduce_spaces_all(text)
	if not len(text): text = nick
	try: msg = hashes['%s/%s' % (jid,text)]
	except: msg = L('Nick %s not found!','%s/%s'%(jid,nick)) % text
	send_msg(type, jid, nick, msg)

def findhash(type, jid, nick, text):
	text = reduce_spaces_all(text)
	if text:
		h = [t for t in hashes if hashes[t]==text]
		if h: msg = L('Found: %s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join(h)
		else: msg = L('Not found: %s','%s/%s'%(jid,nick)) % text
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'md5', md5body, 2, 'Calculate phrase md5 sum.'),
		   (4, 'hashbody', hashbody, 2, 'Show presence-hash of nick'),
		   (6, 'findhash', findhash, 2, 'Show room and nick by presence-hash')]

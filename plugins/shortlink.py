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

SHORT_TINYURL = 'http://tinyurl.com/api-create.php?url=%s'
SHORT_CLCK = 'http://clck.ru/--?url=%s'
SHORT_QR = 'http://chart.apis.google.com/chart?cht=qr&chs=350x350&chld=M|2&chl=%s'

def shorter_raw(type, jid, nick, text, url):
	text = text.strip()
	if text: msg = load_page(url % enidna(text).decode('utf-8'))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def short_clck(type, jid, nick, text): shorter_raw(type, jid, nick, text, SHORT_CLCK)

def short_tinyurl(type, jid, nick, text): shorter_raw(type, jid, nick, text, SHORT_TINYURL)

def short_qr(type, jid, nick, text): shorter_raw(type, jid, nick, text, SHORT_TINYURL % SHORT_QR)

global execute

execute = [(3, 'clck', short_clck, 2, 'URL Shortener'),
		   (3, 'tinyurl', short_tinyurl, 2, 'URL Shortener'),
		   (3, 'qr', short_qr, 2, 'QR-code generator')]

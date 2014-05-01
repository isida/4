#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) Vit@liy <vitaliy@root.ua>                                  #
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

def spell(type, jid, nick, text):
	tmp = text.strip().split(' ', 1)
	if tmp[0]:
		langs = re.sub('-|:;', ',', tmp[0]).lower()
		if len(tmp) == 2 and re.match('((uk)|(en)|(ru))(,((uk)|(en)|(ru)))*?$', langs): text = tmp[1].encode('utf-8')
		else: text, langs = text.encode('utf-8'), ''
		url = 'http://speller.yandex.net/services/spellservice.json/checkText?text=%s&lang=%s&options=7' % (urllib.quote_plus(text), langs)
		j = json.loads(load_page(url),encoding='utf-8')
		msg = text.decode('utf-8')
		deltapos = 0
		for err in j:
			try:
				msg = msg[:err['pos']+deltapos] + err['s'][0] + msg[err['len']+err['pos']+deltapos:]
				deltapos += len(err['s'][0]) - err['len']
			except: pass
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(0, 'spell', spell, 2, 'Spellchecker. Example: spell [uk|ru|en] sentence')]
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

kinopoisk_error_string = '<META HTTP-EQUIV="Pragma" CONTENT="no-cache">'

def kinopoisk(type, jid, nick, text):
	text=text.strip()
	if len(text) > 2:
		query=urllib.quote(text.encode('cp1251'))
		data = html_encode(load_page('http://m.kinopoisk.ru/search/'+query))
		if kinopoisk_error_string in data: msg = unhtml_hard(re.findall(kinopoisk_error_regexp,data,re.I+re.U+re.S)[0])
		else:
			temp_urls = re.findall('<a href="http://m.kinopoisk.ru/movie/(\d+?)/">(.+?)</a>', data)
			if temp_urls:
				msg = L('Found:','%s/%s'%(jid,nick))
				for n, t_u in enumerate(temp_urls):
					rs = ''
					if n < 3:
						try:
							r = load_page('http://www.kinopoisk.ru/rating/%s.xml' % t_u[0])
							r = re.findall('>([\.\d]+?)<', r)
							rs = ' (KP: %s / IMDB: %s)' % (r[0], r[1])
						except:
							pass
					msg += '\nhttp://www.kinopoisk.ru/film/%s/ - %s%s' % (t_u[0], t_u[1], rs)
			else: msg = L('Not found!','%s/%s'%(jid,nick))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(0, 'film', kinopoisk, 2, 'Search in www.kinopoisk.ru. Example:\nfilm film_name')]

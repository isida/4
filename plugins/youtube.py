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

def youtube(type, jid, nick, text):
	if '\n' in text:
		try: lim = int(text.split('\n',1)[1])
		except: lim = GT('youtube_default_videos')
		if lim > GT('youtube_max_videos'): lim = GT('youtube_max_videos')
		if lim < 1: lim = 1
		text = text.split('\n',1)[0]
	else: lim = GT('youtube_default_videos')
	req = text.lower().encode("utf-8").replace(' ','+')
	url = 'http://gdata.youtube.com/feeds/api/videos?q=%s&alt=json-in-script&callback=yt&max-results=%s&format=5'
	res = json.loads(load_page(url % (req,lim)).split('yt(',1)[1][:-2])['feed']
	if res.has_key('entry'):
		msg = L('Found:','%s/%s'%(jid,nick))
		for t in res['entry']:
			y_title = t['title']['$t']
			try: y_views = t['yt$statistics']['viewCount']
			except: y_views = ''
			y_link  = t['media$group'][u'media$player'][0]['url'].split('?v=',1)[1].split('&')[0]
			y_time  = t['media$group'][u'media$thumbnail'][0]['time'].split('.',1)[0]
			msg += unescape('\nhttp://youtu.be/%s - %s [%s] %s' % (y_link,y_title,y_time,y_views))
	else: msg = L('Not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'youtube', youtube, 2, 'Search at YouTube')]

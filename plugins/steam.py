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

#http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=xxxx&steamids=76561198018559638
#http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=xxxx&steamid=76561198018559638&relationship=friend

steam_api_url = 'http://api.steampowered.com/ISteamUser/%s'
steam_summary = steam_api_url % 'GetPlayerSummaries/v0002/?'
steam_friends = steam_api_url % 'GetFriendList/v0001/?'

def time_str(t):
	try: return time.strftime('%Y.%m.%d %H:%M',time.localtime(t))
	except: return t

def steam(type, jid, nick, text):
	text = text.strip().split()
	need_id = len(text) > 1
	text = text[0]
	if text.isdigit():
		STEAM_API = GT('steam_api_key')
		if len(STEAM_API) == 32:
			try:
				data = load_page(steam_summary, {'key': STEAM_API, 'steamids': text})
				data = json.loads(data)['response']['players']
				if data:
					data = data[0]
					_PERSONANAME = data.get('personaname',L('Unknown','%s/%s'%(jid,nick)))
					_REALNAME = data.get('realname',L('Unknown','%s/%s'%(jid,nick)))
					_LOCCOUNTRYCODE = data.get('loccountrycode',L('Unknown','%s/%s'%(jid,nick)))
					_TIMECREATED = data.get('timecreated',L('Hidden','%s/%s'%(jid,nick)))
					_LASTLOGOFF = data.get('lastlogoff',L('Hidden','%s/%s'%(jid,nick)))
					_PROFILEURL = data.get('profileurl',L('Unknown','%s/%s'%(jid,nick)))
					data = load_page(steam_friends, {'key': STEAM_API, 'steamid': text, 'relationship': 'friend'})
					if data.startswith(L('Error! %s')%''):
						_FRIENDS = L('Hidden','%s/%s'%(jid,nick))
						_LEN_FRIENDS = L('Unknown','%s/%s'%(jid,nick))
					else:
						data = json.loads(data)['friendslist']['friends']
						_FRIENDS = ','.join(t['steamid'] for t in data)
						data = load_page(steam_summary, {'key': STEAM_API, 'steamids': _FRIENDS})
						data = json.loads(data)['response']['players']
						_FRIENDS = [(t.get('personaname','-'),t['steamid']) for t in data]
						_LEN_FRIENDS = len(_FRIENDS)
						if need_id: _FRIENDS = ' | '.join('%s %s' % t for t in _FRIENDS)
						else: _FRIENDS = ', '.join(t[0] for t in _FRIENDS)
					msg = L('Nick: %s\nName: %s\nCountry: %s\nCreated: %s\nLast logoff: %s\nTotal friends: %s\nFriends: %s\nProfile: %s','%s/%s'%(jid,nick)) %\
						(_PERSONANAME,_REALNAME,_LOCCOUNTRYCODE,time_str(_TIMECREATED),time_str(_LASTLOGOFF),_LEN_FRIENDS,_FRIENDS,_PROFILEURL)
					if need_id and type == 'groupchat':
						send_msg(type, jid, nick, L('Send for you in private','%s/%s'%(jid,nick)))
						type = 'chat'
				else: msg = L('Steam user not found!','%s/%s'%(jid,nick))
			except: msg = L('Steam API is broken!','%s/%s'%(jid,nick))
		else: msg = L('Steam API key is wrong!','%s/%s'%(jid,nick))
	else: msg = L('Steam ID should be digital!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'steam', steam, 2, 'Show information about Steam profile')]

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

bmn_last_res = {}

def dec(data):
	b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
	enc = ''
	for i in range(0, len(data)/4):
		h1 = b64.index(data[4*i])
		h2 = b64.index(data[4*i+1])
		h3 = b64.index(data[4*i+2])
		h4 = b64.index(data[4*i+3])
		bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
		o1 = bits >> 16 & 255
		o2 = bits >> 8 & 255
		o3 = bits & 255
		if h3 == 64: enc += chr(o1)
		elif h4 == 64: enc += chr(o1) + chr(o2)
		else: enc += chr(o1) + chr(o2) + chr(o3)
	return enc

def d(strInput, key):
	strInput = dec(strInput)
	strOutput = ''
	intOffset = (key + 112) / 12
	for i in range(4, len(strInput)):
		thisCharCode = ord(strInput[i])
		newCharCode = thisCharCode - intOffset
		strOutput += chr(newCharCode)
	return strOutput

def decrypt(i, key):
	i = list(i)
	return map(lambda x: d(x, key), i[:3]) + i[-2:]

def bugmenot(type, jid, nick,text):
	global bmn_last_res
	result = ''
	text = text.strip()
	if text:
		connct = httplib.HTTPConnection('www.bugmenot.com')
		connct.request('GET', '/view/' + text.encode("utf-8"))
		r = connct.getresponse().read()
		try: key = int(re.findall('var key = (\d+)',r)[0])
		except: key = ''
		blocked = '<h2>Site Blocked</h2>' in r
		if key and not blocked:
			l = re.findall('<tr><th>Username </th><td><script>d\(\'(.+)\'\);</script></td></tr>\s+?<tr><th>Password </th><td><script>d\(\'(.+?)\'\);</script></td></tr>\s+?<tr><th>Other</th><td><script>d\(\'(.+?)\'\);</script></td></tr>\s+?<tr><th>Stats</th><td class="stats"><em class=".+?">(\d+?)% success rate</em> \((\d+?) votes\)</td></tr>', r)
			l = [decrypt(i, key) for i in l]
			logins = [i[0] for i in l]
			passwords = [i[1] for i in l]
			other = [i[2] for i in l]
			stats = [L('%s%% (%s votes)','%s/%s'%(jid,nick)) % (i[3],i[4]) for i in l]
			data = zip(logins, passwords, other, stats)
			if data:
				first = data[0]
				if bmn_last_res.has_key(jid): bmn_last_res[jid].update({nick: data[1:]})
				else: bmn_last_res[jid] = {nick: data[1:]}
			else: result = L('What?','%s/%s'%(jid,nick))
		elif blocked: result = L('Site Blocked','%s/%s'%(jid,nick))
		else: result = L('What?','%s/%s'%(jid,nick))
	else:
		if bmn_last_res.has_key(jid) and bmn_last_res[jid].has_key(nick) and bmn_last_res[jid][nick]:
			first = bmn_last_res[jid][nick][0]
			bmn_last_res[jid][nick] = bmn_last_res[jid][nick][1:]
		else: result = L('No results!','%s/%s'%(jid,nick))
	if not result: result = rss_replace(L('Login: %s, Pass: %s - %s %s','%s/%s'%(jid,nick)) % first)
	send_msg(type, jid, nick, result)

def bmn_clear(room,jid,nick,type,arr):
	if type == 'unavailable' and bmn_last_res.has_key(room) and bmn_last_res[room].has_key(nick): del bmn_last_res[room][nick]

global execute, presence_control

presence_control = [bmn_clear]

execute = [(3, 'bugmenot', bugmenot, 2, 'Search in bugmenot.com')]


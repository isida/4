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

def geoip(type, jid, nick, text):
	text = text.lower().strip()
	is_ip = None
	if text.count('.') == 3:
		is_ip = True
		for ii in text:
			if not nmbrs.count(ii):
				is_ip = None
				break
	if is_ip: IP = text
	else:
		try: IP = socket.gethostbyname_ex(text.encode('idna'))[2][0]
		except: IP = None
	if IP:
		DEC_IP = sum([int(t[1])*256**t[0] for t in enumerate(IP.split('.')[::-1],0)])
		INFO = cur_execute_fetchone('select country,region,city,postalCode,latitude,longitude,metroCode,areaCode from geoip_location where locid=(select locId from geoip_blocks where startIpNum<=%s and endIpNum>=%s limit 1);',(DEC_IP,DEC_IP))
		if INFO: msg = L('IP: %s\nAddress: %s, %s, %s, %s\nLat/lon: %s/%s | Metro/Area: %s/%s','%s/%s'%(jid,nick)) % tuple([t,'?'][t == ''] for t in tuple((IP,) + INFO))
		else: msg = L('GEO info not found!','%s/%s'%(jid,nick))
	else: msg = L('I can\'t resolve it','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

if base_type in ['pgsql','sqlite3']: execute = [(4, 'geo', geoip, 2, 'GEOIP information about IP or domain')]

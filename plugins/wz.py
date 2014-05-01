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

def check_wz(text):
	if not len(text): return True
	for tm in text:
		if ord(tm)<33 or ord(tm)>127: return True
	return None

def get_weather(text):
	wzc = cur_execute_fetchall('select code from wz where code ilike %s or city ilike %s or counry ilike %s',(text,text,text))
	if not wzc: return 'Not Found'
	if len(wzc) != 1: return 'Not Found'
	return load_page('http://weather.noaa.gov/pub/data/observations/metar/decoded/%s.TXT' % wzc[0][0].upper())

def weather(type, jid, nick, text):
	if check_wz(text): msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	else:
		wzz = get_weather(text)
		if 'Not Found' in wzz: msg = L('City not found!','%s/%s'%(jid,nick))
		elif len(wzz.split('\n')) < 9: msg = L('Unexpected error','%s/%s'%(jid,nick))
		else:
			wzz = wzz.split('\n')
			wzr = []
			wzr.append(wzz[0])			# 0
			wzr.append(wzz[1])			# 1
			wzr.append(sfind(wzz,'Temperature'))	# 2
			wzr.append(sfind(wzz,'Wind'))		# 3
			wzr.append(sfind(wzz,'Relative'))	# 4
			wzr.append(sfind(wzz,'Sky'))		# 5
			wzr.append(sfind(wzz,'Weather'))	# 6
			wzr.append(sfind(wzz,'Visibility'))	# 7
			wzr.append(sfind(wzz,'Pressure'))	# 8
			if ')' in wzr[0]: msg = wzr[0][:wzr[0].find(')')+1]
			else: msg = wzr[0]
			msg += '\n'+ wzr[1]
			wzz1 = wzr[2].find(':')+1 # Temperature
			wzz2 = wzr[2].find('(',wzz1)
			wzz3 = wzr[2].find(')',wzz2)
			msg += '\n'+ wzr[2][:wzz1] + ' ' + wzr[2][wzz2+1:wzz3]
			wzz1 = wzr[3].find('(')
			wzz2 = wzr[3].find(')',wzz1)
			wzz3 = wzr[3].find(':',wzz2)
			msg += '\n'+ wzr[3][:wzz1-1] + wzr[3][wzz2+1:wzz3]
			msg += '\n'+ wzr[4]
			if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
			if len(wzr[6]): msg += ','+ wzr[6][wzr[6].find(':')+1:]
			if not (len(wzr[5])+len(wzr[6])): msg += ', clear'
			msg += '\n'+ wzr[7][:-2]
			wzz1 = wzr[8].find('(')
			wzz2 = wzr[8].find(':',wzz1)
			wzz3 = wzr[8].find('(',wzz2)
			msg += ', '+ wzr[8][:wzz1-1]+': '+wzr[8][wzz3+1:-1]
	send_msg(type, jid, nick, msg)

def weather_short(type, jid, nick, text):
	if check_wz(text): msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	else:
		wzz = get_weather(text)
		if 'Not Found' in wzz: msg = L('City not found!','%s/%s'%(jid,nick))
		elif len(wzz.split('\n')) < 9: msg = L('Unexpected error','%s/%s'%(jid,nick))
		else:
			wzz = wzz.split('\n')
			wzr = []
			wzr.append(wzz[0])			# 0
			wzr.append(sfind(wzz,'Temperature'))	# 2
			wzr.append(sfind(wzz,'Wind'))		# 3
			wzr.append(sfind(wzz,'Relative'))	# 4
			wzr.append(sfind(wzz,'Sky'))		# 5
			wzr.append(sfind(wzz,'Weather'))	# 6
			if ')' in wzr[0]: msg = wzr[0][:wzr[0].find(')')+1]
			else: msg = wzr[0]
			wzz1 = wzr[1].find(':')+1 # Temperature
			wzz2 = wzr[1].find('(',wzz1)
			wzz3 = wzr[1].find(')',wzz2)
			msg += ' | '+ wzr[1][:wzz1] + ' ' + wzr[1][wzz2+1:wzz3]
			wzz1 = wzr[2].find('(')
			wzz2 = wzr[2].find(')',wzz1)
			wzz3 = wzr[2].find(':',wzz2)
			msg += ' | '+ wzr[2][:wzz1-1] + wzr[2][wzz2+1:wzz3]
			msg += ' | '+ wzr[3]
			if len(wzr[4]): msg += ','+ wzr[4][wzr[4].find(':')+1:]
			if len(wzr[5]): msg += ','+ wzr[5][wzr[5].find(':')+1:]
			if not (len(wzr[4])+len(wzr[5])): msg += ', clear'
	send_msg(type, jid, nick, msg)

def weather_raw(type, jid, nick, text):
	if check_wz(text): msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	else:
		msg = get_weather(text)[:-1]
		if 'Not Found' in msg: msg = L('City not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def weather_search(type, jid, nick, text):
	if len(text):
		wzc = cur_execute_fetchall('select code,city,counry from wz where code ilike %s or city ilike %s or counry ilike %s',(text,text,text))
		if not wzc: msg = msg = L('City not found!','%s/%s'%(jid,nick))
		else:
			msg = ''
			for tmp in wzc: msg += '\n%s - %s (%s)' % tmp
			msg = L('Found: %s','%s/%s'%(jid,nick)) % msg
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'wzz', weather_raw, 2, 'Weather by airport code. Full version.'),
	 (3, 'wzs', weather_short, 2, 'Weather by airport code. Short version.'),
	 (3, 'wz', weather, 2, 'Weather by airport code. Optimized version.'),
	 (3, 'wzsearch', weather_search, 2, 'Search weather by code, city, country.')]

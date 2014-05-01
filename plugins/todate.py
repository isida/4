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

def get_holiday(sdate):

	''' Function get holiday from file plugins/date.txt and return title of
	holiday if holiday found, else return empty unicode message. Input params
	must be	list of int

	:[month, day]:'''

	result = ''
	date_base = readfile(date_file).decode('UTF').split('\n')
	for ddate in date_base:
		if ddate != '\n' or ddate != '':
			ddate = ddate.split('-')
			hdate = ddate[0]
			if '.' in hdate:
				hdate = map(int, hdate.split('.'))
				hdate.reverse()
				if hdate == sdate:
					result += ddate[1].strip() + ', '
	if len(result) > 2: result = result[:-2]
	return result

def parse_date_string(string_date, spl='.'):

	''' Parse date string and return list [year, month, day] '''

	date_formats = ['%d'+spl+'%m', '%d'+spl+'%m'+spl+'%y',
		'%d'+spl+'%m'+spl+'%Y', '%Y'+spl+'%m'+spl+'%d']
	#output = list(time.localtime())[:3]
	for format in date_formats:
		try: output = list(time.strptime(string_date, format))[:3]
		except: pass
	return output

def to_date(type, jid, nick, text):
	dmass = (L('days','%s/%s'%(jid,nick)), L('day','%s/%s'%(jid,nick)), L('Days','%s/%s'%(jid,nick)).lower(), L('Days','%s/%s'%(jid,nick)).lower(),
		L('Days','%s/%s'%(jid,nick)).lower(), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)))
	splitters = ('.', '-', ':', '/', ',', '\\')
	if len(text):
		try:
			spl = [spl for spl in splitters if spl in text][0]
			sdate = parse_date_string(text, spl)
			if sdate[0] == 1900: sdate[0] = list(time.localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			hday = get_holiday(sdate)
			text = text.replace(spl, '.')
			msg = ''
			if len(hday) > 0: text = hday
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),
					L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),
					L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)))
			if days_remain < 0: msg += L('was %s %s ago','%s/%s'%(jid,nick)) % \
				(str(abs(days_remain)), dmass[int(str(days_remain)[-1])])
			elif  days_remain == 0: msg += L('today','%s/%s'%(jid,nick))
			else: msg += L('will be in %s %s','%s/%s'%(jid,nick)) % \
				(str(abs(days_remain)), dmass[int(str(days_remain)[-1])])
			msg = text + ' ' + msg
		except: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def todate(type, jid, nick, text):
	dmass = (L('days','%s/%s'%(jid,nick)), L('day','%s/%s'%(jid,nick)), L('Days','%s/%s'%(jid,nick)).lower(), L('Days','%s/%s'%(jid,nick)).lower(),
		L('Days','%s/%s'%(jid,nick)).lower(), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)), L('days','%s/%s'%(jid,nick)))
	splitters = ('.', '-', ':', '/', ',', '\\')
	msg = ''
	if len(text):
		try:
			if ' ' in text: ddate, msg = text.split(' ', 1)[0], text.split(' ', 1)[1]
			else: ddate = text
			spl = [spl for spl in splitters if spl in ddate][0]
			if len(msg) == 0: msg = L('before the %s remained','%s/%s'%(jid,nick)) % ddate.replace(spl, '.')
			sdate = parse_date_string(ddate, spl)
			if sdate[0] == 1900: sdate[0] = list(time.localtime())[0]
			year = sdate.pop(0)
			month, day = sdate
			days_remain = (datetime.date(year, month, day) - datetime.date.today()).days
			if len(str(abs(days_remain))) > 1 and str(days_remain)[-2] == '1':
				dmass = (L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),
					L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)),
					L('days','%s/%s'%(jid,nick)),L('days','%s/%s'%(jid,nick)))
			if days_remain < 0: msg = L('Date has already in past!','%s/%s'%(jid,nick))
			else: msg += ' %s %s' % (days_remain,dmass[int(str(days_remain)[-1])])
		except: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'to_date', to_date, 2, 'Calculate count of days for requested date, if the date is holiday, that returned title of holiday.\nSupported date formats: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nSupported splitters: ,-.:/\\\ntodate 05.09\ntodate 5/9/2010'),
	(3, 'todate', todate, 2, 'Calculate count of days for requested date.\nSupported date formats: dd.mm.yyyy, dd.mm, dd.mm.yy, yyyy.mm.dd\nSupported splitter: ,-.:/\\\ntodate 05.09 before New year remained\ntodate 5/9/2010 before New year remained')]

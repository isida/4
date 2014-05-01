#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) dr.Schmurge <dr.schmurge@isida-bot.com>                    #
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

def month_cal(type, jid, nick, text):
	text = text.split()
	try: month = int(text[0])
	except: month = tuple(time.localtime())[1]
	try: year = int(text[1])
	except: year = tuple(time.localtime())[0]
	try: smbl = text[2]
	except: smbl = GT('calendar_default_splitter')
	try:
		msg = L('\nMon Tue Wed Thu Fri Sat Sun\n','%s/%s'%(jid,nick)) + '\n'.join([' '.join([['%2d' % r,'  '][r==0] for r in t]) for t in calendar.monthcalendar(year,month)])
		msg = L('Now: %s%s','%s/%s'%(jid,nick)) % (timeadd(tuple(time.localtime())), msg.replace(' ',smbl))
	except: msg = L('Error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'calendar', month_cal, 2, 'Calendar. Without parameters show calendar for current month.\ncalendar [month][year][symbol_splitter]')]

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

def gtalkers(type, jid, nick, text):
	if text:
		ttext = '%%%s%%' % text
		tma = cur_execute_fetchall('select * from talkers where (jid ilike %s or nick ilike %s or room ilike %s) order by -words limit %s',(ttext,ttext,ttext,10))
	else: tma = cur_execute_fetchall('select * from talkers order by -words limit %s',(10,))
	if tma:
		msg = '%s\n' % L('Talkers:\nNick\t\tWords\tPhrases\tEffect\tConf.','%s/%s'%(jid,nick))
		msg += '\n'.join(['%s. %s\t\t%s\t%s\t%s\t%s' % (cnd + 1, tt[2], tt[3], tt[4], round(tt[3]/float(tt[4]), 2),'%s@%s.%s' % (getName(tt[0]),'.'.join([tmp[0] for tmp in tt[0].split('@')[1].split('.')[:-1]]),tt[0].split('.')[-1])) for cnd, tt in enumerate(tma)])
	else: msg = '%s %s' % (text, L('Not found!','%s/%s'%(jid,nick)))
	send_msg(type, jid, nick, msg)

def talkers(type, jid, nick, text):
	if text:
		ttext = '%%%s%%' % text
		tma = cur_execute_fetchall('select * from talkers where room=%s and (jid ilike %s or nick ilike %s) order by -words limit %s',(jid,ttext,ttext,10))
	else: tma = cur_execute_fetchall('select * from talkers where room=%s order by -words limit %s',(jid,10))
	if tma:
		msg = '%s\n' % L('Talkers:\nNick\t\tWords\tPhrases\tEffect','%s/%s'%(jid,nick))
		msg += '\n'.join(['%s. %s\t\t%s\t%s\t%s' % (cnd + 1, tt[2], tt[3], tt[4], round(tt[3]/float(tt[4]), 2)) for cnd, tt in enumerate(tma)])
	else: msg = '%s %s' % (text, L('Not found!','%s/%s'%(jid,nick)))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'talkers', talkers, 2, 'Show local talkers'),
	   (4, 'gtalkers', gtalkers, 2, 'Show global talkers')]
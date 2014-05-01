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

JIDCATCHER_DEFAULT_LIMIT = 10

def info_search(type, jid, nick, text):
	msg = L('What I must find?','%s/%s'%(jid,nick))
	if text:
		if '\n' in text:
			text,lim = text.split('\n',1)
			try:
				lim = int(lim)
				if lim < 100 or lim > 1: raise
			except: lim = JIDCATCHER_DEFAULT_LIMIT
		else: lim = JIDCATCHER_DEFAULT_LIMIT
		cur_execute('delete from jid where server ilike %s',('<temporary>%',))
		ttext = '%%%s%%' % text
		tma = cur_execute_fetchall('select * from jid where login ilike %s or server ilike %s or resourse ilike %s order by login limit %s',(ttext,ttext,ttext,lim))
		if tma: msg = '%s\n%s' % (L('Found:','%s/%s'%(jid,nick)),'\n'.join(['%s. %s@%s/%s' % tuple([tma.index(tt)+1]+list(tt)) for tt in tma]))
		else: msg = L('\'%s\' not found!','%s/%s'%(jid,nick)) % text
	send_msg(type, jid, nick, msg)

def info_res(type, jid, nick, text):
	cur_execute('delete from jid where server ilike %s',('<temporary>%',))
	if text.lower() == 'count':
		tlen = cur_execute_fetchall('select count(*) from (select resourse,count(*) from jid group by resourse) tmp;')[0][0]
		text,jidbase = '',''
	else:
		text1 = '%%%s%%' % text
		tlen = cur_execute_fetchall('select count(*) from (select resourse,count(*) from jid where resourse ilike %s group by resourse) tmp;',(text1,))[0][0]
		jidbase = cur_execute_fetchall('select resourse,count(*) from jid where resourse ilike %s group by resourse order by -count(*),resourse limit %s',(text1,JIDCATCHER_DEFAULT_LIMIT))
	if not tlen: msg = L('\'%s\' not found!','%s/%s'%(jid,nick)) % text
	else:
		if text: msg = L('Found resources: %s','%s/%s'%(jid,nick)) % tlen
		else: msg = L('Total resources: %s','%s/%s'%(jid,nick)) % tlen
		if jidbase: msg += '\n%s' % '\n'.join(['%s. %s\t%s' % tuple([jidbase.index(jj)+1]+list(jj)) for jj in jidbase])
	send_msg(type, jid, nick, msg)

def info_serv(type, jid, nick, text):
	cur_execute('delete from jid where server ilike %s',('<temporary>%',))

	if '\n' in text:
		text,lim = text.split('\n',1)
		try:
			lim = int(lim)
			if lim > 100 or lim < 1: raise
		except: lim = JIDCATCHER_DEFAULT_LIMIT
	else: lim = JIDCATCHER_DEFAULT_LIMIT
	
	if text == 'count':
		tlen = cur_execute_fetchone('select count(*) from (select server,count(*) from jid group by server) tmp;')[0]
		text,jidbase = '',''
	else:
		text1 = '%%%s%%' % text
		if base_type == 'pgsql': reqv = 'select * from (select row_number() over(order by -count(*)),server,count(*) from jid group by server order by -count(*),server) tmp where tmp.server ilike %s order by tmp.row_number;'
		elif base_type == 'mysql': reqv = 'select * from (select @i:=@i+1 as itr,sr,cn from (select server as sr,count(*) as cn from jid group by server order by -count(*)) as t1,(select @i:=0) as t2) as t3 where sr like %s'
		elif base_type == 'sqlite3':
			# TODO: It's works not properly. Need fix record's numbers!
			reqv = 'select row_number(),sr,cn from (select server as sr,count(*) as cn from jid group by server order by -cn) where sr like %s order by -cn'
		jidbase = cur_execute_fetchall(reqv,(text1,))
		tlen = len(jidbase)
		jidbase = jidbase[:lim]
	if not tlen: msg = L('\'%s\' not found!','%s/%s'%(jid,nick)) % text
	else:
		if text: msg = L('Found servers: %s','%s/%s'%(jid,nick)) % tlen
		else: msg = L('Total servers: %s','%s/%s'%(jid,nick)) % tlen
		if jidbase: msg = '%s\n%s' %(msg,'\n'.join(['%s. %s [%s]' % (int(jj[0]),jj[1],jj[2]) for jj in jidbase]))
	send_msg(type, jid, nick, msg)

#room number date

def info_top(type, jid, nick, text):
	if text: room = text
	else: room = getRoom(jid)
	cnf = cur_execute_fetchone('select count ,time from top where room=%s',(room,))
	if cnf: msg = L('Max count of members: %s %s','%s/%s'%(jid,nick)) % (cnf[0], '(%s)' % disp_time(cnf[1],'%s/%s'%(jid,nick)))
	else: msg = L('Statistic not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def jidcatcher_presence(room,jid,nick,type,text):
	if jid != 'None' and not jid.startswith('<temporary>'):
		tmp = (getName(jid),getServer(jid),getResourse(jid))
		try:
			tmpp = cur_execute_fetchone('select login from jid where login=%s and server=%s and resourse=%s',tmp)
			if not tmpp: cur_execute('insert into jid values (%s,%s,%s)', tmp)
		except: pass

		cnt = len(['' for t in megabase if t[0]==room])
		cnf = cur_execute_fetchone('select count from top where room=%s',(room,))
		if cnf:
			if cnt > cnf[0]: cur_execute('update top set count =%s, time=%s where room=%s;',(cnt,int(time.time()),room))
		else: cur_execute('insert into top values (%s,%s,%s);',(room,cnt,int(time.time())))

global execute, presence_control

presence_control = [jidcatcher_presence]

execute = [(4, 'res', info_res, 2, 'Without parameters show top10 resources for all conferences, where bot is present.\nwith parameters - search in resources base\ncount - number of results.'),
		   (6, 'serv', info_serv, 2, 'Wihtout parameters show all servers freom where joined in rooms, where bot is present\nwith parameters - search on servers base\ncount - show number of results.'),
		   (9, 'search', info_search, 2, 'Search in internal jids base.'),
		   (2, 'top', info_top, 2, 'Conference\'s activity.')]

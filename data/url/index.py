#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    List of URL                                                              #
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
#    along with this program.  If nоt, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

import time,cgi,urllib2

def cur_execute_fetchall_sqlite3(*params):
	conn = sqlite3.connect(sqlite_base)
	if 'split_part' in list(params)[0]: conn.create_function('split_part', 3, sqlite3_split_part)
	if 'row_number' in list(params)[0]:
		global sqlite3_row_number_last_x
		sqlite3_row_number_last_x = 0
		conn.create_function('row_number', 0, sqlite3_row_number)
	try: cur = conn.cursor()
	except: return None
	par = None
	try:
		params = list(params)
		params[0] = params[0].replace('%s','?').replace(' ilike ',' like ').replace(' update ',' `update` ').replace(' repeat ',' `repeat` ').replace(' option ',' `option` ').replace(' count ',' `count` ').replace(' match ',' `match` ')
		params = tuple(params)
		cur.execute(*params)
		try: par = cur.fetchall()
		except Exception, par:
			par = None
			if halt_on_exception: raise
	except Exception, par:
		par = None
		conn.rollback()
		if halt_on_exception: raise
	conn.close()
	return par

def cur_execute_fetchall_mysql(*params):
	conn = mysqldb.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
	try: cur = conn.cursor()
	except: return None
	par = None
	try:
		params = list(params)
		params[0] = params[0].replace(' ilike ',' like ').replace(' update ',' `update` ').replace(' repeat ',' `repeat` ').replace(' option ',' `option` ').replace(' count ',' `count` ').replace(' match ',' `match` ').replace('split_part(','substring_index(')
		params = tuple(params)
		cur.execute(*params)
		try: par = cur.fetchall()
		except Exception, par:
			par = None
			if halt_on_exception: raise
	except Exception, par:
		par = None
		conn.rollback()
		if halt_on_exception: raise
	conn.close()
	return par

def cur_execute_fetchall(*params):
	if base_type == 'sqlite3': return cur_execute_fetchall_sqlite3(*params)
	elif base_type == 'mysql': return cur_execute_fetchall_mysql(*params)
	global conn
	try: cur = conn.cursor()
	except: return None
	if base_type == 'pgsql': psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = None
	try:
		cur.execute(*params)
		try: par = cur.fetchall()
		except Exception, par:
			if database_debug:
				try: par = str(par)
				except: par = unicode(par)
			else: par = None
			if halt_on_exception: raise
	except Exception, par:
		if database_debug:
			try: par = str(par)
			except: par = unicode(par)
			pprint(par,'red')
		else: par = None
		conn.rollback()
		if halt_on_exception: raise
	cur.close()
	return par
	
html_head = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href=".css/isida.css" rel="stylesheet" type="text/css" />
<link rel="shortcut icon" href="/icon.ico">
<title>List of URL</title></head>
<body>
<div class="title">%s</div>

<div class="main">
'''
html_end = '''
</div><br>
%s</body></html>
'''

max_link_size = 64
url_count_limit = 100
database_debug = False
halt_on_exception = False
execfile('config.py')

if base_type == 'pgsql':
	import psycopg2
	import psycopg2.extensions
	conn = psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
elif base_type == 'mysql':
	import mysql.connector as mysqldb
elif base_type == 'sqlite3':
	import sqlite3

if base_type in ['mysql','sqlite3']:
	class psycopg2():
		def InterfaceError(): return None

form = cgi.FieldStorage()

try: room = form.getvalue('room').decode('utf8')
except: room = ' '
roomz = [t[0] for t in cur_execute_fetchall('select room from url group by room order by room;')]
roomz = [' '] + roomz
if not roomz: print 'Error! Stored URL not found!'
if not room or room not in roomz: room = roomz[0]

try: nick = form.getvalue('nick').decode('utf8')
except: nick = ' '
nickz = [t[0] for t in cur_execute_fetchall('select nick from url group by nick order by nick;')]
nickz = [' '] + nickz
if not nickz: print 'Error! Stored URL not found!'
if not nick or nick not in nickz: nick = nickz[0]


try: min_date = cur_execute_fetchall('select time from url order by time limit 1;')[0][0]
except: min_date = int(time.time())
try: now_date = cur_execute_fetchall('select time from url order by -time limit 1;')[0][0]
except: now_date = int(time.time())

min_date = '%04d-%02d-%02d' % time.localtime(min_date)[:3]
max_date = '%04d-%02d-%02d' % time.localtime(now_date)[:3]
try:
	sel_date = form.getvalue('calendar')
	if not sel_date: raise
	now_date = sel_date
except:
	sel_date = ''
	now_date = ''#max_date

drop_list = '''<form action="/url/" method=post>
Choice room/nick
<select name="room">
%s</select>
<select name="nick">
%s</select>
<input type=submit value="&nbsp;Apply&nbsp;">
and/or Choice date
<input type="date" name="calendar" value="%s" max="%s" min="%s">
<input type="submit" value="&nbsp;Apply&nbsp;">
</form>'''

drop_opt = '<option value="%s">%s\n'

dopt_r = drop_opt % (room,room) + ''.join([drop_opt % (t,t) for t in roomz if t != room])
dopt_n = drop_opt % (nick,nick) + ''.join([drop_opt % (t,t) for t in nickz if t != nick])

print html_head % (drop_list % (dopt_r.encode('utf8'),dopt_n.encode('utf8'),now_date,max_date,min_date),)

if sel_date: date_from, date_to = sel_date, sel_date
else: date_from, date_to = min_date, max_date

date_from = int(time.mktime([int(t) for t in date_from.split('-')]+[0,0,0,0,0,0]))
date_to = int(time.mktime([int(t) for t in date_to.split('-')]+[23,59,59,0,0,0]))

if room != ' ':
	if nick != ' ':
		url_count = cur_execute_fetchall('select count(*) from url where room=%s and time>%s and time<%s;',(room,date_from,date_to))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where room=%s and nick=%s and time>%s and time<%s order by -time limit %s;',(room,nick,date_from,date_to,url_count_limit))
	else:
		url_count = cur_execute_fetchall('select count(*) from url where room=%s and time>%s and time<%s;',(room,date_from,date_to))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where room=%s and time>%s and time<%s order by -time limit %s;',(room,date_from,date_to,url_count_limit))
else:
	if nick != ' ':
		url_count = cur_execute_fetchall('select count(*) from url where time>%s and time<%s;',(date_from,date_to))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where nick=%s and time>%s and time<%s order by -time limit %s;',(nick,date_from,date_to,url_count_limit))
	else:
		url_count = cur_execute_fetchall('select count(*) from url where time>%s and time<%s;',(date_from,date_to))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where time>%s and time<%s order by -time limit %s;',(date_from,date_to,url_count_limit))
if url:
	tm = []
	color = int('ccc',16)
	mask = color ^ int('eee',16)
	for t in url:
		try: ll = urllib2.unquote(t[3].encode('utf8')).decode('utf8')
		except: ll = 'error'
		lnk = ll if len(ll) < max_link_size else '%s...%s' % (ll[:max_link_size-10],ll[-10:])
		if t[4]: text = t[4].strip()
		else: text = '-'
		if len(text) >= max_link_size: text = '%s...' % text[:max_link_size]
		text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
		tmp = '<tr bgcolor="#%s">\n<td align="center">&nbsp;%s&nbsp;</td>\n<td align="center">&nbsp;%s&nbsp;</td>\n<td>&nbsp;<a href="%s" target="_blank">%s</a></td>\n<td>&nbsp;%s</td>\n</tr>\n' % (hex(color)[2:],'%04d.%02d.%02d&nbsp;%02d:%02d:%02d' % time.localtime(t[2])[:6],t[1],t[3],lnk,text)
		tm.append(tmp.encode('utf-8'))
		color = color ^ mask
	print '''
<table border="1" class="urlbody" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="urlheader">
'''
	print '<td><b>%s .. %s of %s</b></td>' % (1,len(url),url_count)
	print '''
</tr>
</table>
'''
	print '''
<table border="1" class="urlbody" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="urltitle">
<td><b>Date</b></td>
<td><b>&nbsp;Nick&nbsp;</b></td>
<td><b>URL</b></td>
<td><b>Title</b></td>
</tr>
	'''
	print ''.join(tm)
	print '</table>'
else: 
	print '''
<table border="1" class="paste" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="paste">
<td>&nbsp;URL not found!</td>
</tr>
</table>
	'''
try: custom_end = cur_execute_fetchall('select value from config_owner where option=%s;',('html_logs_end_text',))[0][0]
except: custom_end = ''
print html_end % custom_end

# The end is near!

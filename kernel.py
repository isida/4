#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida Jabber Bot                                                         #
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

from __future__ import with_statement

import calendar
import crontab
import datetime
import gc
import json
import hashlib
import htmlentitydefs
import httplib
import logging
import operator
import os
import math
import random
import re
import socket
import string
import sys
import time
import urllib
import urllib2

import chardet
import xmpp

global execute, prefix, comms, hashlib, trace

def sqlite3_split_part(txt, spltr, cnt):
	if txt: return (txt.split(spltr) + [''] * (cnt-1))[cnt-1]
	else: return txt

sqlite3_row_number_last_x = 0
def sqlite3_row_number():
	global sqlite3_row_number_last_x
	sqlite3_row_number_last_x += 1
	return sqlite3_row_number_last_x

def cur_execute_sqlite3(*params):
	conn = sqlite3.connect(sqlite_base)	
	if 'split_part' in list(params)[0]: conn.create_function('split_part', 3, sqlite3_split_part)
	if 'row_number' in list(params)[0]:
		global sqlite3_row_number_last_x
		sqlite3_row_number_last_x = 0
		conn.create_function('row_number', 0, sqlite3_row_number)
	cur = conn.cursor()
	par = True
	try:
		params = list(params)
		params[0] = params[0].replace('%s','?').replace(' ilike ',' like ').replace(' update ',' `update` ').replace(' repeat ',' `repeat` ').replace(' option ',' `option` ').replace(' count ',' `count` ').replace(' match ',' `match` ')
		params = tuple(params)
		cur.execute(*params)
		prm = params[0].split()[0].lower()
		if prm in ['update','insert','delete','create','drop','alter']: conn.commit()
	except Exception, par:
		par = None
		conn.rollback()
		if halt_on_exception: raise
	conn.commit()
	conn.close()
	return par
	
def cur_execute_mysql(*params):
	conn = mysqldb.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
	cur = conn.cursor()
	par = True
	try:
		params = list(params)
		params[0] = params[0].replace(' ilike ',' like ').replace(' update ',' `update` ').replace(' repeat ',' `repeat` ').replace(' option ',' `option` ').replace(' count ',' `count` ').replace(' match ',' `match` ').replace('split_part(','substring_index(')
		params = tuple(params)
		cur.execute(*params)
		prm = params[0].split()[0].lower()
		if prm in ['update','insert','delete','create','drop','alter']: conn.commit()
	except Exception, par:
		par = None
		conn.rollback()
		if halt_on_exception: raise
	conn.commit()
	conn.close()
	return par

def cur_execute(*params):
	if base_type == 'sqlite3': return cur_execute_sqlite3(*params)
	elif base_type == 'mysql': return cur_execute_mysql(*params)
	global conn
	cur = conn.cursor()
	if base_type == 'pgsql': psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = True
	try:
		cur.execute(*params)
		prm = params[0].split()[0].lower()
		if prm in ['update','insert','delete','create','drop','alter']: conn.commit()
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

def cur_execute_fetchone_sqlite3(*params):
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
		try: par = cur.fetchone()
		except Exception, par:
			par = None
			if halt_on_exception: raise
	except Exception, par:
		par = None
		conn.rollback()
	conn.close()
	return par

def cur_execute_fetchone_mysql(*params):
	conn = mysqldb.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
	try: cur = conn.cursor()
	except: return None
	par = None
	try:
		params = list(params)
		params[0] = params[0].replace(' ilike ',' like ').replace(' update ',' `update` ').replace(' repeat ',' `repeat` ').replace(' option ',' `option` ').replace(' count ',' `count` ').replace(' match ',' `match` ').replace('split_part(','substring_index(')
		params = tuple(params)
		cur.execute(*params)
		try: par = cur.fetchone()
		except Exception, par:
			par = None
			if halt_on_exception: raise
	except Exception, par:
		par = None
		conn.rollback()
	conn.close()
	return par

def cur_execute_fetchone(*params):
	if base_type == 'sqlite3': return cur_execute_fetchone_sqlite3(*params)
	elif base_type == 'mysql': return cur_execute_fetchone_mysql(*params)
	global conn
	try: cur = conn.cursor()
	except: return None
	if base_type == 'pgsql': psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = None
	try:
		cur.execute(*params)
		try: par = cur.fetchone()
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
			if halt_on_exception: raise
		else: par = None
		conn.rollback()
	cur.close()
	return par

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

def get_color(c):
	color = os.environ.has_key('TERM')
	colors = {'clear':'[0m','blue':'[34m','red':'[31m','magenta':'[35m','green':'[32m','cyan':'[36m','brown':'[33m','light_gray':'[37m','black':'[30m','bright_blue':'[34;1m','bright_red':'[31;1m','purple':'[35;1m','bright_green':'[32;1m','bright_cyan':'[36;1m','yellow':'[33;1m','dark_gray':'[30;1m','white':'[37;1m'}
	return ['','\x1b%s' % colors[c]][color]

def get_color_win32(c):
	colors = {'clear':7,'blue':1,'red':4,'magenta':5,'green':2,'cyan':3,'brown':6,'light_gray':7,'black':0,'bright_blue':9,'bright_red':12,'purple':13,'bright_green':10,'bright_cyan':11,'yellow':14,'dark_gray':8,'white':15}
	return colors[c]

def thr(func,param,name):
	global th_cnt, thread_error_count, sema
	th_cnt += 1
	try:
		if thread_type:
			with sema:
				tmp_th = KThread(group=None,target=log_execute,name='%s_%s' % (th_cnt,name),args=(func,param))
				tmp_th.start()
		else: thread.start_new_thread(log_execute,(func,param))
	except SystemExit: pass
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		if 'thread' in SM.lower(): thread_error_count += 1
		else: logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())),unicode(func)))
		if thread_type:
			try: tmp_th.kill()
			except: pass
		if halt_on_exception: raise

def log_execute(proc, params):
	try: proc(*params)
	except SystemExit: pass
	except: logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())),unicode(proc)))

def sender(item):
	global message_out, presence_out, iq_out, unknown_out, last_stanza, messages_log
	last_stanza = unicode(item)
	if last_stanza[:2] == '<m':
		message_out += 1
		id = get_id()
		item.setAttr('id',id)
		messages_log[id] = item
	elif last_stanza[:2] == '<p': presence_out += 1
	elif last_stanza[:2] == '<i': iq_out += 1
	else: unknown_out += 1
	if time_nolimit: time.sleep(time_nolimit)
	try: cl.send(item)
	except Exception,SM:
		pprint(last_stanza,'red')
		pprint(SM,'red')
		if halt_on_exception: raise

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def getFile(filename,default):
	if os.path.isfile(filename):
		try: filebody = eval(readfile(filename))
		except:
			if os.path.isfile(back_file % filename.split('/')[-1]):
				while True:
					try:
						filebody = eval(readfile(back_file % filename.split('/')[-1]))
						break
					except: pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(back_file % filename.split('/')[-1],str(filebody))
	return filebody

def get_config(room,item):
	setup = cur_execute_fetchone('select value from config_conf where room=%s and option = %s',(room,item))
	try:
		if setup[0] in ['True','true']: return True
		elif setup[0] in ['False','false','None','none']: return False
		else: return setup[0]
	except:
		try: return config_prefs[item][3]
		except: return None

def get_config_int(room,item):
	setup = cur_execute_fetchone('select value from config_conf where room=%s and option = %s',(room,item))
	try: return int(setup[0])
	except: return int(config_prefs[item][3])

def put_config(room,item,value):
	if value in [True,False,None]: value = str(value)
	setup = cur_execute_fetchone('select value from config_conf where room=%s and option = %s',(room,item))
	if setup: cur_execute('update config_conf set value=%s where room=%s and option = %s', (value,room,item))
	else: cur_execute('insert into config_conf values (%s,%s,%s)', (room,item,value))

def GT(item):
	try:
		gt_result = cur_execute_fetchone('select value from config_owner where option = %s;',(item,))[0]
		if gt_result in ['true','false','none']: gt_result = gt_result.capitalize()
	except:
		try: gt_result = owner_prefs[item][2]
		except: gt_result = None
	try: return eval(gt_result)
	except: return gt_result

def PT(item,value):
	if value in [True,False,None] or isinstance(value,type([])): value = str(value)
	setup = cur_execute_fetchone('select value from config_owner where option = %s;',(item,))
	if setup: cur_execute('update config_owner set value=%s where option = %s', (value,item))
	else: cur_execute('insert into config_owner values (%s,%s)', (item,value))

def get_subtag(body,tag):
	T = re.findall('%s=\"(.*?)\"' % tag,body,re.S)
	if T: return T[0]
	else: return ''

def get_tag(body,tag):
	T = re.findall('<%s.*?>(.*?)</%s>' % (tag,tag),body,re.S)
	if T: return T[0]
	else: return ''

def get_tag_full(body,tag):
	T = re.findall('(<%s[^>]*?>|</%s>)' % (tag,tag),body,re.S)
	if T and len(T)==1: return T[0]
	elif len(T) >= 2 and T[0][1:len(tag)+1] == T[1][-len(tag)-1:-1]:
		T1 = re.findall('(%s.*?%s)' % (re.escape(T[0]),re.escape(T[1])),body,re.S)
		if T1: return T1[0]
		else: return ''
	elif len(T): return T[0]
	else: return ''

def get_tag_item(body,tag,item):
	body = get_tag_full(body,tag)
	return get_subtag(body,item)

def parser(t):
	try: return ''.join([['?',l][l<='~'] for l in unicode(t)])
	except:
		fp = file(slog_folder % 'critical_exception_%s.txt' % int(time.time()), 'wb')
		fp.write(t)
		fp.close()

def remove_sub_space(t): return ''.join([['?',l][l>=' ' or l in '\t\r\n'] for l in unicode(t)])

def smart_encode(text,enc):
	tx,splitter = '','|'
	while splitter in text: splitter += '|'
	ttext = text.replace('</','<%s/' % splitter).split(splitter)
	for tmp in ttext:
		try: tx += unicode(tmp,enc)
		except: pass
	return tx

def timeadd(lt): return '%02d.%02d.%02d %02d:%02d:%02d' % (lt[2],lt[1],lt[0],lt[3],lt[4],lt[5])

def onlytimeadd(lt): return '%02d:%02d:%02d' % (lt[3],lt[4],lt[5])

def pprint(*text):
	global last_logs_store
	c,wc,win_color = '','',''
	if len(text) > 1:
		if is_win32: win_color = get_color_win32(text[1])
		else: c,wc = get_color(text[1]),get_color('clear')
	elif is_win32: win_color = get_color_win32('clear')
	text = text[0]
	lt = tuple(time.localtime())
	zz = '%s[%s]%s %s%s' % (wc,onlytimeadd(lt),c,text,wc)
	last_logs_store = ['[%s] %s' % (onlytimeadd(lt),text)] + last_logs_store[:last_logs_size]
	if debug_console:
		if is_win32 and win_color:
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, get_color_win32('clear'))
			print zz.split(' ',1)[0],
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, win_color)
			try: print zz.split(' ',1)[1]
			except: print parser(zz.split(' ',1)[1])
			ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, get_color_win32('clear'))
		else:
			try: print zz
			except: print parser(zz)
	if CommandsLog:
		fname = slog_folder % '%02d%02d%02d.txt' % (lt[0],lt[1],lt[2])
		fbody = '%s|%s\n' % (onlytimeadd(lt),text.replace('\n','\r'))
		fl = open(fname, 'a')
		fl.write(fbody.encode('utf-8'))
		fl.close()

def send_presence_all(sm):
	pr=xmpp.Presence(typ='unavailable')
	pr.setStatus(sm)
	sender(pr)
	time.sleep(2)

def errorHandler(text):
	draw_warning(text)
	sys.exit('exit')

def get_joke(text):

	def joke_blond(text):

		def blond_text(text):
			b = ''
			cnt = random.randint(0,1)
			for tmp in text:
				if cnt: b += tmp.upper()
				else: b += tmp.lower()
				cnt = not cnt
			return b

		text = text.split(' ')
		new_text = []
		for t in text:
			if t == '/me' or [True for s in ['http://','https://','ftp://','svn://','xmpp:','git://'] if t.startswith(s)]: new_text.append(t)
			else: new_text.append(blond_text(t))
		return ' '.join(new_text)

	def joke_upyachka(text):
		upch = [u'пыщь!!!111адын',u'ололололо!!11',u'ГОЛАКТЕКО ОПАСНОСТЕ!!11',u'ТЕЛОИД!!',u'ЖАЖА1!',u'ОНОТОЛЕЙ!!!!!',u'ПОТС ЗОХВАЧЕН11!!!',
				u'ПыЩЩЩЩЩЩЩЩЩь!!!!!!!1111',u'ПыЩЩЩЩЩЩЩЩЩь11111адинадин1адин']
		return '%s %s' % (text.strip(),random.choice(upch))

	def no_joke(text): return text

	jokes = [joke_blond,no_joke,joke_upyachka]
	return random.choice(jokes)(text)

def msg_validator(t): return ''.join([[l,'?'][l<' ' and l not in '\n\t\r' or l>u'\uff00'] for l in unicode(t)])

def message_exclude_update():
	global messages_excl
	excl = GT('exclude_messages').replace('\r','').replace('\t','').split('\n')
	messages_excl = []
	for c in excl:
		if '#' not in c and len(c): messages_excl.append(c)

def message_validate(item):
	if messages_excl:
		for c in messages_excl:
			cn = re.findall(c,' %s ' % item,re.S|re.I|re.U)
			for tmp in cn: item = item.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
	return item

def send_msg(mtype, mjid, mnick, mmessage):
	global between_msg_last,time_limit
	if mmessage:
		mmessage = message_validate(mmessage)
		mnick = message_validate(mnick)
		# 1st april joke :)
		if time.localtime()[1:3] == (4,1) and GT('1st_april_joke'): mmessage = get_joke(mmessage)
		no_send = True
		if len(mmessage) > msg_limit:
			cnt = 0
			maxcnt = int(len(mmessage)/msg_limit) + 1
			mmsg = mmessage
			while len(mmsg) > msg_limit and not game_over:
				tmsg = u'[%s/%s] %s[…]' % (cnt+1,maxcnt,mmsg[:msg_limit])
				cnt += 1
				sender(xmpp.Message('%s/%s' % (mjid,mnick), tmsg, 'chat'))
				mmsg = mmsg[msg_limit:]
				time.sleep(time_limit)
			tmsg = '[%s/%s] %s' % (cnt+1,maxcnt,mmsg)
			sender(xmpp.Message('%s/%s' % (mjid,mnick), tmsg, 'chat'))
			if mtype == 'chat': no_send = None
			else: mmessage = mmessage[:msg_limit] + u'[…]'
		if no_send:
			if mtype == 'groupchat' and mnick != '': mmessage = '%s: %s' % (mnick,mmessage)
			else: mjid += '/' + mnick
			while mmessage[-1:] in ['\n','\t','\r',' ']: mmessage = mmessage[:-1]
			mmessage = msg_validator(mmessage)
			if len(mmessage): sender(xmpp.Message(mjid, mmessage, mtype))

def os_version_disco():
	iSys = sys.platform
	iOs = os.name
	isidaPyVer = sys.version.split()[0]
	if iOs == 'posix':
		osInfo = os.uname()
		isidaOs = osInfo[0]
		isidaOsVer = '%s-%s/PYv%s' % (osInfo[2].split('-',1)[0],osInfo[4],isidaPyVer)
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key): return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = get("ProductName")
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			isidaOs = osInfo
			isidaOsVer = 'SP:%s/BLD:%s/PYv%s' % (spInfo,buildInfo,isidaPyVer)
		except:
			isidaOs = 'Windows'
			isidaOsVer = '%s/BLD:%s/PYv%s' % (osInfo.replace('Windows','').strip(),buildInfo,isidaPyVer)
	else: isidaOs = isidaOsVer = 'unknown'
	return isidaOs, isidaOsVer

def os_version():
	iSys = sys.platform
	iOs = os.name
	isidaPyVer = '%s [%s]' % (sys.version.split(' (')[0],sys.version.split(')')[0].split(', ')[1])
	if iOs == 'posix':
		osInfo = os.uname()
		isidaOs = '%s %s-%s / Python %s' % (osInfo[0],osInfo[2],osInfo[4],isidaPyVer)
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key): return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = ' '.join(get("ProductName").split()[:3])
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			isidaOs = '%s %s [%s] / Python %s' % (osInfo,spInfo,buildInfo,isidaPyVer)
		except: isidaOs = '%s [%s] / Python %s' % (osInfo,buildInfo,isidaPyVer)
	else: isidaOs = 'unknown'
	return isidaOs

def caps_and_send(tmp):
	tmp.setTag('x', namespace=xmpp.NS_VCARD_UPDATE)
	tmp.getTag('x', namespace=xmpp.NS_VCARD_UPDATE).setTagData('photo',photo_hash)
	tmp.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':capsNode,'ver':capsHash,'hash':'md5'})
	sender(tmp)

def join(conference,passwd):
	global pres_answer,cycles_used,cycles_unused,current_join
	id = get_id()
	current_join[conference] = id
	if Settings['status'] == 'online': j = xmpp.Node('presence', {'id': id, 'to': conference}, payload = [xmpp.Node('status', {},[Settings['message']]),\
																										  xmpp.Node('priority', {},[Settings['priority']])])
	else: j = xmpp.Node('presence', {'id': id, 'to': conference}, payload = [xmpp.Node('show', {},[Settings['status']]),\
																		xmpp.Node('status', {},[Settings['message']]),\
																		xmpp.Node('priority', {},[Settings['priority']])])
	j.setTag('x', namespace=xmpp.NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
	j.getTag('x').setTagData('password', passwd)
	caps_and_send(j)
	answered, Error, join_timeout = None, None, 3
	if is_start: join_timeout_delay = 0.3
	else: join_timeout_delay = 1
	while not answered and join_timeout >= 0 and not game_over:
		if is_start:
			cyc = cl.Process(1)
			if str(cyc) == 'None': cycles_unused += 1
			elif int(str(cyc)): cycles_used += 1
			else: cycles_unused += 1
		else: time.sleep(join_timeout_delay)
		join_timeout -= join_timeout_delay
		for tmp in pres_answer:
			if tmp[0]==id:
				Error = tmp[1]
				pres_answer.remove(tmp)
				answered = True
				break
		if current_join.has_key(conference) and current_join[conference] != id: break
	if current_join.has_key(conference):
		if current_join[conference] != id: Error = {'CAPTCHA':current_join[conference],'ID':id}
		current_join.pop(conference)
	return Error

def leave(conference, sm):
	j = xmpp.Presence(conference, 'unavailable', status=sm)
	sender(j)

def muc_filter_action(act,jid,room,reason):
	if act in ['visitor','kick']:
		nick = get_nick_by_jid(room,getRoom(jid))
		if nick and act=='visitor': sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':'visitor', 'nick':nick},[xmpp.Node('reason',{},reason)])])]))
		elif nick and act=='kick': sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':'none', 'nick':nick},[xmpp.Node('reason',{},reason)])])]))
		elif not nick and act=='visitor': sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':'visitor', 'jid':jid},[xmpp.Node('reason',{},reason)])])]))
		elif not nick and act=='kick': sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':'none', 'jid':jid},[xmpp.Node('reason',{},reason)])])]))
	elif act=='ban': sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':jid},[xmpp.Node('reason',{},reason)])])]))
	return None

def paste_text(text,room,jid):
	nick = get_nick_by_jid_res(room,jid)
	_html_paste = GT('html_paste_enable')
	if _html_paste:
		text = html_escape(text).replace(' ','&nbsp;')
		nick = html_escape(nick)
	paste_header = ['','<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><link href="%s" rel="stylesheet" type="text/css" /><title>\n' % paste_css_path][_html_paste]
	url = '%s%s' % (str(hex(int(time.time()*100)))[2:-1],['.txt','.html'][_html_paste])
	lt = tuple(time.localtime())
	ott = onlytimeadd(tuple(time.localtime()))
	paste_body = ['%s','<p><span class="paste">%s</span></p>\n'][_html_paste] % (text)
	lht = '%s [%s] - %02d/%02d/%02d %02d:%02d:%02d' % (nick,room,lt[0],lt[1],lt[2],lt[3],lt[4],lt[5])
	paste_he = ['%s\t\thttp://isida-bot.com\n\n' % lht,'%s%s</title></head><body><div class="main"><div class="top"><div class="heart"><a href="http://isida-bot.com">http://isida-bot.com</a></div><div class="conference">%s</div></div><div class="container">\n' % (paste_header,lht,lht)][_html_paste]
	fl = open(pastepath+url, 'a')
	fl.write(paste_he.encode('utf-8'))
	fl.write(paste_body.encode('utf-8'))
	paste_ender = ['','</div></div></body></html>'][_html_paste]
	fl.write(paste_ender.encode('utf-8'))
	fl.close()
	return pasteurl+url

def disp_time(*t):
	if len(t) == 2: rn = t[1]
	else: rn = ''
	t = t[0]
	lt=tuple(time.localtime(t))
	return '%02d:%02d:%02d, %02d.%s\'%s, %s' % (lt[3],lt[4],lt[5],lt[2],L(wmonth[lt[1]-1],rn).replace('_',''),lt[0],L(wday[lt[6]],rn))

def nice_time(*ttim):
	if len(ttim) == 2: rn = ttim[1]
	else: rn = ''
	ttim = ttim[0]	
	gt=tuple(time.gmtime(ttim))
	lt=tuple(time.localtime(ttim))
	timeofset = (datetime.datetime(*lt[:6])-datetime.datetime(*gt[:6])).seconds / 3600.0
	if timeofset < 0: t_gmt = 'GMT%s' % int(timeofset)
	else: t_gmt = 'GMT+%s' % int(timeofset)
	if timeofset%1: t_gmt += ':%02d' % int((timeofset%1*60/100) * 100)
	t_utc='%s%02d%02dT%02d:%02d:%02d' % gt[:6]
	t_display = '%02d:%02d:%02d, %02d.%s\'%s, %s, ' % (lt[3],lt[4],lt[5],lt[2],L(wmonth[lt[1]-1],rn).replace('_',''),lt[0],L(wday[lt[6]],rn))
	#t_tz = time.tzname[time.localtime()[8]]
	#enc = chardet.detect(t_tz)['encoding']
	#if t_tz == None: body = ''
	#if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	#t_tz = unicode(t_tz,enc)
	#t_display += '%s, %s' % (t_tz,t_gmt)
	#return t_utc,t_tz,t_display
	t_display += t_gmt
	return t_utc,t_gmt,t_display

def get_eval_item(mess,string):
	try:
		result = eval('mess.%s' % string)
		if result: return result.encode('utf-8')
	except: pass
	return ''

def match_for_raw(original,regexp,gr):
	orig_drop = orig_reg = re.findall(regexp, original.replace('\n',' '), re.S|re.I|re.U)
	while '' in orig_drop: orig_drop.remove('')
	orig_join = ''.join(orig_reg)
	if orig_join:
		#orig_split = original.split()
		#match_percent = 100.0 / len(original) * len(orig_join)
		#match_percent = 100.0 / len(orig_drop) * len(orig_split)
		match_percent = 100.0 / len(orig_drop) * sum([len(tmp) <= 2 for tmp in orig_drop])

		raw_percent = get_config(gr,'muc_filter_raw_percent')
		if raw_percent.isdigit(): raw_percent = int(raw_percent)
		else: raw_percent = int(config_prefs['muc_filter_raw_percent'][3])
		return ['',orig_join][match_percent >= raw_percent]
	else: return ''

def caps_matcher(c_caps,c_list):
	result = False
	for t in c_list:
		r = int(t[0] == '*')*2+int(t[-1] == '*')
		if r == 3 and t[1:-1].lower() in c_caps.lower(): return True
		elif r == 2 and c_caps.endswith(t[1:]): return True
		elif r == 1 and c_caps.startswith(t[:-1]): return True
		elif c_caps == t: return True
	return result

def iqCB(sess,iq):
	global timeofset, iq_in, iq_request, last_msg_base, last_msg_time_base, ddos_ignore, ddos_iq, user_hash, server_hash, server_hash_list
	global disco_excl, message_excl, users_locale
	iq_in += 1
	id = iq.getID()
	if id == None: return None
	room = unicode(iq.getFrom())
	if cur_execute_fetchone('select * from bot_owner where jid=%s',(getRoom(room),)): towh = selfjid
	else: towh = '%s/%s' % (getRoom(room),get_nick_by_jid_res(getRoom(room), selfjid))
	query = iq.getTag('query')
	was_request = id in iq_request
	al,tjid = get_level(getRoom(room),getResourse(room))
	acclvl = al >= 7 and GT('iq_disco_enable')
	nnj,tjid = False,getRoom(tjid)
	if room == selfjid: nnj = True
	else:
		for tmp in megabase:
			if '%s/%s' % tuple(tmp[0:2]) == room:
				nnj = True
				break

	c_lang = iq.getAttr('xml:lang')
	if c_lang: users_locale[room] = c_lang[:2].replace('uk','ua')

	if getServer(Settings['jid']) == room: nnj = True

	if iq.getType()=='error' and was_request:
		try: er_name = get_tag(unicode(iq),'error').replace('<','').split()[0]
		except: er_name = 'Unknown error!'
		iq_async(id,time.time(),er_name,'error')

	elif iq.getType()=='result' and was_request:
		try: nspace = query.getNamespace()
		except: nspace = 'None'
		if nspace == xmpp.NS_MUC_ADMIN: iq_async(id,nspace,time.time(),iq)
		elif nspace == xmpp.NS_MUC_OWNER: iq_async(id,nspace,time.time(),iq)
		elif nspace == xmpp.NS_VERSION:
			ver_client = unicode(query.getTagData(tag='name'))
			ver_version = unicode(query.getTagData(tag='version'))
			ver_os = unicode(query.getTagData(tag='os'))
			t = cur_execute_fetchone('select jid from versions where room=%s and jid=%s and client=%s and version=%s and os=%s',(getRoom(room),tjid,ver_client,ver_version,ver_os))
			if not t: cur_execute('insert into versions values (%s,%s,%s,%s,%s,%s)',(getRoom(room),tjid,ver_client,ver_version,ver_os,int(time.time())))
			iq_async(id,nspace,time.time(),'%s %s // %s' % (ver_client,ver_version,ver_os))
		elif nspace == xmpp.NS_TIME: iq_async(id,nspace,time.time(),query.getTagData(tag='display'),query.getTagData(tag='utc'),query.getTagData(tag='tz'))
		elif iq.getTag('time',namespace=xmpp.NS_URN_TIME): iq_async(id,xmpp.NS_URN_TIME,time.time(),iq.getTag('time').getTagData(tag='utc'),iq.getTag('time').getTagData(tag='tzo'))
		elif iq.getTag('vCard',namespace=xmpp.NS_VCARD): iq_async(id,xmpp.NS_VCARD,time.time(),unicode(iq),iq)
		else: iq_async(id,nspace,time.time(),unicode(iq),iq)

	elif iq.getType()=='get' and nnj and not ddos_ignore.has_key(tjid):
		iq_ddos_requests,iq_ddos_limit = GT('ddos_iq_requests'),GT('ddos_iq_limit')
		nick = getResourse(room)
		qry = unicode(iq.getTag(name='query'))
		if ddos_iq.has_key(tjid): time_tuple = [time.time()] + ddos_iq[tjid][:iq_ddos_requests-1]
		else: time_tuple = [time.time()]
		ddos_iq[tjid] = time_tuple
		if len(time_tuple) == iq_ddos_requests and (time_tuple[0]-time_tuple[-1]) < iq_ddos_limit:
			ddos_ignore[tjid] = [getRoom(room),nick,time.time()+GT('ddos_limit')[al]]
			pprint('!!! IQ-DDOS Detect: %s %s [%s] %s' % (al, room, tjid, qry),'bright_red')
			return
		for t in [tmp[2] for tmp in giq_hook if tmp[1] == 'get']:
			to_send = t(iq,id,room,acclvl,query,towh,al)
			if to_send:
				if to_send != True: sender(to_send)
				raise xmpp.NodeProcessed
	elif iq.getType()=='set':
		for t in [tmp[2] for tmp in giq_hook if tmp[1] == 'set']:
			to_send = t(iq,id,room,acclvl,query,towh,al)
			if to_send:
				if to_send != True: sender(to_send)
				raise xmpp.NodeProcessed

def iq_async_clean():
	global iq_reques
	while not game_over:
		to = GT('timeout')
		while to > 0 and not game_over:
			to -= 1
			time.sleep(1)
		if len(iq_request):
			for tmp in iq_request.keys():
				if iq_request[tmp][0] + GT('timeout') < time.time(): iq_request.pop(tmp)
				break

def presence_async_clean():
	global pres_answer
	while not game_over:
		to = GT('timeout')
		while to > 0 and not game_over:
			to -= 1
			time.sleep(1)
		if len(pres_answer):
			tm = []
			for tmp in pres_answer:
				if tmp[2] + GT('timeout') > time.time(): tm.append(tmp)
			pres_answer = tm

def iq_async(*answ):
	global iq_request
	req = iq_request.pop(answ[0])
	try: er_code = answ[3]
	except: er_code = None
	if er_code == 'error': is_answ = (answ[1]-req[0],(answ[2],'error'))
	elif req[3] == xmpp.NS_URN_PING or req[3] == answ[1]: is_answ = (answ[2]-req[0],answ[3:])
	elif req[3] == xmpp.NS_VCARD and answ[1] == 'None':
		answ[4].setTag('vCard',namespace=xmpp.NS_VCARD)
		is_answ = (answ[2]-req[0],answ[3:])
	else:
		pprint('!!! Got a fake iq answer. Request: %s. Answer: %s. Raw: %s' % (req[3],answ[1],answ[3]),'red')
		is_answ = (answ[2]-req[0],('%s %s' % (L('Error!'),L('Got a fake iq answer!')),))
	req[2].append(is_answ)
	thr(req[1],(tuple(req[2])),'iq_async_%s' % answ[0])

def remove_ignore():
	global ddos_ignore
	while not game_over:
		if len(ddos_ignore):
			tt = time.time()
			for tmp in ddos_ignore.keys():
				if tt > ddos_ignore[tmp][2]:
					try:
						ddos_ignore.pop(tmp)
						pprint('!!! DDOS: Jid %s is removed from ignore!' % tmp,'red')
					except: pprint('!!! DDOS: Unable find jid %s in ignore list. Perhaps it\'s removed by bot\'s owner!' % tmp,'red')
		time.sleep(10)

def com_parser(access_mode, nowname, type, room, nick, text, jid):
	global last_command, ddos_ignore
	jjid = getRoom(jid)
	if ddos_ignore.has_key(jjid): return
	if last_command[1:7] == [nowname, type, room, nick, text, jid] and time.time() < last_command[7]+GT('ddos_diff')[access_mode]:
		ddos_ignore[jjid] = [room,nick,time.time()+GT('ddos_limit')[access_mode]]
		pprint('!!! DDOS Detect: %s %s/%s %s %s' % (access_mode, room, nick, jid, text),'bright_red')
		send_msg(type, room, nick, L('Warning! Exceeded the limit of sending the same commands. You to ignore for %s.','%s/%s'%(room,nick)) % un_unix(GT('ddos_limit')[access_mode],'%s/%s'%(room,nick)))
		return None
	no_comm = True
	cof = cur_execute_fetchall('select * from commonoff;')#!!!
	for parse in comms:
		if access_mode >= parse[0] and nick != nowname:
			not_offed = True
			if access_mode != 9 or ignore_owner:
				for co in cof:
					if co[0]==room and co[1]==text.lower()[:len(co[1])]:
						not_offed = None
						break
			p1l = parse[1].lower()
			if not_offed and (text.lower() == p1l or text[:len(parse[1])+1].lower() in ['%s '%p1l,'%s\n'%p1l]):
				pprint('%s %s/%s [%s] %s' % (jid,room,nick,access_mode,text),'bright_cyan')
				no_comm = None
				if not parse[3]: thr(parse[2],(type, room, nick, parse[4:]),parse[1])
				elif parse[3] == 1: thr(parse[2],(type, room, nick),parse[1])
				elif parse[3] == 2: thr(parse[2],(type, room, nick, text[len(parse[1])+1:]),parse[1])
				last_command = [access_mode, nowname, type, room, nick, text, jid, time.time()]
				break
	return no_comm

def messageCB(sess,mess):
	global lfrom, lto, lastserver, lastnick, comms, message_in, no_comm, last_hash, current_join
	message_in += 1
	type=unicode(mess.getType())
	room=unicode(mess.getFrom().getStripped())
	allow_execute = True
	if getRoom(Settings['jid']) == getRoom(room):
		allow_execute = False
		msg = 'Warning! Self-message detected!'
		pprint('!!! %s Stanza:\n%s' % (msg,unicode(mess)))
		own = cur_execute_fetchall('select * from bot_owner;')
		if own:
			for ajid in own: send_msg('chat', ajid[0], '', msg)
	text=unicode(mess.getBody())
	id = mess.getID()
	try: was_send = messages_log.pop(id)
	except: was_send = None
	if was_send and type == 'error' and mess.getTag('error',attrs={'code':'500','type':'wait'}):
		time.sleep(time_limit)
		sender(was_send)
		return

	if current_join and room in [getRoom(t) for t in current_join.keys()]:
		try:
			tt = {}
			for t in mess.getTag('captcha',attrs={'xmlns':'urn:xmpp:captcha'}).getTag('x',attrs={'xmlns':'jabber:x:data'}).getTags('field'):
				tt[t.getAttrs()['var']] = t.getTagData('value')
			if current_join[tt['from']] == tt['sid']:
				pprint('*** Captcha: %s' % text)
				current_join[tt['from']] = text
			else: current_join.pop(tt['from'])
		except:
			for t in current_join.keys():
				if room == getRoom(t):
					current_join.pop(t)
					break
	try:
		code = mess.getTag('x',namespace=xmpp.NS_MUC_USER).getTagAttr('status','code')
		if code in msg_status_codes:
			append_message_to_log(room,'','',type,msg_status_codes[code])
			return
	except: pass
	if (text == 'None' or text == '') and not mess.getSubject(): return
	if mess.getTimestamp() != None: return
	nick=mess.getFrom().getResource()
	if nick != None: nick = unicode(nick)
	towh=unicode(mess.getTo().getStripped())
	lprefix = get_local_prefix(room)
	ft = back_text = text
	rn = '%s/%s' % (room,nick)
	access_mode,jid = get_level(room,nick)
	if not allow_execute: access_mode = -1
	nowname = get_xnick(room)
	if '@' not in jid and (jid == 'None' or jid.startswith('j2j.')) and is_owner(room): access_mode = 9
	if type == 'groupchat' and nick != '' and access_mode >= 0 and jid not in ['None',Settings['jid']]: talk_count(room,jid,nick,text)
	if nick != '' and nick != None and nick != nowname and len(text)>1 and text != 'None' and text != to_censore(text,room) and access_mode >= 0 and get_config(getRoom(room),'censor'):
		cens_text = L('Censored!',rn)
		lvl = get_level(room,nick)[0]
		if lvl >= 5 and get_config(getRoom(room),'censor_warning'): send_msg(type,room,nick,cens_text)
		elif lvl == 4 and get_config(getRoom(room),'censor_action_member') != 'off':
			act = get_config(getRoom(room),'censor_action_member')
			muc_filter_action(act,jid,room,cens_text)
		elif lvl < 4 and get_config(getRoom(room),'censor_action_non_member') != 'off':
			act = get_config(getRoom(room),'censor_action_non_member')
			muc_filter_action(act,jid,room,cens_text)
	no_comm = True
	if text != 'None' and text and access_mode >= 0 and not mess.getSubject():
		no_comm = True
		is_par = False
		if text.startswith('%s: ' % nowname) or text.startswith('%s, ' % nowname):
			text = text[len(nowname)+2:]
			is_par = True
		btext = text
		if text.startswith(lprefix):
			text = text[len(lprefix):]
			is_par = True
		if type == 'chat': is_par = True
		if is_par: no_comm = com_parser(access_mode, nowname, type, room, nick, text, jid)
		if no_comm:
			btl = btext.lower()
			if base_type == 'mysql': alias = cur_execute_fetchone("select match ,cmd from alias where (room=%s or room=%s) and ( match =%s or %s like concat( match ,' %%')) order by room desc",(room,'*',btl,btl))
			else: alias = cur_execute_fetchone("select match ,cmd from alias where (room=%s or room=%s) and ( match =%s or %s ilike match ||' %%') order by room desc",(room,'*',btl,btl))
			if alias:
				pprint('%s %s/%s [%s|alias] %s' % (jid,room,nick,access_mode,text),'bright_cyan')
				argz = btext[len(alias[0])+1:]
				if not argz:
					ppr = alias[1].replace('%*', '').replace('%{reduce}*', '').replace('%{reduceall}*', '').replace('%{unused}*', '')
					ppr = re.sub('\%\{nick2jid\}[0-9\*]','',ppr,flags=re.S|re.I|re.U)
					cpar = re.findall('%([0-9]+)', ppr, re.S)
					if len(cpar):
						for tmp in cpar:
							try: ppr = ppr.replace('%'+tmp,'')
							except: pass
				else:
					if '%' not in alias[1]: ppr = '%s %%*' % alias[1]
					else: ppr = alias[1]
					ppr = ppr.replace('%*', argz).replace('%{reduce}*', argz.strip()).replace('%{reduceall}*', reduce_spaces_all(argz))
					argz = argz.split()
					argzbk = list(argz)
					n2j = re.findall('\%\{nick2jid\}([0-9])',ppr,flags=re.S|re.I|re.U)
					if n2j:
						for t in n2j:
							it = int(t)
							try: curr_nick = get_jid_by_nick(room, argz[it])
							except: curr_nick = ''
							ppr = re.sub('\%%\{nick2jid\}%s' % t,curr_nick,ppr,flags=re.S|re.I|re.U)
							argzbk = argzbk[:it]+argzbk[it+1:]
					n2j = re.findall('\%\{nick2jid\}(\*)',ppr,flags=re.S|re.I|re.U)
					if n2j:
						curr_nick = get_jid_by_nick(room, ' '.join(argz))
						ppr = re.sub('\%\{nick2jid\}[0-9\*]',curr_nick,ppr,flags=re.S|re.I|re.U)
						argz = []
					if '%' in ppr:
						cpar = re.findall('%([0-9]+)', ppr, re.S)
						if cpar:
							for tmp in cpar:
								try:
									it = int(tmp)
									ppr = ppr.replace('%'+tmp,argz[it])
									argzbk = argzbk[:it]+argzbk[it+1:]
								except: pass
							ppr = ppr.replace('%{unused}*',' '.join(argzbk))

				if len(ppr) == ppr.count(' '): ppr = ''
				no_comm = com_parser(access_mode, nowname, type, room, nick, ppr, jid)

	thr(msg_afterwork,(mess,room,jid,nick,type,back_text,no_comm,access_mode,nowname),'msg_afterwork')

def msg_afterwork(mess,room,jid,nick,type,back_text,no_comm,access_mode,nowname):
	global topics
	not_alowed_flood = False
	subj = unicode(mess.getSubject())
	text = back_text
	if subj != 'None':
		if '\n' in subj: subj = '\n%s'  % subj
		subj = L('*** Topic: %s','%s/%s'%(room,nick)) % subj
		if len(text) and text != 'None': subj = text.replace(': ',':\n',1) if '\n' in text else text
		topics[room],nick = subj,''
		text = subj
		not_alowed_flood, no_comm = True, False

	# Fetch and store xhtml images!
	if type == 'groupchat' and get_config(room,'paste_xhtml_images'):
		try:
			raw_data = mess.getTag('html',attrs={'xmlns':'http://jabber.org/protocol/xhtml-im'}).getTag('body').getTagAttr('img','src')
			ext = re.findall('^data:image/(.*?);',raw_data[:32])[0]
			def unproc(t): return chr(int(t.group(0)[1:],16))
			img = re.sub('%[0-9A-F]{2}', unproc, raw_data.split('base64,',1)[1]).decode('base64')
			filename = '%s.%s' % (hex(int(time.time()))[2:],ext)
			fp = file(pastepath + filename, 'wb')
			fp.write(img)
			fp.close()
			send_msg(type, room, '', L('Fetched xhtml image: %s%s','%s/%s'%(room,nick)) % (pasteurl,filename))
			pprint('*** Fetched xhtml image from %s/%s [%s], size %s, file %s' % (room,nick,jid,len(img),pastepath + filename),'cyan')
		except: pass

	for tmp in gmessage: not_alowed_flood = tmp(room,jid,nick,type,text) or not_alowed_flood
	if no_comm:
		for tmp in gactmessage: not_alowed_flood = not_alowed_flood or tmp(room,jid,nick,type,text)
	if not not_alowed_flood and no_comm and text not in ['None','',' '] and not mess.getSubject():
		if room != selfjid: is_flood = get_config(getRoom(room),'flood') not in ['off',False]
		else: is_flood = None
		if selfjid != jid and access_mode >= 0 and (back_text[:len(nowname)+2] == nowname+': ' or back_text[:len(nowname)+2] == nowname+', ' or type == 'chat') and is_flood:
			pprint('Send msg human: %s/%s [%s] <<< %s' % (room,nick,type,text),'dark_gray')
			if len(back_text) > 128: send_msg_human(type, room, nick, L('Too many letters!','%s/%s'%(room,nick)), 'msg_human')
			else:
				if back_text[:len(nowname)] == nowname: back_text = back_text[len(nowname)+2:]
				try:
					text = getAnswer(type, room, nick, back_text)
					if text: send_msg_human(type, room, nick, text, 'msg_human')
				except: pass

def send_msg_human(type, room, nick, text, th):
	if nick: rn = '%s/%s' % (room,nick)
	else: rn = room
	pprint('Send msg human: %s [%s] >>> %s' % (rn,type,text),'dark_gray')
	thr(send_msg_hmn,(type, room, nick, text),th)

def send_msg_hmn(type, room, nick, text):
	time.sleep(len(text)/4.0+random.randint(0,3))
	send_msg(type, room, nick, text)

def to_censore(text,room):
	ccn = []
	custom_replace = {}
	if get_config(getRoom(room),'censor_custom'):
		custom_censor = get_config(getRoom(room),'censor_custom_rules').replace('\r','').replace('\t','').split('\n')
		for c in custom_censor:
			if c.count('#') <= 1: cc=c.split('#',1)
			else:
				cc=c.split('#')
				if cc[-1] == cc[-2] == '': cc = ['#'.join(cc[:-2]),'#']
				else: cc = ['#'.join(cc[:-1]),cc[-1]]
			if cc[0]:
				try:
					_ = re.compile(cc[0],re.S|re.I|re.U)
					ccn.append(cc[0])
					if len(cc) > 1: custom_replace[cc[0]] = reduce_spaces_all(cc[1])
				except: pass
	wca = None
	def_replacer = GT('censor_text')
	for c in censor+ccn:
		cn = re.findall(c,' %s ' % text,re.S|re.I|re.U)
		for tmp in cn:
			t = ''.join(tmp)
			try: replacer = custom_replace[c]
			except: replacer = def_replacer
			text,wca = text.replace(t,[replacer*len(t),replacer][len(replacer)>1]),True
	if wca: text = text.strip(' ')
	return text

def check_hash_actions():
	global hash_actions_list
	if hash_actions_list:
		for tmp in hash_actions_list.keys():
			if time.time() > hash_actions_list[tmp][1]:
				hal = hash_actions_list.pop(tmp)
				if hal[0] == L('whitelist'): put_config(tmp,'muc_filter_whitelist',False)
				elif hal[0] == L('lock by hash'):
					hashes_list = reduce_spaces_all(get_config(tmp,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
					if hal[2] in hashes_list:
						hashes_list.remove(hal[2])
						put_config(tmp,'muc_filter_deny_hash_list',' '.join(hashes_list))
					if not hashes_list: put_config(tmp,'muc_filter_deny_hash',False)
				pprint('Removed hash action %s in %s' % (hal[0],tmp),'cyan')

def presenceCB(sess,mess):
	global megabase, pres_answer, cu_age, presence_in, hashes, last_hash, users_locale
	presence_in += 1
	room=unicode(mess.getFrom().getStripped())
	nick=unicode(mess.getFrom().getResource())
	text=unicode(mess.getStatus())
	type=unicode(mess.getType())
	affiliation=unicode(mess.getAffiliation())
	role=unicode(mess.getRole())
	jid=unicode(mess.getJid())
	mss = unicode(mess)
	bad_presence = mss.count('<x xmlns=\"http://jabber') > 1 and mss.count(' affiliation=\"') > 1 and mss.count(' role=\"') > 1
	priority=unicode(mess.getPriority())
	show=unicode(mess.getShow())
	reason=unicode(mess.getReason())
	status=unicode(mess.getStatusCode())
	try: chg_nick = [None,esc_max2(mess.getTag('x',namespace=xmpp.NS_MUC_USER).getTagAttr('item','nick'))][status == '303']
	except: chg_nick = None
	actor=unicode(mess.getActor())
	to=unicode(mess.getTo())
	id = mess.getID()
	tt = int(time.time())
	if type=='error':
		try: error_code = mess.getTagAttr('error','code')
		except: error_code = None
		try: error_type = mess.getTagAttr('error','type')
		except: error_type = None
		try:
			error_text = mess.getTag('error').getTagData(tag='text')
			if not error_text: raise
		except:
			try: error_text = get_tag(unicode(mess.getTag('error')),'error')
			except: error_text = L('Unknown error!')
		if not error_text and presence_error.has_key(error_code): error_text = presence_error[error_code]
		if error_code:
			if error_type: error_msg = '%s [%s]' % (error_code,error_type)
			else: error_msg = error_code
			if error_text: error_msg = '%s - %s' % (error_msg,error_text)
		else:
			if error_type: error_msg = '%s [%s]' % (error_type.capitalize(),error_text)
			else: error_msg = error_text
		pres_answer.append((id,error_msg,tt))
		return
	elif id != None: pres_answer.append((id,None,tt))
	if jid == 'None': jid = get_level(room,nick)[1]

	# Get Caps
	if '%s|%s' % (role,affiliation) in levl:
		id_ver = id_lang = id_photo = id_avatar = 'error!'
		hash_error = False
		try: id_node = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
		except: id_node,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
		try: id_ver = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
		except: id_ver,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
		try: id_hash = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("hash")').decode('utf-8')
		except: id_hash,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("hash")'),True
		try: id_ext = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ext")').decode('utf-8')
		except: id_ext,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ext")'),True
		try:
			id_bmver = mess.getAttr('ver').decode('utf-8')
			if id_bmver or id_bmver == '': id_bmver = '%s_' % id_bmver
			else: id_bmver = ''
		except: id_bmver = ''
		if id_ext and id_hash: id_hash = '%s|%s' % (id_hash,id_ext)
		elif id_ext: id_hash = id_ext
		if id_hash: capses['%s/%s' % (room,nick)] = '%s\n%s [%s]\n%s' % (id_node,id_ver,id_hash,id_bmver)
		else: capses['%s/%s' % (room,nick)] = '%s\n%s\n%s' % (id_node,id_ver,id_bmver)

	# Hash control
	if '%s|%s' % (role,affiliation) in levl and levl['%s|%s' % (role,affiliation)] <= 3:
		try: id_lang = get_eval_item(mess,'getAttr("xml:lang")').decode('utf-8')
		except: id_lang,hash_error = get_eval_item(mess,'getAttr("xml:lang")'),True
		try: id_photo = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")').decode('utf-8')
		except: id_photo,hash_error = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")'),True
		try: id_avatar = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")').decode('utf-8')
		except: id_avatar,hash_error = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")'),True

		hash_body = '<'.join([unicode(tmp) for tmp in id_avatar,id_photo,id_ver,id_bmver,id_lang]) + '<<'
		if hash_error:
			writefile(slog_folder % 'bad_stanza_%s.txt' % int(time.time()),unicode(mess).encode('utf-8'))
			hash_body = parser(hash_body.decode('utf-8'))

		current_hash = hashlib.md5(hash_body.encode('utf-8')).digest().encode('base64').replace('\n','')
		hashes['%s/%s' % (room,nick)] = current_hash
		if type != 'unavailable' and not get_config(room,'muc_filter_whitelist') and get_config(room,'muc_filter_hash'):
			try: lh = last_hash[room]
			except: lh = [current_hash,[]]
			try:
				hash_ev = get_config_int(room,'muc_filter_hash_events')
				if not 3 <= hash_ev <= 1000: raise
			except:
				hash_ev = config_prefs['muc_filter_hash_events'][3]
				put_config(room,'muc_filter_hash_events',hash_ev)
			try:
				hash_tm = get_config_int(room,'muc_filter_hash_time')
				if not 3 <= hash_tm <= 1000: raise
			except:
				hash_tm = config_prefs['muc_filter_hash_time'][3]
				put_config(room,'muc_filter_hash_time',hash_tm)
			if current_hash == lh[0]:
				if lh[1]: lh[1] = [time.time()] + lh[1][:hash_ev-1]
				else: lh[1] = [time.time()]
				lh[0] = current_hash
			else: lh = [current_hash,[]]
			if lh[1] and len(lh[1]) == hash_ev and lh[1][0]-lh[1][-1] <= hash_tm:
				pprint('Hash high action: %s %s/%s' % (current_hash,room,nick),'red')
				h_action = get_config(room,'muc_filter_hash_action')
				try:
					h_action_time = get_config_int(room,'muc_filter_hash_action_time')
					if not 3 <= h_action_time <= 86400: raise
				except:
					h_action_time = config_prefs['muc_filter_hash_action_time'][3]
					put_config(room,'muc_filter_hash_action_time',h_action_time)
				hash_actions_list[room] = [h_action,h_action_time+time.time(),current_hash]
				if h_action == L('whitelist'): put_config(room,'muc_filter_whitelist',True)
				elif h_action == L('lock by hash'):
					put_config(room,'muc_filter_deny_hash',True)
					hashes_list = reduce_spaces_all(get_config(room,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
					if not current_hash in hashes_list:
						hashes_list.append(current_hash)
						put_config(room,'muc_filter_deny_hash_list',' '.join(hashes_list))
				h_action_current = get_config(room,'muc_filter_hash_action_current')
				if h_action_current != L('off'):
					pprint('MUC-Filter initial flush by hash: %s %s' % (room,jid),'brown')
					muc_filter_action(h_action_current,jid,room,L('Deny by hash lock!'))
					for tmp in hashes.keys():
						tmp_room,tmp_nick = tmp.split('/',1)
						if tmp_room == room and hashes[tmp] == current_hash:
							tmp_access,tmp_jid = get_level(room,tmp_nick)
							if tmp_access <= 3 and tmp_jid != 'None':
								in_base = cur_execute_fetchall('select sum(sum) from (select sum(age) from age where jid=%s and room=%s union all select %s-time from age where jid=%s and room=%s and status=0) as sum_age;',(getRoom(tmp_jid),room,int(time.time()),getRoom(tmp_jid),room))
								if not in_base: nmute = True
								else:
									newbie_time = get_config(room,'muc_filter_newbie_time')
									if newbie_time.isdigit(): newbie_time = int(newbie_time)
									else: newbie_time = 60
									if in_base[0] < newbie_time: nmute = True
									else: nmute = False
								if nmute:
									pprint('MUC-Filter flush by hash: %s %s' % (room,tmp_jid),'brown')
									muc_filter_action(h_action_current,tmp_jid,room,L('Deny by hash lock!'))
				lh = [current_hash,[]]
			last_hash[room] = lh

	if bad_presence: send_msg('groupchat', room, '', L('/me detect bad stanza from %s') % nick)
	nowname = get_xnick(room.lower())
	not_found,exit_type,exit_message = 0,'',''
	if type=='unavailable':
		try: users_locale.pop('%s/%s' % (room,nick))
		except: pass
		if status=='307': exit_type,exit_message = L('kicked'),reason
		elif status=='321': exit_type,exit_message = L('kicked'),L('revoke member affiliation in members-only room')
		elif status=='301': exit_type,exit_message = L('banned'),reason
		elif status=='303': exit_type,exit_message = L('change nick to %s') % chg_nick,''
		else: exit_type,exit_message = L('leave'),text
		if exit_message == 'None': exit_message = ''
		try: exit_message += '\r' + acl_ver_tmp['%s/%s' % (room,nick)]
		except: pass
		if nick != '':
			for mmb in megabase:
				if mmb[0]==room and mmb[1]==nick:
					megabase.remove(mmb)
					break
			if to == selfjid and status in ['307','301'] and cur_execute_fetchone('select room from conference where room=%s',('%s/%s' % (room,nick),)):
				cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(room),))
				pprint('*** bot was %s %s %s' % (['banned in','kicked from'][status=='307'],room,exit_message),'red')
				if GT('kick_ban_notify'):
					ntf_list = GT('kick_ban_notify_jid').replace(',',' ').replace('|',' ').replace(';',' ')
					while '  ' in ntf_list: ntf_list = ntf_list.replace('  ',' ')
					ntf_list = ntf_list.split()
					if len(ntf_list):
						ntf_msg = [L('banned in'),L('kicked from')][status == '307']
						ntf_msg = L('Bot was %s %s with reason: %s') % (ntf_msg,room,exit_message)
						for tmp in ntf_list: send_msg('chat', tmp, '', ntf_msg)
	else:
		if reason: exit_message = reason
		c_lang = mess.getAttr('xml:lang')
		if c_lang and nick: users_locale['%s/%s' % (room,nick)] = c_lang[:2].replace('uk','ua')
		if nick != '':
			for mmb in megabase:
				if mmb[0]==room and mmb[1]==nick:
					megabase.remove(mmb)
					megabase.append([room, nick, role, affiliation, jid])
					if role != mmb[2] or affiliation != mmb[3]: not_found = 1
					else: not_found = 2
					break
			if not not_found: megabase.append([room, nick, role, affiliation, jid])
	if jid == 'None': jid, jid2 = '<temporary>%s' % nick, 'None'
	else: jid2, jid = jid, getRoom(jid.lower())
	for tmp in gpresence: thr(tmp,(room,jid2,nick,type,(text, role, affiliation, exit_type, exit_message, show, priority, not_found, chg_nick)),'presence_afterwork')
	al = get_level(getRoom(room),nick)[0]
	if type == 'subscribe':
		if al == 9:
			caps_and_send(xmpp.Presence(room, 'subscribed'))
			caps_and_send(xmpp.Presence(room, 'subscribe'))
			pprint('Subscribtion accepted %s' % room,'light_gray')
		else:
			caps_and_send(xmpp.Presence(room, 'unsubscribed'))
			pprint('Subscribtion rejected %s' % room,'red')
	elif type == 'unsubscribed':
		if al == 9:
			caps_and_send(xmpp.Presence(room, 'unsubscribe'))
			caps_and_send(xmpp.Presence(room, 'unsubscribed'))
			pprint('Unsubscribtion accepted %s' % room,'light_gray')
		else: pprint('Unsubscribtion rejected %s' % room,'red')
	if reason in ['','None',None] and nick != '' and (nick != 'None' or (text != 'None' and len(text)>1)) and nick != nowname and al >= 0 and get_config(getRoom(room),'censor'):
		nt = '%s %s' % (nick,text)
		if nt != to_censore(nt,room):
			cens_text = L('Censored!','%s/%s'%(room,nick))
			if al >= 5 and get_config(getRoom(room),'censor_warning'): send_msg('groupchat',room,nick,cens_text)
			elif al == 4 and get_config(getRoom(room),'censor_action_member') != 'off':
				act = get_config(getRoom(room),'censor_action_member')
				muc_filter_action(act,jid2,getRoom(room),cens_text)
			elif al < 4 and get_config(getRoom(room),'censor_action_non_member') != 'off':
				act = get_config(getRoom(room),'censor_action_non_member')
				muc_filter_action(act,jid2,getRoom(room),cens_text)
	ab = cur_execute_fetchone('select * from age where room=%s and jid=%s and nick=%s',(room, jid, nick))
	ttext = '%s\n%s\n%s\n%s\n%s' % (role,affiliation,priority,show,text)
	if ab:
		if type=='unavailable': cur_execute('update age set time=%s, age=%s, status=%s, type=%s, message=%s where room=%s and jid=%s and nick=%s', (tt,ab[4]+(tt-ab[3]),1,exit_type,exit_message,room, jid, nick))
		else:
			if ab[5]: cur_execute('update age set time=%s, status=%s, message=%s where room=%s and jid=%s and nick=%s', (tt,0,ttext,room, jid, nick))
			else: cur_execute('update age set status=%s, message=%s where room=%s and jid=%s and nick=%s', (0,ttext,room, jid, nick))
	else: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (room,nick,jid,tt,0,0,'',ttext,nick.lower()))

	if not cur_execute_fetchone('select time from first_join where room=%s and jid=%s;',(room,jid)):
		cur_execute('insert into first_join values (%s,%s,%s);', (room,jid,tt))

def onoff_no_tr(msg):
	if msg in [None,False,0,'0']: return 'off'
	elif msg in [True,1,'1']: return 'on'
	else: return msg

def onoff(*msg):
	if len(msg) == 1: return L(onoff_no_tr(msg[0]))
	else: return L(onoff_no_tr(msg[0]),msg[1])

def getName(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	if '@' not in jid: return ''
	return jid[:jid.find('@')].lower()

def getServer(jid):
	jid = unicode(jid)
	if '/' not in jid: jid += '/'
	if jid == 'None': return jid
	return jid[jid.find('@')+1:jid.find('/')].lower()

def getResourse(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	try: return jid.split('/')[1]
	except: return ''

def getRoom(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	if '@' in jid: return '%s@%s' % (getName(jid),getServer(jid))
	else: return getServer(jid)

def now_schedule():
	while not game_over:
		to = GT('schedule_time')
		while to > 0 and not game_over:
			time.sleep(2)
			to -= 2
		if not game_over:
			for tmp in gtimer:
				if not game_over: thr(tmp,(),('time_thread_%s' % tmp).split(' ',2)[1])

def check_rss():
	global rss_processed
	if rss_processed: return
	l_hl = int(time.time())
	feedbase = cur_execute_fetchall('select * from feed order by time;')
	if feedbase:
		for fd in feedbase:
			ltime = fd[1]
			timetype = ltime[-1:].lower()
			if not timetype in ('h','m'): timetype = 'h'
			try: ofset = int(ltime[:-1])
			except: ofset = 4
			if timetype == 'h': ofset *= 3600
			elif timetype == 'm': ofset *= 60
			try: ll_hl = int(fd[3])
			except: ll_hl = 0
			in_room = cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%fd[4],))
			if ofset < 600: ofset = 600
			if in_room and ll_hl + ofset <= l_hl:
				rss_processed = True
				pprint('check rss: %s in %s' % (fd[0],fd[4]),'green')
				rss('groupchat', fd[4], 'RSS', 'new %s 10 %s silent' % (fd[0],fd[2]))
				break
	rss_processed = False

def talk_count(room,jid,nick,text):
	jid = getRoom(jid)
	ab = cur_execute_fetchone('select * from talkers where room=%s and jid=%s',(room,jid))
	wtext = len(reduce_spaces_all(text).split(' '))
	if ab: cur_execute('update talkers set nick=%s, words=%s, frases=%s where room=%s and jid=%s', (nick,ab[3]+wtext,ab[4]+1,room,jid))
	else: cur_execute('insert into talkers values (%s,%s,%s,%s,%s)', (room, jid, nick, wtext, 1))

def flush_stats():
	pprint('Executed threads: %s | Error(s): %s' % (th_cnt,thread_error_count),'bright_blue')
	pprint('Message in %s | out %s' % (message_in,message_out),'bright_blue')
	pprint('Presence in %s | out %s' % (presence_in,presence_out),'bright_blue')
	pprint('Iq in %s | out %s' % (iq_in,iq_out),'bright_blue')
	pprint('Unknown out %s' % unknown_out,'bright_blue')
	pprint('Cycles used %s | unused %s' % (cycles_used,cycles_unused),'bright_blue')
	if is_win32: ctypes.windll.Kernel32.SetConsoleTextAttribute(win_console_color, get_color_win32('clear'))

def disconnecter():
	global bot_exit_type, game_over
	pprint('--- Restart by disconnect handler! ---','bright_blue')
	pprint('--- Last stanza ---','bright_blue')
	pprint(last_stanza,'bright_blue')
	pprint('-'*19,'blue')
	game_over, bot_exit_type = True, 'restart'
	time.sleep(2)

def get_L_(jid):
	if jid:
		_CL = get_config(getRoom(jid),'set_default_locale')
		if _CL != 'off' and locales.has_key(_CL): return _CL
	try:
		loc = users_locale[jid]
		if locales.has_key(loc): return loc
		else: return CURRENT_LOCALE
	except: return CURRENT_LOCALE

def L(*par):
	if len(par) == 2: text,jid = par
	else: text,jid = par[0],''
	if not len(text): return text
	loc = get_L_(jid)
	try: return locales[loc][text]
	except: return text
	
def get_id():
	global id_count
	id_count += 1
	return 'request_%s' % id_count

def draw_warning(wt):
	wt = '!!! Warning! %s !!!' % wt
	pprint('!'*len(wt),'bright_red')
	pprint(wt,'bright_red')
	pprint('!'*len(wt),'bright_red')

def get_bot_version():
	if os.path.isfile(ver_file):
		bvers = readfile(ver_file).decode('utf-8').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		bV = '%s.%s-%s' % (botVersionDef,bvers,base_type)
		if bvers[:-1] == 'M': draw_warning('Launched bot\'s modification!')
	else: bV = '%s-%s' % (botVersionDef, base_type)
	return bV

def update_locale():
	global CURRENT_LOCALE
	locales = {}
	llist = ['en'] + [tmp[:-4] for tmp in os.listdir(loc_folder[:-6]) if tmp[-4:]=='.txt']
	CL = cur_execute_fetchone('select value from config_owner where option = %s', ('bot_locale',))
	if CL: CURRENT_LOCALE = CL[0]
	for t in llist:
		locales[t] = {}
		lf = loc_folder % t
		if os.path.isfile(lf):
			lf = readfile(lf).decode('UTF').replace('\r','').split('\n')
			for c in lf:
				if ('#' not in c[:3]) and len(c) and '\t' in c: locales[t][c.split('\t',1)[0].replace('\\n','\n').replace('\\t','\t')] = c.split('\t',1)[1].replace('\\n','\n').replace('\\t','\t')
	return locales,CURRENT_LOCALE

def init_hash():
	id_category = 'client'
	id_type = 'bot'
	id_lang = CURRENT_LOCALE
	id_name = 'iSida'
	capsHash = '%s<' % '/'.join([t.replace('/','//') for t in [id_category,id_type,id_lang,id_name]])
	bot_features.sort()
	capsHash += ''.join(['%s<' % t for t in bot_features])
	capsHash += '%s<' % xmpp.NS_SOFTWAREINFO
	tmp = ['%s<%s' % (t,bot_softwareinfo[t]) for t in bot_softwareinfo.keys()]
	tmp.sort()
	capsHash += ''.join(['%s<' % t for t in tmp])
	capsHash = hashlib.sha1(capsHash.encode('utf-8')).digest().encode('base64').replace('\n','')
	return id_category,id_type,id_lang,id_name,capsHash

def get_repo():
	dirs = os.listdir('.')+os.listdir('../')
	if '.svn' in dirs: return 'svn'
	elif '.git' in dirs: return 'git'
	else: return 'unknown'

def get_value_from_array2(a,v):
	for t in a:
		if t[0] == v: return t[1]
	return None

def get_array_from_array2(a1,a2):
	a_res = []
	for t in a1:
		if t[0] in a2: a_res.append(t)
	return a_res

def self_vcard():
	global iq_request
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(selfjid)}, payload = [xmpp.Node('vCard', {'xmlns': xmpp.NS_VCARD},[])])
	iq_request[iqid]=(time.time(),self_vcard_async,[],xmpp.NS_VCARD)
	sender(i)

def self_vcard_async(is_answ):
	global photo_hash
	try: vc = is_answ[1][1].getTag('vCard',namespace=xmpp.NS_VCARD)
	except: return
	if not vc or unicode(vc) == '<vCard xmlns="vcard-temp" />': return
	else:
		data = []
		for t in vc.getChildren():
			if t.getChildren():
				cm = []
				for r in t.getChildren():
					if r.getData(): cm.append(('%s.%s' % (t.getName(),r.getName()),unicode(r.getData())))
				data += cm
			elif t.getData(): data.append((t.getName(),t.getData()))
		if data:
			try:
				photo_data = get_value_from_array2(data,'PHOTO.BINVAL').decode('base64')
				photo_hash = hashlib.sha1(photo_data).hexdigest()
				PT('photo_hash',photo_hash)
			except: pass

# --------------------- Иницилизация переменных ----------------------

nmbrs = ['0','1','2','3','4','5','6','7','8','9','.']
ul = slog_folder % 'update.log'				# лог последнего обновление
halt_on_exception = False					# остановка на ошибках
debug_xmpppy = False				# отладка xmpppy
debug_console = False				# отладка действий бота
CommandsLog = None					# логгирование команд
prefix = '_'						# префикс комманд
msg_limit = 1000					# лимит размера сообщений
botName = 'iSida'					# название бота
botVersionDef = u'4.0'				# версия бота
disco_config_node = 'http://isida-bot.com/config'
pres_answer = []					# результаты посылки презенсов
iq_request = {}						# iq запросы
th_cnt = 0							# счётчик тредов
thread_error_count = 0				# счётчик ошибок тредов
bot_exit_type = None				# причина завершения бота
last_stream = []					# очередь станз к отправке
last_command = []					# последняя исполненная ботом команда
messages_log = {}					# лог отправленных сообщений
thread_type = True					# тип тредов
time_limit = 0.5					# максимальная задержка между посылкой станз с одинаковым типом в groupchat
time_nolimit = 0.1					# задержка между посылкой станз с разными типами
message_in,message_out = 0,0		# статистика сообщений
iq_in,iq_out = 0,0					# статистика iq запросов
presence_in,presence_out = 0,0		# статистика презенсов
unknown_out = 0						# статистика ошибочных отправок
cycles_used,cycles_unused = 0,0		# статистика циклов
id_count = 0						# номер запроса
megabase = []						# главная временная база с полной информацией из презенсов
ignore_owner = None					# исполнять отключенные команды для владельца бота
configname = 'settings/config.py'	# конфиг бота
topics = {}							# временное хранение топиков
last_msg_base = {}					# последние сообщения
last_msg_time_base = {}				# время между последними сообщениями последние сообщения
no_comm = True
muc_rejoins = {}
muc_statuses = {}
muc_repeat = {}
last_stanza = ''					# последняя станза, посланная ботом
ENABLE_TLS = True					# принудительное отключение TLS
ENABLE_SASL = True					# включение SASL
base_timeout = 20					# таймаут на доступ ко всем базам
between_msg_last = {}				# время последнего сообщения
last_sender_activity = time.time()	# время последней отправки
hashes = {}							# хеши презенсов
capses = {}							# капсы клиентов
last_hash = {}						# хеш последнего события
hash_actions_list = {}				# список действий на хеш-события
smile_folder = '.smiles'			# папка со смайлами в чатлогах
smile_descriptor = 'icondef.xml'	# дескриптор смайлов
last_logs_store = []				# последние записи в логах
last_logs_size = 20					# максимальное количество последних записей в логах
ddos_ignore = {}					# данные при подозрении на ddos
ddos_iq = {}
CURRENT_LOCALE = 'en'
user_hash = {}
server_hash = {}
server_hash_list = {}
newbie_msg = {}
mute_msg = {}
messages_excl = []
rss_processed = False
database_debug = False
current_join = {}
default_censor_set = 1				# номер набора правил для цензора
users_locale = {}
base_type = 'pgsql'     # тип базы: pgsql, mysql, sqlite3
base_name = 'isidabot'  # название базы
base_user = 'isidabot'  # пользователь базы
base_host = 'localhost' # хост базы
base_port = '5432'		# порт для подключения
base_charset = 'utf8'   # кодировка
bot_features = [xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_COMMANDS,disco_config_node,xmpp.NS_PING,xmpp.NS_URN_TIME,xmpp.NS_X_OOB,xmpp.NS_MUC_FILTER,
				xmpp.NS_VERSION,xmpp.NS_TIME,xmpp.NS_MUC,xmpp.NS_LAST,xmpp.NS_DATA,xmpp.NS_MUC_ROOMS]

gc.enable()

gt=tuple(time.gmtime())
lt=tuple(time.localtime())
if lt[0:3] == gt[0:3]: timeofset = int(lt[3])-int(gt[3])
elif lt[0:3] > gt[0:3]: timeofset = int(lt[3])-int(gt[3]) + 24
else: timeofset = int(gt[3])-int(lt[3]) + 24
is_win32 = sys.platform == 'win32'

if os.path.isfile(configname): execfile(configname)
else: errorHandler('%s is missed.' % configname)

if base_type == 'pgsql':
	import psycopg2
	import psycopg2.extensions
elif base_type == 'mysql':
	import mysql.connector as mysqldb
elif base_type == 'sqlite3':
	import sqlite3
else: errorHandler('Unknown database backend!')

if base_type in ['mysql','sqlite3']:
	class psycopg2():
		def InterfaceError(): return None

if thread_type:
	import threading
	sema = threading.BoundedSemaphore(value=30)
	#try: threading.stack_size(65536)
	#except ValueError: pass

	class KThread(threading.Thread):
		def __init__(self, *args, **keywords):
			threading.Thread.__init__(self, *args, **keywords)
			self.killed = False

		def start(self):
			self.__run_backup = self.run
			self.run = self.__run
			threading.Thread.start(self)

		def __run(self):
			sys.settrace(self.globaltrace)
			self.__run_backup()
			self.run = self.__run_backup

		def globaltrace(self, frame, why, arg):
			if why == 'call': return self.localtrace
			else: return None

		def localtrace(self, frame, why, arg):
			if self.killed:
				if why == 'line': raise SystemExit()
			return self.localtrace

		def kill(self): self.killed = True

	def garbage_collector():
		gc.collect()
		garbage_collector_timer = threading.Timer(3600,garbage_collector)
		garbage_collector_timer.start()

	garbage_collector()

else: import thread

if is_win32:
	import ctypes
	ctypes.windll.Kernel32.GetStdHandle.restype = ctypes.c_ulong
	win_console_color = ctypes.windll.Kernel32.GetStdHandle(ctypes.c_ulong(0xfffffff5))

botVersion = get_bot_version()
try: tmp = botOs
except: botOs = os_version()

tmp_os,tmp_ver = os_version_disco()
bot_softwareinfo = {'software':botName,'software_version':'%s-%s-%s' % (botVersionDef,get_repo().replace('unknown','none'),base_type),'os':tmp_os,'os_version':tmp_ver}

sm_f = os.path.join(public_log % smile_folder)
if os.path.isdir(sm_f):
	smiles_dirs_case = [sd for sd in os.listdir(sm_f) if sd[0] != '.' and os.path.isfile(os.path.join(sm_f,sd,smile_descriptor))]
	smiles_dirs = [sd.lower() for sd in smiles_dirs_case]
else: smiles_dirs, smiles_dirs_case = [], []

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)	# включение логгирования
capsNode = 'http://v4.isida-bot.com'
god = SuperAdmin.lower()

pprint('-'*50,'blue')
if os.path.basename(sys.argv[0]) != 'isida.py': errorHandler('Ugly launch detect! Read wiki!')

if base_type == 'pgsql': conn = psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
elif base_type == 'mysql': pass
elif base_type == 'sqlite3': pass
else: errorHandler('Can\'t connect to `%s` base type!' % base_type)

own = cur_execute_fetchall('select * from bot_owner;')
if not own: cur_execute('insert into bot_owner values (%s)',(SuperAdmin.lower(),))

pprint('*** Loading localization','white')
locales,CURRENT_LOCALE = update_locale()

pprint('*** Init caps hash','white')
id_category,id_type,id_lang,id_name,capsHash = init_hash()

pl_folder	= 'plugins/%s'

gpresence	= []
gmessage	= []
gactmessage	= []
giq_hook    = []

pprint('*** Loading Main plugin','white')
execfile(pl_folder % 'main.py')
pprint('*** Loading AI plugin','white')
execfile(pl_folder % 'ai.py')

GTIMER_DEF  = [check_rss,check_hash_actions,clean_user_and_server_hash]
pliname		= data_folder % 'ignored.txt'
gtimer		= list(GTIMER_DEF)
pprint('*** Loading other plugins','white')

pl,pl_ignore,plugins = os.listdir(pl_folder % ''),getFile(pliname,[]),[]
for tmp in pl:
	if tmp.endswith('.py') and not tmp.startswith('.') and tmp not in ['main.py','ai.py']: plugins.append(tmp)
plugins.sort()

for pl in plugins:
	if pl in pl_ignore: pprint('Ignore plugin: %s' % pl,'red')
	else:
		presence_control,message_control,message_act_control,iq_control,timer,execute,iq_hook = [],[],[],[],[],[],[]
		pprint('Append plugin: %s' % pl,'cyan')
		execfile(pl_folder % pl)
		for cm in execute: comms.append((cm[0],cm[1],cm[2],cm[3],'%s\r%s' % (pl[:-3],cm[4]))+cm[5:])
		for tmr in timer: gtimer.append(tmr)
		for tmp in presence_control: gpresence.append(tmp)
		for tmp in message_control: gmessage.append(tmp)
		for tmp in message_act_control: gactmessage.append(tmp)
		for tmp in iq_hook: giq_hook.append(tmp)
		giq_hook.sort()

if os.path.isfile(starttime_file):
	try: starttime = int(readfile(starttime_file))
	except: starttime = readfile(starttime_file)
else: starttime = int(time.time())
sesstime = int(time.time())
cu_age = []
close_age_null()
try:
	confbase = cur_execute_fetchall('select * from conference;')
	if confbase: confbase.sort()
	else: raise
except:
	c_room,c_passwd = '%s/%s' % (defaultConf.lower(),Settings['nickname']),''
	confbase = [(c_room,c_passwd)]
	cur_execute('insert into conference (room,passwd) values (%s,%s);',(c_room,c_passwd))

censor = []

if os.path.isfile(cens):
	cf = readfile(cens).decode('UTF').replace('\r','').split('# censor ')[default_censor_set].split('\n')
	for c in cf:
		if '#' not in c and len(c): censor.append(c)

if os.path.isfile(custom_cens):
	cf = readfile(cens).decode('UTF').replace('\r','').split('\n')
	for c in cf:
		if '#' not in c and len(c): censor.append(c)

pprint('*'*50,'blue')
pprint('*** Name: %s' % botName,'yellow')
pprint('*** Version: %s' % botVersion,'yellow')
pprint('*** OS: %s ' % botOs,'yellow')
pprint('*'*50,'blue')
pprint('*** (c) 2oo9-%s Disabler Production Lab.' % str(time.localtime()[0]).replace('0','o'),'bright_cyan')

if float(sys.version[:3]) < 2.7: errorHandler('Required Python >= 2.7')

lastnick = Settings['nickname']
jid = xmpp.JID(Settings['jid'])
if getResourse(jid) in ['None','']: jid = xmpp.JID(Settings['jid'].split('/')[0]+'/my owner is stupid and can not complete the configuration')
selfjid = jid
pprint('JID: %s' % unicode(jid),'light_gray')

message_exclude_update()
photo_hash = GT('photo_hash')
if not photo_hash: photo_hash = ''

try:
	try:
		Server = (':'.join(server.split(':')[:-1]),server.split(':')[-1])
		Port = int(Server[1])
		pprint('Trying to connect to %s' % server,'yellow')
	except: Server,Port = None,5222
	if debug_xmpppy: cl = xmpp.Client(jid.getDomain(),Port,ENABLE_TLS=ENABLE_TLS)
	else: cl = xmpp.Client(jid.getDomain(),Port,debug=[],ENABLE_TLS=ENABLE_TLS)
	try:
		Proxy = proxy
		pprint('Using proxy %s' % Proxy['host'],'green')
	except NameError: Proxy = None
	try:
		Secure = secure
		pprint('Tryins secured connection','cyan')
	except NameError: Secure = None
	con_stat = cl.connect(Server,Proxy,Secure,ENABLE_TLS=ENABLE_TLS)
	if con_stat: pprint('Connected as %s' % con_stat.upper(),'yellow')
	else: raise
except:
	pprint('No connection. Restart in %s sec.' % GT('reboot_time'),'red')
	time.sleep(GT('reboot_time'))
	sys.exit('restart')
auth_type = cl.auth(jid.getNode(), Settings['password'], jid.getResource(),sasl=ENABLE_SASL)
if auth_type: pprint('Authenticated via %s' % auth_type.upper(),'yellow')
else:
	pprint('Authentication error!','red')
	sys.exit('exit')
pprint('Registration Handlers','yellow')
cl.RegisterHandler('message',messageCB)
cl.RegisterHandler('iq',iqCB)
cl.RegisterHandler('presence',presenceCB)
cl.RegisterDisconnectHandler(disconnecter)
cl.UnregisterDisconnectHandler(cl.DisconnectHandler)
if GT('show_loading_by_status'):
	if GT('show_loading_by_status_show') == 'online': caps_and_send(xmpp.Presence(status=GT('show_loading_by_status_message'), priority=Settings['priority']))
	else: caps_and_send(xmpp.Presence(show=GT('show_loading_by_status_show'), status=GT('show_loading_by_status_message'), priority=Settings['priority']))
else:
	if Settings['status'] == 'online': caps_and_send(xmpp.Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(xmpp.Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))

pprint('Update self vcard','yellow')
self_vcard()
time.sleep(1)
pprint('Wait conference','yellow')
time.sleep(0.5)
game_over = None
thr(remove_ignore,(),'ddos_remove')
cb = []
is_start = True
lastserver = getServer(confbase[-1][0].lower())
join_percent, join_pers_add = 0, 100.0/len(confbase)

for tocon in confbase:
	if tocon[1]: pprint('->- %s | pass: %s' % tocon,'green')
	else: pprint('->- %s' % tocon[0],'green')
	if GT('show_loading_by_status_percent'):
		join_percent += join_pers_add
		join_status = '%s %s%%' % (GT('show_loading_by_status_message'),int(join_percent))
		if GT('show_loading_by_status'):
			if GT('show_loading_by_status_room'): join_status = '%s [%s]' % (join_status,tocon[0])
			if GT('show_loading_by_status_show') == 'online': caps_and_send(xmpp.Presence(status=join_status, priority=Settings['priority']))
			else: caps_and_send(xmpp.Presence(show=GT('show_loading_by_status_show'), status=join_status, priority=Settings['priority']))
	baseArg = unicode(tocon[0])
	if '/' not in baseArg: baseArg += '/%s' % unicode(Settings['nickname'])
	zz = join(baseArg, tocon[1])
	while unicode(zz)[:3] == '409' and not game_over:
		time.sleep(1)
		baseArg += '_'
		zz = join(baseArg, tocon[1])
	if zz:
		pprint('-!- Error "%s" while join in to %s' % (zz,baseArg),'red')
		if GT('show_loading_by_status'):
			if GT('show_loading_by_status_room'): join_status = L('Error while join in to %s - %s') % (tocon[0],zz)
			if GT('show_loading_by_status_show') == 'online': caps_and_send(xmpp.Presence(status=join_status, priority=Settings['priority']))
			else: caps_and_send(xmpp.Presence(show=GT('show_loading_by_status_show'), status=join_status, priority=Settings['priority']))
	else: pprint('-<- %s' % baseArg,'bright_green')
	if game_over: break
is_start = plugins_reload = None
pprint('Joined','white')

thr(now_schedule,(),'schedule')
thr(iq_async_clean,(),'async_iq_clean')
thr(presence_async_clean,(),'async_presence_clean')
try: thr(bomb_random,(),'bomb_random')
except: pass

if GT('show_loading_by_status'):
	if Settings['status'] == 'online': caps_and_send(xmpp.Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(xmpp.Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))

while 1:
	try:
		while not game_over:
			cyc = cl.Process(1)
			if str(cyc) == 'None': cycles_unused += 1
			elif int(str(cyc)): cycles_used += 1
			else: cycles_unused += 1
			if plugins_reload:
				from isida import update as isida_update
				isida_update(get_repo())
				botVersion = get_bot_version()
				bot_softwareinfo['software_version'] = botVersion
				pprint('*** Reload localization','white')
				locales,CURRENT_LOCALE = update_locale()
				pprint('*** Reinit caps hash','white')
				self_vcard()
				id_category,id_type,id_lang,id_name,capsHash = init_hash()
				gtimer,gpresence,gmessage,gactmessage,giq_hook = list(GTIMER_DEF),[],[],[],[]
				pprint('*** Reload Main plugin','white')
				execfile(pl_folder % 'main.py')
				pprint('*** Reload AI plugin','white')
				execfile(pl_folder % 'ai.py')
				pprint('*** Reload other plugins','white')
				pl,pl_ignore,plugins = os.listdir(pl_folder % ''),getFile(pliname,[]),[]
				for tmp in pl:
					if tmp.endswith('.py') and not tmp.startswith('.') and tmp not in ['main.py','ai.py']: plugins.append(tmp)
				plugins.sort()
				for pl in plugins:
					if pl in pl_ignore: pprint('Ignore plugin: %s' % pl,'red')
					else:
						presence_control,message_control,message_act_control,iq_control,timer,execute,iq_hook = [],[],[],[],[],[],[]
						pprint('Append plugin: %s' % pl,'cyan')
						execfile(pl_folder % pl)
						for cm in execute: comms.append((cm[0],cm[1],cm[2],cm[3],'%s\r%s' % (pl[:-3],cm[4]))+cm[5:])
						for tmr in timer: gtimer.append(tmr)
						for tmp in presence_control: gpresence.append(tmp)
						for tmp in message_control: gmessage.append(tmp)
						for tmp in message_act_control: gactmessage.append(tmp)
						for tmp in iq_hook: giq_hook.append(tmp)
						giq_hook.sort()
				pprint('*** Soft update finished! Plugins loaded: %s. Commands: %s' % (len(plugins)+1,len(comms)),'white')
				plugins_reload = None
		atempt_to_shutdown(False)
		sys.exit(bot_exit_type)

	except KeyboardInterrupt: atempt_to_shutdown_with_reason(L('Shutdown by CTRL+C...'),0,'exit',False)

	except xmpp.SystemShutdown: atempt_to_shutdown_with_reason(L('System Shutdown. Trying to restart in %s sec.') % GT('reboot_time'),GT('reboot_time'),'restart',False)

	except psycopg2.InterfaceError: atempt_to_shutdown_with_reason(L('Interface error! Trying to restart in %s sec.') % int(GT('reboot_time')/4),int(GT('reboot_time')/4),'restart',False)

	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		pprint('*** Error *** %s ***' % SM,'red')
		logging.exception(' [%s] ' % timeadd(tuple(time.localtime())))
		if 'parsing finished' in SM.lower() or 'database is locked' in SM.lower(): atempt_to_shutdown_with_reason(L('Critical error! Trying to restart in %s sec.') % int(GT('reboot_time')/4),GT('reboot_time')/4,'restart',True)
		if halt_on_exception: raise

# The end is near!

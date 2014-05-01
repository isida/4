#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Create and indexate databases for iSida Jabber Bot                       #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
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

import os, sys, sqlite3

set_folder = u'settings/'		# папка настроек

agestat = set_folder+u'agestat.db'	# статистика возрастов
jidbase = set_folder+u'jidbase.db'	# статистика jid'ов
talkers = set_folder+u'talkers.db'	# статистика болтунов
wtfbase = set_folder+u'wtfbase2.db'	# определения
answers = set_folder+u'answers.db'	# ответы бота
saytobase = set_folder+u'sayto.db'	# база команды "передать"
distbase = set_folder+u'dist_user.db'	# пользоватальская база команды "dist"

print 'Databases creator and indexator for Isida Jabber Bot v2.00 and higher'
print '(c) Disabler Production Lab.'

stb = os.path.isfile(agestat)
agest = sqlite3.connect(agestat)
cu_agest = agest.cursor()
print agestat,
if not stb:
	cu_agest.execute('''create table age (room text, nick text, jid text, time integer, age integer, status integer, type text, message text)''')
	agest.commit()
	print 'was created,',
else: print 'used exist,',
try: cu_agest.execute('''drop index rj''')
except: pass
try: cu_agest.execute('''drop index rnj''')
except: pass
cu_agest.execute('''create index rj on age (room,jid)''')
cu_agest.execute('''create index rnj on age (room,nick,jid)''')
agest.commit()
print 'indexed'
agest.close()

stb = os.path.isfile(jidbase)
jidst = sqlite3.connect(jidbase)
cu_jidst = jidst.cursor()
print jidbase,
if not stb:
	cu_jidst.execute('''create table jid (login text, server text, resourse text)''')
	jidst.commit()
	print 'was created,',
else: print 'used exist,',
try: cu_jidst.execute('''drop index log''')
except: pass
try: cu_jidst.execute('''drop index srv''')
except: pass
try: cu_jidst.execute('''drop index res''')
except: pass
cu_jidst.execute('''create index log on jid (login)''')
cu_jidst.execute('''create index srv on jid (server)''')
cu_jidst.execute('''create index res on jid (resourse)''')
jidst.commit()
print 'indexed'
jidst.close()

stb = os.path.isfile(talkers)
talkst = sqlite3.connect(talkers)
cu_talkst = talkst.cursor()
print talkers,
if not stb:
	cu_talkst.execute('''create table talkers (room text, jid text, nick text, words integer, frases integer)''')
	talkst.commit()
	print 'was created,',
else: print 'used exist,',
try: cu_talkst.execute('''drop index rj''')
except: pass
try: cu_talkst.execute('''drop index rjn''')
except: pass
cu_talkst.execute('''create index rj on talkers (room,jid)''')
cu_talkst.execute('''create index rjn on talkers (room,jid,nick)''')
talkst.commit()
print 'indexed'
talkst.close()

stb = os.path.isfile(wtfbase)
wtfst = sqlite3.connect(wtfbase)
cu_wtfst = wtfst.cursor()
print wtfbase,
if not stb:
	cu_wtfst.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text, lim integer)''')
	wtfst.commit()
	print 'was created,',
else: print 'used exist,',
try: cu_wtfst.execute('''drop index r''')
except: pass
try: cu_wtfst.execute('''drop index rj''')
except: pass
try: cu_wtfst.execute('''drop index rw''')
except: pass
try: cu_wtfst.execute('''drop index rww''')
except: pass
cu_wtfst.execute('''create index r on wtf (room)''')
cu_wtfst.execute('''create index rj on wtf (room,jid)''')
cu_wtfst.execute('''create index rw on wtf (room,wtfword)''')
cu_wtfst.execute('''create index rww on wtf (room,wtfword,wtftext)''')
wtfst.commit()
print 'indexed'
wtfst.close()

stb = os.path.isfile(answers)
answst = sqlite3.connect(answers)
cu_answst = answst.cursor()
print answers,
if not stb:
	cu_answst.execute('''create table answer (ind integer, body text)''')
	cu_answst.execute('insert into answer values (?,?)', (1,u';-)'))
	cu_answst.execute('insert into answer values (?,?)', (2,u'Привет'))
	answst.commit()
	print 'was created,',
else: print 'used exist,',
try: cu_answst.execute('''drop index id''')
except: pass
cu_answst.execute('''create index id on answer (ind)''')
answst.commit()
print 'indexed'
answst.close()

stb = os.path.isfile(saytobase)
sdb = sqlite3.connect(saytobase)
cu = sdb.cursor()
print saytobase,
if not stb:
	cu.execute('''create table st (who text, room text, jid text, message text)''')
	sdb.commit()
	print 'was created,',
else: print 'used exist,',
try: cu.execute('''drop index rj''')
except: pass
cu.execute('''create index rj on st (room,jid)''')
sdb.commit()
print 'indexed'
sdb.close()

if os.path.isfile(distbase):
	distb = sqlite3.connect(distbase)
	cu = distb.cursor()
	print distbase + ' used exist,',
	try: cu.execute('''drop index di''')
	except: pass
	cu.execute('''create index di on dist (point)''')
	distb.commit()
	print 'indexed'
	distb.close()

########################################

print 'Finished!'

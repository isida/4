#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Update iSida Jabber Bot from version 1.7 to 1.8                          #
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
wtfbase = set_folder+u'wtfbase.db'	# определения
answers = set_folder+u'answers.db'	# ответы бота

mainbase = set_folder+u'main.db'	# основная база данных

print 'Updater for Isida Jabber Bot from 1.7 to 1.8'
print '(c) Disabler Production Lab.'

print 'Open main base'

mdb = sqlite3.connect(mainbase)
cu = mdb.cursor()

print 'Create new bases'

os.system('rm -rf '+agestat)
agest = sqlite3.connect(agestat)
cu_agest = agest.cursor()
cu_agest.execute('''create table age (room text, nick text, jid text, time integer, age integer, status integer, type text, message text)''')
tmp = cu.execute('select * from age').fetchall()
print 'Import age statistic ...', len(tmp)
for aa in tmp:
	cu_agest.execute('insert into age values (?,?,?,?,?,?,?,?)', (aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7]))
agest.commit()
agest.close()

os.system('rm -rf '+jidbase)
jidst = sqlite3.connect(jidbase)
cu_jidst = jidst.cursor()
cu_jidst.execute('''create table jid (login text, server text, resourse text)''')
tmp = cu.execute('select * from jid').fetchall()
print 'Import jid base ...', len(tmp)
for aa in tmp:
	cu_jidst.execute('insert into jid values (?,?,?)', (aa[0],aa[1],aa[2]))
jidst.commit()
jidst.close()

os.system('rm -rf '+talkers)
talkst = sqlite3.connect(talkers)
cu_talkst = talkst.cursor()
cu_talkst.execute('''create table talkers (room text, jid text, nick text, words integer, frases integer)''')
tmp = cu.execute('select * from talkers').fetchall()
print 'Import talkers base ...', len(tmp)
for aa in tmp:
	cu_talkst.execute('insert into talkers values (?,?,?,?,?)', (aa[0],aa[1],aa[2],aa[3],aa[4]))
talkst.commit()
talkst.close()

os.system('rm -rf '+wtfbase)
wtfst = sqlite3.connect(wtfbase)
cu_wtfst = wtfst.cursor()
cu_wtfst.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text)''')
tmp = cu.execute('select * from wtf').fetchall()
cnt = 1
print 'Import wtf base ...', len(tmp)
for aa in tmp:
	cu_wtfst.execute('insert into wtf values (?,?,?,?,?,?,?)', (cnt,aa[1],aa[2],aa[3],aa[4],aa[5],aa[6]))
	cnt += 1
wtfst.commit()
wtfst.close()

os.system('rm -rf '+answers)
answst = sqlite3.connect(answers)
cu_answst = answst.cursor()
cu_answst.execute('''create table answer (ind integer, body text)''')
tmp = cu.execute('select * from answer').fetchall()
print 'Import auto-answer base ...', len(tmp)
cnt = 1
for aa in tmp:
	cu_answst.execute('insert into answer values (?,?)', (cnt,aa[1]))
	cnt += 1
answst.commit()
answst.close()


########################################

print 'Done'
mdb.close()
print 'Finished!'

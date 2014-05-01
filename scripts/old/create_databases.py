#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Create databases for iSida Jabber Bot                                    #
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

print 'Databases creator for Isida Jabber Bot v2.00 and higher'
print '(c) Disabler Production Lab.'

print 'Create new bases'

stb = os.path.isfile(agestat)
agest = sqlite3.connect(agestat)
cu_agest = agest.cursor()
if not stb:
	cu_agest.execute('''create table age (room text, nick text, jid text, time integer, age integer, status integer, type text, message text)''')
	agest.commit()
else: print agestat, 'was skiped!'
agest.close()

stb = os.path.isfile(jidbase)
jidst = sqlite3.connect(jidbase)
cu_jidst = jidst.cursor()
if not stb:
	cu_jidst.execute('''create table jid (login text, server text, resourse text)''')
	jidst.commit()
else: print jidbase, 'was skiped!'
jidst.close()

stb = os.path.isfile(talkers)
talkst = sqlite3.connect(talkers)
cu_talkst = talkst.cursor()
if not stb:
	cu_talkst.execute('''create table talkers (room text, jid text, nick text, words integer, frases integer)''')
	talkst.commit()
else: print talkers, 'was skiped!'
talkst.close()

stb = os.path.isfile(wtfbase)
wtfst = sqlite3.connect(wtfbase)
cu_wtfst = wtfst.cursor()
if not stb:
	cu_wtfst.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text, lim integer)''')
	wtfst.commit()
else: print wtfbase, 'was skiped!'
wtfst.close()

stb = os.path.isfile(answers)
answst = sqlite3.connect(answers)
cu_answst = answst.cursor()
if not stb:
	cu_answst.execute('''create table answer (ind integer, body text)''')
	cu_answst.execute('insert into answer values (?,?)', (1,u';-)'))
	cu_answst.execute('insert into answer values (?,?)', (2,u'Привет'))
	answst.commit()
else: print answers, 'was skiped!'
answst.close()

stb = os.path.isfile(saytobase)
sdb = sqlite3.connect(saytobase)
cu = sdb.cursor()
if not stb:
	cu.execute('''create table st (who text, room text, jid text, message text)''')
	sdb.commit()
else: print saytobase, 'was skiped!'
sdb.close()

########################################

print 'Finished!'

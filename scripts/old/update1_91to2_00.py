#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Update iSida Jabber Bot from version 1.9 to 2.00                         #
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

set_folder = u'settings/'				# папка настроек

wtfbase = set_folder+u'wtfbase.db'		# старые определения
wtfbase2 = set_folder+u'wtfbase2.db'	# новые определения

print 'Updater for Isida Jabber Bot from 1.8-1.91 to 2.00'
print '(c) Disabler Production Lab.'

os.system('rm -rf '+wtfbase2)

wtf1 = sqlite3.connect(wtfbase)
cu_wtf1 = wtf1.cursor()

wtf2 = sqlite3.connect(wtfbase2)
cu_wtf2 = wtf2.cursor()
cu_wtf2.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text, lim integer)''')

tmp = cu_wtf1.execute('select * from wtf').fetchall()
print 'Import wtf base ...', len(tmp)
for aa in tmp:
	if aa[1] == 'global': aa += (5,)
	else: aa += (0,)
	cu_wtf2.execute('insert into wtf values (?,?,?,?,?,?,?,?)', aa)
wtf2.commit()
wtf2.close()
wtf1.close()

print 'Finished!'

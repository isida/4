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

def answers_ie(type, jid, nick, text):
	if text.lower().strip().split(' ',1)[0] == 'export':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		base_size = len(cur_execute_fetchall('select * from answer'))
		fnd = cur_execute_fetchall('select body from answer where body ilike %s group by body order by body',('%',))
		answer = ''
		msg = L('Export to file: %s | Total records: %s | Unique records: %s','%s/%s'%(jid,nick)) % (fname,base_size,len(fnd))
		for i in fnd:
			if i[0] != '': answer += i[0].strip() +'\n'
		writefile(fname,answer.encode('utf-8'))
	elif text.lower().strip().split(' ',1)[0] == 'import':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		if os.path.isfile(fname):
			answer = readfile(fname).decode('utf-8')
			answer = answer.split('\n')
			cur_execute('delete from answer where body ilike %s',('%',))
			msg = L('Import from file: %s | Total records: %s','%s/%s'%(jid,nick)) % (fname,len(answer))
			idx = 1
			for i in answer:
				if i != '':
					cur_execute('insert into answer values (%s,%s)', (idx,unicode(i.strip())))
					idx += 1
		else: msg = L('File %s not found!','%s/%s'%(jid,nick)) % fname
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'answers', answers_ie, 2, 'Import/Export answers base.\nanswers import [filename] - import from file\nanswers export [filename] - export to file')]

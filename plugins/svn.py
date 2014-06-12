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

def svn_get(type, jid, nick,text):
	if len(text):
		if text[:7] !='http://' and text[:8] !='https://' and text[:6] !='svn://': text = 'http://%s' % text
		count,revn = 1,0
		if '-v' in text.split(): text,verb = reduce_spaces_all(text.replace('-v','')),True
		else: verb = False
		text = ''.join(re.findall('[-a-z\/\:\.0-9\ ]+', text, re.S+re.I+re.U))
		if ' ' in text:
			text = text.split(' ')
			url = text[0]
			try: count = int(text[1])
			except:
				try:
					if 'r' in text[1].lower(): revn = int(text[1][text[1].find('r')+1:])
				except: revn = 0
		else: url=text
		if revn != 0: sh_exe = 'sh -c \"LANG=%s svn log %s -r%s\"' % (L('en_EN.UTF8','%s/%s'%(jid,nick)),url,revn)
		else:
			if count > 10: count = 10
			sh_exe = 'sh -c \"LANG=%s svn log %s --limit %s\"' % (L('en_EN.UTF8','%s/%s'%(jid,nick)),url,count)
		if verb: sh_exe = '%s -v\"' % sh_exe[:-1]
		svn_log = shell_execute(sh_exe,'%s/%s'%(jid,nick)).replace('\n\n','\n')
		while svn_log and svn_log[-1] in ['-','\n']: svn_log = svn_log[:-1]
		rpl = re.findall('-{10,}',svn_log)
		if rpl: svn_log = svn_log.replace(rpl[0],'-'*3)
		msg = 'SVN from %s\n%s' % (url,svn_log)
	else: msg = L('Read user manual for commands...','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'svn', svn_get, 2, 'Show svn log.\nsvn [http://]url [limit] - show last revision(s) limit\nsvn [http://]url rXXX - show XXX revision')]

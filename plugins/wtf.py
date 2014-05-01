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

def wtfall(type, jid, nick, text):
	if text:
		ww = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by -time',(jid,'global','import',text))
		if ww: msg = L('I know that %s is %s','%s/%s'%(jid,nick)) % (text,'\n%s' % '\n\n'.join([L('from %s: %s','%s/%s'%(jid,nick)) % (t[3],t[5]) for t in ww]))
		else: msg = L('I don\'t know!','%s/%s'%(jid,nick))
	else: msg = L('What search?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def wtfsearch(type, jid, nick, text):
	if text:
		text = '%%%s%%' % text
		ww = cur_execute_fetchall('select wtfword from wtf where (room=%s or room=%s or room=%s) and (room ilike %s or jid ilike %s or nick ilike %s or wtfword ilike %s or wtftext ilike %s)',(jid,'global','import',text,text,text,text,text))
		if ww: msg = L('Some matches in definitions: %s','%s/%s'%(jid,nick)) % ', '.join(zip(*ww)[0])
		else: msg = L('No matches.','%s/%s'%(jid,nick))
	else: msg = L('What need to find?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def wtfrand(type, jid, nick):
	ww = cur_execute_fetchall('select * from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	tlen = len(ww)
	ww = ww[random.randint(0,tlen-1)]
	msg = L('I know that %s is %s','%s/%s'%(jid,nick)) % (ww[4],ww[5])
	send_msg(type, jid, nick, msg)

def wtfnames(type, jid, nick, text):
	text = text.strip().lower()
	if text == 'all': tmp = cur_execute_fetchall('select distinct wtfword from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	elif text in ['global','import']: tmp = cur_execute_fetchall('select distinct wtfword from wtf where room=%s',(text,))
	else: tmp = cur_execute_fetchall('select distinct wtfword from wtf where room=%s',(jid,))
	if tmp: msg = L('All I know is: %s','%s/%s'%(jid,nick)) % ', '.join(zip(*tmp)[0])
	else: msg = L('No matches.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def wtfcount(type, jid, nick):
	tlen = cur_execute_fetchall('select count(*) from wtf')[0][0]
	cnt = cur_execute_fetchall('select count(*) from wtf where room=%s',(jid,))[0][0]
	glb = cur_execute_fetchall('select count(*) from wtf where room=%s',('global',))[0][0]
	imp = cur_execute_fetchall('select count(*) from wtf where room=%s',('import',))[0][0]
	msg = L('Locale definition: %s\nGlobal: %s\nImported: %s\nTotal: %s','%s/%s'%(jid,nick)) % (cnt,glb,imp,tlen)
	send_msg(type, jid, nick, msg)

def wtf(type, jid, nick, text): wtf_get(0,type, jid, nick, text)

def wtff(type, jid, nick, text): wtf_get(1,type, jid, nick, text)

def wwtf(type, jid, nick, text): wtf_get(2,type, jid, nick, text)

def wtfp(type, jid, nick, text):
	if '\n' in text:
		text = text.split('\n')
		tnick = text[1]
		ttext = text[0]
		is_found = 0
		for mmb in megabase:
			if mmb[0]==jid and mmb[1]==tnick:
				is_found = 1
				break
		if is_found:
			wtf_get(0,'chat', jid, tnick, ttext)
			send_msg(type, jid, nick, L('Send to private %s','%s/%s'%(jid,nick)) % tnick)
		else: send_msg(type, jid, nick, L('Nick %s not found!','%s/%s'%(jid,nick)) % tnick)
	else: wtf_get(0,'chat', jid, nick, text)

def wtf_get(ff,type, jid, nick, text):
	if text:
		ww = cur_execute_fetchone('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by -time',(jid,'global','import',text))
		if ww:
			msg = L('I know that %s is %s','%s/%s'%(jid,nick)) % (text,ww[5])
			if ff == 1: msg += L('\nfrom: %s %s','%s/%s'%(jid,nick)) % (ww[3],'[%s]' % disp_time(ww[6],'%s/%s'%(jid,nick)))
			elif ff == 2: msg = L('I know that %s was defined by %s %s %s','%s/%s'%(jid,nick)) % (text,ww[3],'(%s)' % ww[2],'[%s]' % disp_time(ww[6],'%s/%s'%(jid,nick)))
		else: msg = L('I don\'t know!','%s/%s'%(jid,nick))
	else: msg = L('What search?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def dfn(type, jid, nick, text):
	text = text.strip()
	if '=' in text and text[0] != '=':
		al, realjid = get_level(jid,nick)
		what, text = map(lambda x: x.strip(), text.split('=', 1))
		matches = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by -time',(jid,'global','import',what))
		if matches:
			match_jid = None
			grr = getRoom(realjid)
			for t in matches:
				if getRoom(t[2]) == grr:
					match_jid = t[2]
					break
			if matches[0][1] == 'global': msg, text = L('This is global definition and not allowed to change!','%s/%s'%(jid,nick)), ''
			elif text == '':
				if match_jid:
					msg = L('Definition removed!','%s/%s'%(jid,nick))
					cur_execute('delete from wtf where wtfword=%s and room=%s and jid=%s',(what,jid,match_jid))
				else: msg = L('This definition is not Your!','%s/%s'%(jid,nick))
			else:
				msg = L('Definition updated!','%s/%s'%(jid,nick))
				if match_jid: cur_execute('delete from wtf where wtfword=%s and room=%s and jid=%s',(what,jid,match_jid))
		elif text == '': msg = L('Nothing to remove!','%s/%s'%(jid,nick))
		else: msg = L('Definition saved!','%s/%s'%(jid,nick))
		idx = cur_execute_fetchall('select count(*) from wtf')[0][0]
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, jid, realjid, nick, what, text, int(time.time()),al))
	else: msg = L('What need to remember?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def gdfn(type, jid, nick, text):
	text = text.strip()
	if '=' in text and text[0] != '=':
		al, realjid = get_level(jid,nick)
		what, text = map(lambda x: x.strip(), text.split('=', 1))
		matches = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by lim,-time',(jid,'global','import',what))
		if matches:
			max = -1
			for t in matches:
				if t[7] >= max: max,match=t[7],t
			if match[7] > al:
				msg,text = L('Not enough rights!','%s/%s'%(jid,nick)),''
				try: msg += ' ' + L(unlevltxt[unlevlnum[match[7]]],'%s/%s'%(jid,nick)) % L(unlevl[match[7]],'%s/%s'%(jid,nick))
				except: pass
			elif text == '':
				msg = L('Definition removed!','%s/%s'%(jid,nick))
				cur_execute('delete from wtf where wtfword=%s',(what,))
			else:
				msg = L('Definition updated!','%s/%s'%(jid,nick))
				if getRoom(realjid) == getRoom(match[2]): cur_execute('delete from wtf where wtfword=%s and jid=%s',(what,match[2]))
		elif text == '': msg = L('Nothing to remove!','%s/%s'%(jid,nick))
		else: msg = L('Definition saved!','%s/%s'%(jid,nick))
		idx = cur_execute_fetchall('select count(*) from wtf')[0][0]
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, 'global', realjid, nick, what, text, int(time.time()),al))
	else: msg = L('What need to remember?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'wtfrand', wtfrand, 1, 'Random definition from base.'),
	 (3, 'wtfnames', wtfnames, 2, 'List of definitions in conference.\nwtfnames [all|global|import]'),
	 (3, 'wtfcount', wtfcount, 1, 'Definitions count.'),
	 (3, 'wtfsearch', wtfsearch, 2, 'Search in definitions base.'),
	 (3, 'wtfall', wtfall, 2, 'All definitions of word.'),
	 (9, 'wwtf', wwtf, 2, 'Information about definition commiter.'),
	 (3, 'wtff', wtff, 2, 'Show definition with nick and date.'),
	 (3, 'wtfp', wtfp, 2, 'Show definition in private.\nwtfp word\n[nick]'),
	 (0, 'wtf', wtf, 2, 'Show definition.'),
	 (3, 'dfn', dfn, 2, 'Set definition.\ndfn word=definition - remember definition as word\ndfn word= - remove definition word'),
	 (3, 'gdfn', gdfn, 2, 'Set global definition.\ngdfn word=definition - remember definition as word\ngdfn word= - remove definition word')]

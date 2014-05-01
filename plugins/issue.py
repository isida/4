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

# id, room, jid, nick, level, tags, body, status, date, comment, accept_by, accept_date

# translate: new,pending,accepted,rejected,removed,done,Pending by,Accepted by,Rejected by,Removed by,Mark as done by

issue_status = ['new','pending','accepted','rejected','removed','done']
issue_status_show = ['','Pending by','Accepted by','Rejected by','Removed by','Mark as done by']
issue_new_id     = 0
issue_pending_id = 1
issue_accept_id  = 2
issue_reject_id  = 3
issue_remove_id  = 4
issue_done_id    = 5
issue_number_format = '#%04d'

def issue(type, room, nick, text):
	ttext = reduce_spaces_all(text)
	subc = ttext.split()
	acclvl,jid = get_level(room,nick)
	if ttext.isdigit() or (ttext and ttext[0] == '#' and ttext[1:].isdigit()) or not subc or len(subc) == 1 or subc[0] == 'show' or (acclvl <= 3 and type == 'chat'): msg,type = issue_show(subc,room,type,nick)
	elif subc[0] in ['del','delete','rm','remove']: msg = issue_remove(subc,acclvl,room,jid,nick)
	elif subc[0] == 'pending': msg = issue_pending(subc,acclvl,room,jid,nick)
	elif subc[0] == 'accept': msg = issue_accept(subc,acclvl,room,jid,nick)
	elif subc[0] == 'reject': msg = issue_reject(subc,acclvl,room,jid,nick)
	elif subc[0] == 'done': msg = issue_done(subc,acclvl,room,jid,nick)
	else: msg = issue_new(subc,acclvl,room,jid,nick,text)
	send_msg(type, room, nick, msg)

def issue_new(s,acclvl,room,jid,nick,text):
	tags = []
	for t in s:
		if t[0] == '*' and len(t) > 1:
			tags.append(t[1:])
			text = text.replace(t,'',1)
		else: break
	s = s[len(tags):]
	if not s: return L('No issue\'s body!','%s/%s'%(room,nick))
	tags = ' '.join(tags)
	body = text.strip()
	try: id = cur_execute_fetchone('select count(*) from issues where room=%s',(room,))[0] + 1
	except: id = 1
	tbody = cur_execute_fetchall('select id from issues where room=%s and body ilike %s',(room,'%%%s%%' % body))
	if tbody: return L('I know same issue(s): %s','%s/%s'%(room,nick)) % ', '.join(issue_number_format % t for t in zip(*tbody)[0])
	stts = cur_execute('insert into issues values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (id, room, getRoom(jid), nick, acclvl, tags, body, issue_new_id, int(time.time()),'','',0))
	if stts == True: return L('Added issue %s','%s/%s'%(room,nick)) % issue_number_format % id
	else: return str(stts)

def issue_show(s,room,type,nick):
	if len(s) > 1 and s[0] == 'show': s = s[1]
	elif len(s) == 1 and s[0] == 'show': s = '%'
	elif s: s = s[0]
	else: s = '%'
	
	if s.isdigit() or (s[0] == '#' and s[1:].isdigit()): s = s.replace('#','')	

	s_original = s
	
	if s.isdigit(): iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and id=%s order by id;',(room,int(s)))
	elif s[0] == '*': iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and tags ilike %s and status<%s order by id;',(room,'%%%s%%' % s[1:],issue_reject_id))
	else:
		if s != '%': s = '%%%s%%' % s
		iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and (tags ilike %s or body ilike %s or comment ilike %s or nick ilike %s) and status<%s order by id;',(room,s,s,s,s,issue_reject_id))
	if iss:
		tm = []
		if len(iss) > 1 and type == 'groupchat':
			send_msg(type, room, nick, L('Sent in private message','%s/%s'%(room,nick)))
			type = 'chat'
		for t in iss:
			if t[2]: tmp = '%s (%s) *%s | %s\n%s' % (issue_number_format % t[0],L(issue_status[t[4]],'%s/%s'%(room,nick)),' *'.join(t[2].split()),L('Created by %s','%s/%s'%(room,nick)) % t[1],t[3])
			else: tmp = '%s (%s) %s\n%s' % (issue_number_format % t[0],L(issue_status[t[4]],'%s/%s'%(room,nick)),L('Created by %s','%s/%s'%(room,nick)) % t[1],t[3])
			if t[4]:
				tmp = '%s\n%s %s [%s]' % (tmp,L(issue_status_show[t[4]],'%s/%s'%(room,nick)),t[6],disp_time(t[7],'%s/%s'%(room,nick)))
				if t[5]: tmp += L(', by reason: %s','%s/%s'%(room,nick)) % t[5]
			tm.append(tmp)
		return L('Issue(s) list:\n%s','%s/%s'%(room,nick)) % '\n\n'.join(tm), type
	elif s_original == '%': return L('Issues not found!','%s/%s'%(room,nick)), type
	else: return L('Issues with match \'%s\' not found!','%s/%s'%(room,nick)) % s_original, type

def issue_remove(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need remove?','%s/%s'%(room,nick))
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.','%s/%s'%(room,nick))
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.','%s/%s'%(room,nick))
	if iss:
		if iss[0][2] != issue_remove_id:
			if acclvl >= 7 or iss[0][0] == jid:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_remove_id,nick,int(time.time()),cmt,room,id))
				return L('Issue %s removed!','%s/%s'%(room,nick)) % issue_number_format % id
			else: return L('There is not Your issue or You have no rights to remove it.','%s/%s'%(room,nick))
		else: return L('Issue %s was removed earlier!','%s/%s'%(room,nick)) % issue_number_format % id
	else: return L('Issue %s not found!','%s/%s'%(room,nick)) % issue_number_format % id

def issue_accept(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need accept?','%s/%s'%(room,nick))
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.','%s/%s'%(room,nick))
		iss = cur_execute_fetchall('select jid,level,status,tags from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.','%s/%s'%(room,nick))
	if iss:
		if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
			if len(s) > 2:
				tags = iss[0][3].split()
				cnt = 2
				for t in s[2:]:
					if t[0] == '*' and len(t) > 1:
						if t[1:] not in tags: tags.append(t[1:])
						else: tags.remove(t[1:])
						cnt += 1
					else: break
				s = s[cnt:]
				tags = ' '.join(tags)
				cmt = ' '.join(s)
			else: cmt,tags = '',iss[0][3]
			cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s,tags=%s where room=%s and id=%s', (issue_accept_id,nick,int(time.time()),cmt,tags,room,id))
			if iss[0][2] != issue_accept_id: return L('Issue %s accepted!','%s/%s'%(room,nick)) % issue_number_format % id
			else: return L('Issue %s was accepted earlier!','%s/%s'%(room,nick)) % issue_number_format % id
		else: return L('There is not Your issue or You have no rights to accept it.','%s/%s'%(room,nick))
	else: return L('Issue %s not found!','%s/%s'%(room,nick)) % issue_number_format % id

def issue_reject(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need reject?','%s/%s'%(room,nick))
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.','%s/%s'%(room,nick))
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.','%s/%s'%(room,nick))
	if iss:
		if iss[0][2] != issue_reject_id:
			if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_reject_id,nick,int(time.time()),cmt,room,id))
				return L('Issue %s rejected!','%s/%s'%(room,nick)) % issue_number_format % id
			else: return L('There is not Your issue or You have no rights to reject it.','%s/%s'%(room,nick))
		else: return L('Issue %s was rejected earlier!','%s/%s'%(room,nick)) % issue_number_format % id
	else: return L('Issue %s not found!','%s/%s'%(room,nick)) % issue_number_format % id

def issue_pending(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue is pending?','%s/%s'%(room,nick))
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.','%s/%s'%(room,nick))
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.','%s/%s'%(room,nick))
	if iss:
		if iss[0][2] != issue_reject_id:
			if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_pending_id,nick,int(time.time()),cmt,room,id))
				return L('Issue %s is mark as pending!','%s/%s'%(room,nick)) % issue_number_format % id
			else: return L('There is not Your issue or You have no rights to mark as pending.','%s/%s'%(room,nick))
		else: return L('Issue %s was marked as pending earlier!','%s/%s'%(room,nick)) % issue_number_format % id
	else: return L('Issue %s not found!','%s/%s'%(room,nick)) % issue_number_format % id

def issue_done(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue is done?','%s/%s'%(room,nick))
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.','%s/%s'%(room,nick))
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.','%s/%s'%(room,nick))
	if iss:
		if iss[0][2] != issue_reject_id:
			if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_done_id,nick,int(time.time()),cmt,room,id))
				return L('Issue %s marked as done!','%s/%s'%(room,nick)) % issue_number_format % id
			else: return L('There is not Your issue or You have no rights to mark as done.','%s/%s'%(room,nick))
		else: return L('Issue %s was marked as done earlier!','%s/%s'%(room,nick)) % issue_number_format % id
	else: return L('Issue %s not found!','%s/%s'%(room,nick)) % issue_number_format % id

global execute

execute = [(3, 'issue', issue, 2, 'Issues\nissue [[[show|pending|accept|reject|delete|done] id] reason] - actions with issue\nissue *tag1 *tag2 some text - add issue `some text` with tags tag1 and tag2')]

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

def clients_stats_old(type, jid, nick, text):
	text = reduce_spaces_all(text).lower().split()
	if text:
		is_short = 'short' in text
		is_os = 'os' in text
		is_global = 'global' in text or 'total' in text or 'all' in text
		if is_short or is_global or is_os:
			for t in ['all','total','global','short','os']:
				if t in text: text.remove(t)
		if text: match = '%%\r%%%s%%' % ' '.join(text)
		else: match = '%\r%'
	else:
		match = '%\r%'
		is_short = is_global = is_os = False
	if is_global: req,par = 'select message from age where message ilike %s',(match,)
	else: req,par = 'select message from age where room=%s and message ilike %s',(jid,match)
	st = cur_execute_fetchall(req,par)
	if st:
		ns = {}
		et = L('Error! %s','%s/%s'%(jid,nick))%''
		for t in st:
			if is_os:
				k = t[0].split('\r',1)[1].split(' // ',1)
				if len(k) == 2: k = k[1]
				else: k = ''
			else: k = t[0].split('\r',1)[1].split(' // ',1)[0]
			k = k.replace('\r','[LF]').replace('\n','[CR]').replace('\t','[TAB]')
			if is_short and k: k = k.split()[0]
			if not k or k == 'None': k = 'Unknown'
			if not k.startswith(et.strip()):
				if ns.has_key(k): ns[k] += 1
				else: ns[k] = 1
		ns = [(ns[t],t) for t in ns.keys()]
		ns.sort(reverse=True)
		msg = L('Client statistic:%s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join(['%s. %s\t- %s' % (ns.index(t)+1,t[1],t[0]) for t in ns[:10]])
	else: msg = L('Clients statistic not available.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def clients_stats(type, jid, nick, text):
	text2 = text.split(' ')
	text = text.lower().split(' ')
	match = '%'
	if text:
		is_short = 'short' in text
		is_os = 'os' in text
		is_user = 'user' in text
		is_global = 'global' in text or 'total' in text or 'all' in text
		if is_short or is_global or is_os or is_user:
			for t in ['all','total','global','short','os','user']:
				if t in text: text.remove(t)
				for t2 in text2:
					if t2.lower() == t.lower():
						text2.remove(t2)
						break
		if is_user:
			if text2:
				cnick = text = ' '.join(text2)
				for t in megabase:
					if t[0] == jid and t[1] in text:
						match,cnick = '%%%s%%' % reduce_spaces_all(text.replace(t[1],'')),t[1]
						break
			else: cnick = nick
			cjid = getRoom(get_level(jid,cnick)[1])
			if cjid == 'None':
				send_msg(type, jid, nick, L('I could be wrong, but %s not is here...','%s/%s'%(jid,nick)) % cnick)
				return
		elif text: match = '%%%s%%' % reduce_spaces_all(' '.join(text))
	else: is_short = is_global = is_os = is_user = False

	if is_global:
		if is_user: req,par = 'select client,version,os from versions where jid=%s and (client ilike %s or version ilike %s or os ilike %s)',(cjid,match,match,match)
		else: req,par = 'select client,version,os from versions where client ilike %s or version ilike %s or os ilike %s',(match,match,match)
	elif is_user: req,par = 'select client,version,os from versions where room=%s and jid=%s',(jid,cjid)
	else: req,par = 'select client,version,os from versions where room=%s and (client ilike %s or version ilike %s or os ilike %s)',(jid,match,match,match)
	st = cur_execute_fetchall(req,par)
	if st:
		ns = {}
		for t in st:
			if is_os:
				k = t[2]
				if k and k.strip() and is_short:
					if '/' in k: k = k.split('/')[0]
					elif k.lower().startswith('microsoft') or k.lower().startswith('(c)') or k.startswith(u'©'): k = k.split()[1]
					else: k = k.split()[0]
					if '=' in k: k = k.split('=')[1]
			else:
				if is_short: k = t[0]
				else: k = '%s %s' % (t[:2])
			if not k or k == 'None': k = 'Unknown'
			k = k.replace('\r','[LF]').replace('\n','[CR]').replace('\t','[TAB]')
			if ns.has_key(k): ns[k] += 1
			else: ns[k] = 1
		ns = [(ns[t],t) for t in ns.keys()]
		ns.sort(reverse=True)
		if is_user:
			if is_short: msg = L('Client statistic:%s','%s/%s'%(jid,nick)) % ' %s' % ', '.join(['%s (%s)' % (t[1],t[0]) for t in ns])
			else: msg = L('Client statistic:%s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join([t[1] for t in ns])
		else: msg = L('Client statistic:%s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join(['%s. %s\t- %s' % (ns.index(t)+1,t[1],t[0]) for t in ns[:10]])
	else: msg = L('Clients statistic not available.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(4, 'clients_old', clients_stats_old, 2, 'Show clients statistic when available.\nclients [total|global|all[ short][ os]] [string]'),
		   (4, 'clients', clients_stats, 2, 'Show clients statistic when available.\nclients [total|global|all[ short][ os]] [string]')]

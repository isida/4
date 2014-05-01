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

visitors_list = {}
visitors_list_lock = False

# -------------- affiliation -----------------

def global_ban(type, jid, nick, text):
	text = text.lower()
	hroom = getRoom(jid)
	al = get_level(jid,nick)[0]
	if al == 9: af = 'owner'
	else: af = get_affiliation(jid,nick)
	if af != 'owner': msg = L('This command available only for conference owner!','%s/%s'%(jid,nick))
	elif text == 'show' and al == 9:
		ir = cur_execute_fetchone('select * from ignore_ban;')
		if len(ir): msg = '%s\n%s' % (L('Global ban is off in:','%s/%s'%(jid,nick)),'\n'.join([t[0] for t in ir]))
		else: msg = L('Global ban enable without limits!','%s/%s'%(jid,nick))
	elif text == 'del' and af == 'owner':
		if cur_execute_fetchone('select * from ignore_ban where room=%s' % (hroom,)): msg = L('Conference %s already deleted from global ban list!','%s/%s'%(jid,nick)) % hroom
		else:
			cur_execute('insert inro ignore_ban values (%s)' % (hroom,))
			msg = L('Conference %s has been deleted from global ban list!','%s/%s'%(jid,nick)) % hroom
	elif text == 'add' and af == 'owner':
		if cur_execute_fetchone('select * from ignore_ban where room=%s' % (hroom,)):
			cur_execute('delete from ignore_ban where room=%s' % (hroom,))
			msg = L('Conference %s has been added from global ban list!','%s/%s'%(jid,nick)) % hroom
		else: msg = L('Conference %s already exist in global ban list!','%s/%s'%(jid,nick)) % hroom
	else:
		if al == 9:
			if cur_execute_fetchone('select * from ignore_ban where room=%s' % (hroom,)): msg = L('Your conference will be ignored for global ban!','%s/%s'%(jid,nick))
			elif '@' not in text or '.' not in text: msg = L('I need jid!','%s/%s'%(jid,nick))
			else:
				reason = L('banned global by %s from %s','%s/%s'%(jid,nick)) % (nick, jid)
				br = [t[0] for t in cur_execute_fetchall("select room from conference where split_part(room,'/',1) not in (select room from ignore_ban as igb);")]
				for tmp in br:
					i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':getRoom(tmp)}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':unicode(text)},[xmpp.Node('reason',{},reason)])])])
					sender(i)
					time.sleep(0.1)
				msg = L('jid %s has been banned in %s conferences.','%s/%s'%(jid,nick)) % (text, len(br))
		else: msg = L('Command temporary blocked!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def muc_tempo_ban(type, jid, nick, text):
	text,mute = text.strip().split('\n'),False
	if text:
		cmd, par = text[0].lower().split(' ',1) if ' ' in text[0] else (text[0].lower().split(' ',1)[0],'')
		if cmd == 'show':
			if not par: par = '%'
			tb = cur_execute_fetchall('select jid,time from tmp_ban where room=%s and jid ilike %s',(jid,par))
			if tb: msg = L('Found: %s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join([['%s\t%s' % (ub[0],un_unix(ub[1]-int(time.time()),'%s/%s'%(jid,nick))),'%s\t< %s' % (ub[0],un_unix(GT('schedule_time'),'%s/%s'%(jid,nick)))][ub[1] < int(time.time())] for ub in tb])
			else: msg = L('Not found.','%s/%s'%(jid,nick))

		elif cmd == 'del':
			if par:
				tb = cur_execute_fetchall('select jid,time from tmp_ban where room=%s and jid ilike %s',(jid,par))
				if tb:
					msg = L('Removed: %s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join([['%s\t%s' % (ub[0],un_unix(ub[1]-int(time.time()),'%s/%s'%(jid,nick))),'%s\t< %s' % (ub[0],un_unix(GT('schedule_time'),'%s/%s'%(jid,nick)))][ub[1] < int(time.time())] for ub in tb])
					for ub in tb: sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[0]))},[])])]))
					cur_execute('delete from tmp_ban where room=%s and jid ilike %s',(jid,par))
				else: msg = L('Not found.','%s/%s'%(jid,nick))
			else: msg = L('What?','%s/%s'%(jid,nick))

		else:
			try: ban_time = int(text[1][:-1]) * {'s':1, 'm':60, 'h':3600, 'd':86400}[text[1][-1].lower()]
			except: ban_time = None
			if ban_time:
				reason = ' '.join(text[2:])
				if not reason: reason = L('No reason!','%s/%s'%(jid,nick))
				reason = L('ban on %s since %s because: %s','%s/%s'%(jid,nick)) % (un_unix(ban_time,'%s/%s'%(jid,nick)), timeadd(tuple(time.localtime())), reason)
				who,msg = text[0],L('done','%s/%s'%(jid,nick))
				try: whojid = getRoom([t[4] for t in megabase if t[0]==jid and t[1]==who][0])
				except: whojid = None
				if not whojid:
					fnd = cur_execute_fetchall('select jid from age where room=%s and (nick=%s or jid=%s) group by jid',(jid,who,who))
					if len(fnd) == 1: whojid = getRoom(fnd[0][0])
					elif len(fnd) > 1: msg = L('I seen different people with this nick!','%s/%s'%(jid,nick))
					else: msg,whojid = L('I don\'n know %s, and use as is!','%s/%s'%(jid,nick)) % who,who
				if whojid:
					sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':unicode(whojid)},[xmpp.Node('reason',{},reason)])])]))
					was_banned = cur_execute_fetchone('select time from tmp_ban where room=%s and jid=%s;',(jid,whojid))
					if was_banned:
						cur_execute('delete from tmp_ban where room=%s and jid=%s;',(jid,whojid))
						ban_tm = was_banned[0]-int(time.time())
						if ban_tm > 0: ban_nm = L('old ban time is %s','%s/%s'%(jid,nick)) % un_unix(ban_tm,'%s/%s'%(jid,nick))
						else: ban_nm = L('just passed!','%s/%s'%(jid,nick))
						msg = L('Updated: %s','%s/%s'%(jid,nick)) % ban_nm
					cur_execute('insert into tmp_ban values (%s,%s,%s)',(jid,whojid,ban_time+int(time.time())))
				if who == nick: mute = True
			else: msg = L('Time format error!','%s/%s'%(jid,nick))
	else: msg = L('What?','%s/%s'%(jid,nick))

	if not mute: send_msg(type, jid, nick, msg)

def muc_ban(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'outcast',0)
def muc_banjid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'outcast',1)
def muc_none(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'none',0)
def muc_nonejid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'none',1)
def muc_member(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'member',0)
def muc_memberjid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'member',1)

def muc_affiliation(type, jid, nick, text, aff, is_jid):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner':
		if is_start: return
		else: send_msg(type, jid, nick, L('Command is locked!','%s/%s'%(jid,nick)))
	elif len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		whojid = [unicode(get_level(jid,who)[1]),who][is_jid]
		if whojid != 'None': sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':aff, 'jid':whojid},reason)])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s','%s/%s'%(jid,nick)) % who)
	else: send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))

def muc_ban_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'outcast')
def muc_none_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'none')
def muc_member_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'member')

def muc_affiliation_past(type, jid, nick, text, aff):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner':
		if is_start: return
		else: msg, text = L('Command is locked!','%s/%s'%(jid,nick)), ''
	else: msg = L('What?','%s/%s'%(jid,nick))
	if len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		fnd = cur_execute_fetchall('select jid from age where room=%s and (nick=%s or jid=%s) group by jid',(jid,who,who))
		if len(fnd) == 1: msg, whojid = L('done','%s/%s'%(jid,nick)), getRoom(unicode(fnd[0][0]))
		elif len(fnd) > 1:
			whojid = getRoom(get_level(jid,who)[1])
			if whojid != 'None': msg = L('done','%s/%s'%(jid,nick))
			else: msg, skip = L('I seen some peoples with this nick. Get more info!','%s/%s'%(jid,nick)), True
		else:
			msg = L('I don\'n know %s, and use as is!','%s/%s'%(jid,nick)) % who
			whojid = who
	else: skip = True
	if skip: send_msg(type, jid, nick, msg)
	else:
		i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':aff, 'jid':unicode(whojid)},reason)])])
		sender(i)
		send_msg(type, jid, nick, msg)

def muc_kick(type, jid, nick, text): muc_role(type, jid, nick, text, 'none',1)
def muc_participant(type, jid, nick, text): muc_role(type, jid, nick, text, 'participant',1)
def muc_visitor(type, jid, nick, text): muc_role(type, jid, nick, text, 'visitor',1)
def muc_moderator(type, jid, nick, text): muc_role(type, jid, nick, text, 'moderator',1)

def muc_role(type, jid, nick, text, role, unused):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner':
		if is_start: return
		else: send_msg(type, jid, nick, L('Command is locked!','%s/%s'%(jid,nick)))
	elif len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		whojid = unicode(get_level(jid,who)[1])
		if whojid != 'None': sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':role, 'nick':who},reason)])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s','%s/%s'%(jid,nick)) % who)
	else: send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))

def check_unban():
	tt = int(time.time())
	ul = cur_execute_fetchall('select room,jid from tmp_ban where time<%s;',(tt,))
	if ul:
		for t in ul: sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':t[0]}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'none', 'jid':getRoom(unicode(t[1]))},[])])]))
		cur_execute('delete from tmp_ban where time<%s;',(tt,))

def visitors_list_lock_wait():
	while visitors_list_lock: time.sleep(0.05)
	return True

def check_visitor():
	global visitors_list, visitors_list_lock
	visitors_list_lock = visitors_list_lock_wait()
	ITT = int(time.time())
	for t in visitors_list:
		room = t.split('/')[0]
		VISITOR_ACT = get_config(getRoom(room),'visitor_action')
		if VISITOR_ACT != 'off' and ITT > visitors_list[t]:
			reason = [xmpp.Node('reason',{},L('Too long was without voice!',t))]
			if VISITOR_ACT == 'kick': sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':room}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':'none', 'nick':t.split('/',1)[1]},reason)])]))
			else: sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':room}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':get_jid_by_nick(t.split('/',1))},reason)])]))
	visitors_list_lock = False

def visitor_presence(room,jid,nick,type,mass):
	global visitors_list, visitors_list_lock
	if getRoom(jid) == getRoom(Settings['jid']): return
	if type == 'error': return
	elif type == 'unavailable':
		visitors_list_lock = visitors_list_lock_wait()
		try: visitors_list.pop('%s/%s' % (room,nick))
		except: pass
		visitors_list_lock = False
	if mass[1] == 'visitor':
		visitors_list_lock = visitors_list_lock_wait()
		visitors_list['%s/%s' % (room,nick)] = int(time.time()) + get_config_int(getRoom(room),'visitor_action_time')	
		visitors_list_lock = False

global execute, timer, presence_control

timer = [check_unban,check_visitor]
presence_control = [visitor_presence]

execute = [(7, 'ban_past', muc_ban_past, 2, 'Ban user.'),
	   (7, 'ban', muc_ban, 2, 'Ban user.'),
	   (7, 'banjid', muc_banjid, 2, 'Ban user by jid.'),
	   (7, 'unban', muc_none, 2, 'Unban user.'),
	   (7, 'unbanjid', muc_nonejid, 2, 'Unban user by jid.'),
	   (7, 'tban', muc_tempo_ban, 2, 'Temporary ban.\ntban show|del [jid] - show/del temporary bans\ntban nick\ntimeD|H|M|S\nreason - ban nick for time because reason.'),
	   (7, 'none_past', muc_none_past, 2, 'Remove user affiliation.'),
	   (7, 'none', muc_none, 2, 'Remove user affiliation.'),
	   (7, 'nonejid', muc_nonejid, 2, 'Remove user affiliation.'),
	   (7, 'member_past', muc_member_past, 2, 'Get member affiliation.'),
	   (7, 'member', muc_member, 2, 'Get member affiliation.'),
	   (7, 'memberjid', muc_memberjid, 2, 'Get member affiliation.'),
	   (7, 'kick', muc_kick, 2, 'Kick user.'),
	   (7, 'participant', muc_participant, 2, 'Change role to participant.'),
	   (7, 'visitor', muc_visitor, 2, 'Revoke voice.'),
	   (7, 'moderator', muc_moderator, 2, 'Grant moderator.'),
	   (8, 'global_ban', global_ban, 2, 'Global ban. Available only for confernce owner.\nglobal_ban del - remove conference from banlist,\nglobal_ban add - add conference into banlist,\nglobal_ban <jid> - ban jid in all rooms, where bot is admin.')]

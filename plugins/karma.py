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

last_karma = {}

def karma(type, jid, nick, text):
	arg = text.split(' ',1)
	try: arg1 = arg[1]
	except: arg1 = None
	a0l = arg[0].lower()

	karma_comm = {'show':		[karma_show,		(jid, nick, arg1)],
				  'top+':		[karma_top,			(jid, nick, arg1, None)],
				  'top-':		[karma_top,			(jid, nick, arg1, True)],
				  'set':		[karma_set,			(jid, nick, arg1)],
				  'clear':		[karma_clear,		(jid, nick, arg1)]}

	if karma_comm.has_key(a0l): msg = karma_comm[a0l][0](*karma_comm[a0l][1])
	else: msg = karma_show(jid, nick, text)
	send_msg(type, jid, nick, msg)

def karma_top(jid, nick, text, order):
	try: lim = int(text)
	except: lim = GT('karma_show_default_limit')
	if lim < 1: lim = 1
	elif lim > GT('karma_show_max_limit'): lim = GT('karma_show_max_limit')
	if order: stat = cur_execute_fetchall('select jid,karma from karma where room=%s order by karma',(jid,))
	else: stat = cur_execute_fetchall('select jid,karma from karma where room=%s order by -karma',(jid,))
	if stat == None: return L('In this room karma is not changed!','%s/%s'%(jid,nick))
	msg, cnt = '', 1
	for tmp in stat:
		tmp2 = get_nick_by_jid(jid, tmp[0])
		if tmp2:
			msg += '\n%s. %s\t%s' % (cnt,tmp2,karma_val(int(tmp[1])))
			cnt += 1
		if cnt > lim: break
	if len(msg): return L('Top karma: %s','%s/%s'%(jid,nick)) % msg
	else: return L('Karma for members is present not changed!','%s/%s'%(jid,nick))

def karma_size_wrong(room):
	k_size = int(config_prefs['karma_limit_size'][3])
	put_config(jid,'karma_limit_size',k_size)
	return k_size

def karma_get_limit(room,nick):
	room = getRoom(room)
	(acclvl, jid) = get_level(room,nick)
	if acclvl >= 7: return -1,-1
	k_log = cur_execute_fetchone('select log from karma_limits where room=%s and jid=%s',(room,getRoom(jid)))
	k_size = get_config(room,'karma_limit_size')
	if ''.join(re.findall('[-0-9, []]*', k_size)) != k_size: k_size = karma_size_wrong(room)
	if len(json.loads(k_size)) != 2: k_size = karma_size_wrong(room)
	k_size = json.loads(k_size)
	k_limit = [k_size[0],k_size[1]][acclvl >= 4]
	k_val = k_limit
	if k_log:
		k_log = json.loads(k_log[0])
		for tmp in k_log:
			if (time.time() - tmp) < 86400: k_val -= 1
		k_log.sort()
	else: k_log = [0]
	return k_val, k_limit, k_log[0]

def karma_show(jid, nick, text):
	if text == None or text == '' or text == nick: text, atext = nick, L('Your','%s/%s'%(jid,nick))
	else: atext = text
	karmajid = getRoom(get_level(jid,text)[1])
	if karmajid == 'None': return L('I\'m not sure, but %s not is here.','%s/%s'%(jid,nick)) % atext
	else:
		lim_text = ''
		if get_config(getRoom(jid),'karma_limit'):
			k_val = karma_get_limit(jid,text)[0]
			if k_val >= 0: lim_text = '. ' + L('Karma limit is %s','%s/%s'%(jid,nick)) % k_val
		stat = cur_execute_fetchone('select karma from karma where room=%s and jid=%s',(jid,karmajid))
		if stat == None: return L('%s have a clear karma','%s/%s'%(jid,nick)) % atext + lim_text
		else: return L('%s karma is %s','%s/%s'%(jid,nick)) % (atext, karma_val(int(stat[0]))) + lim_text

def karma_set(jid, nick, text):
	if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(jid,'karma')): return
	k_acc = get_level(jid,nick)[0]
	try:
		if '\n' in text: text,val = text.split('\n',1)
		else: text,val = text.split(' ',1)
		if k_acc >= 9:
			val = int(val)
			jid, karmajid = getRoom(jid), getRoom(get_level(jid,text)[1])
			if karmajid == getRoom(selfjid): return
			elif karmajid == 'None': return L('You can\'t change karma in outdoor conference!','%s/%s'%(jid,nick))
			else:
				cur_execute('delete from karma where room=%s and jid=%s',(jid,karmajid))
				cur_execute('insert into karma values (%s,%s,%s)',(jid,karmajid,val))
				val = karma_val(val)
				return L('You changes %s\'s karma to %s','%s/%s'%(jid,nick)) % (text,val)
		else: return L('You can\'t change karma!','%s/%s'%(jid,nick))
	except: return L('incorrect digital parameter','%s/%s'%(jid,nick)).capitalize()

def karma_clear(jid, nick, text):
	if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(jid,'karma')): return
	k_acc = get_level(jid,nick)[0]
	if k_acc >= 9:
		if '\n' in text: (param,text) = text.split('\n',1)
		else: param = ''
		jid, karmajid = getRoom(jid), getRoom(get_level(jid,text)[1])
		if karmajid == getRoom(selfjid): return
		elif karmajid == 'None': return L('You can\'t change karma in outdoor conference!','%s/%s'%(jid,nick))
		else:
			if param in ['','all','karma','limits']:
				if param in ['','all','karma']: cur_execute('delete from karma where room=%s and jid=%s',(jid,karmajid))
				if param in ['all','limits']: cur_execute('delete from karma_limits where room=%s and jid=%s',(jid,karmajid))
				return L('You clear karma for %s','%s/%s'%(jid,nick)) % text
			else: return L('Wrong arguments!','%s/%s'%(jid,nick))
	else: return L('You can\'t change karma!','%s/%s'%(jid,nick))

def karma_get_access(room,jid):
	stat = cur_execute_fetchone('select karma from karma where room=%s and jid=%s',(room,jid))
	if stat == None: return None
	if int(stat[0]) < GT('karma_limit'): return None
	return True

def karma_val(val): return ['%+2d' % val,'0'][val==0]

def karma_correct(room):
	def karma_correct_diff(vm,ac):
		lim_up = [GT('karma_discret_lim_up')]
		lim_dn = [GT('karma_discret_lim_dn')]
		kd,rs = GT('karma_discret'),[]
		def validate_mass(m):
			for t in range(0,len(m)-1):
				if abs(m[t]-m[t+1]) < kd or m[t] >= m[t+1]: return False
			return True
		def karma_blur_mass(vm):
			vm = lim_dn + vm + lim_up
			nm = []
			for t in range(0,len(vm)-2): nm.append(int((vm[t]+vm[t+1]+vm[t+2])/3))
			return nm
		while not validate_mass(vm): vm = karma_blur_mass(vm)
		for t in range(0,len(ac)): rs.append([vm[t],ac[t]])
		return rs
	tm,ac,vm,nm = config_group_karma[2],[],[],[]
	for t in tm:
		df = re.findall(r'karma_action_[0-9](.*)',t)
		if df:
			ac += df
			tvm = get_config_int(room,t)
			vm.append(tvm)
			nm.append(t)
	vm = karma_correct_diff(vm,ac)
	for t in range(0,len(nm)): put_config(room,nm[t],str(vm[t][0]))
	return vm

def karma_action_do(room,text,action):
	nick = getResourse(cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%room,))[0])
	action = action.replace('ban','outcast')
	act = {'outcast':muc_affiliation,'none':muc_affiliation,'member':muc_affiliation,
		   'kick':muc_role,'participant':muc_role,'visitor':muc_role,'moderator':muc_role}
	act[action]('chat',room,nick,'%s\n%s' % (text,get_config(room,'karma_action_reason')),action.replace('kick','none'),0)

def karma_change(room,jid,nick,type,text,value):
	global last_karma
	if type == 'chat': msg = L('You can\'t change karma in private!','%s/%s'%(room,nick))
	else:
		last_karma_text = last_karma.pop('%s/%s' % (room,jid), None)
		if last_karma_text:
			karma_text, karma_count = last_karma_text
			last_karma['%s/%s' % (room,jid)] = (karma_text, karma_count + 1)
			if karma_text == text and karma_count >= 2: return
		else: last_karma['%s/%s' % (room,jid)] = (text, 1)
		if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(room,'karma')): return
		if ': ' in text: (text,other) = text.split(': ',1)
		elif ', ' in text: (text,other) = text.split(', ',1)
		else: return
		if len(other) > 2 and get_config(getRoom(room),'karma_hard'): return
		k_acc = get_level(room,nick)[0]
		if k_acc < 0: return
		if k_acc >= 4 or karma_get_access(room,getRoom(jid)):
			jid, karmajid = getRoom(jid), getRoom(get_level(room,text)[1])
			if karmajid == getRoom(selfjid): return
			elif karmajid == 'None': msg = L('You can\'t change karma in outdoor conference!','%s/%s'%(room,nick))
			elif karmajid == jid: msg = L('You can\'t change own karma!','%s/%s'%(room,nick))
			elif get_config(getRoom(jid),'karma_limit') and karma_get_limit(room,nick)[0] == 0: msg = L('Karma limit is %s','%s/%s'%(room,nick)) % L('over','%s/%s'%(room,nick)) + '. ' + L('Please wait: %s','%s/%s'%(room,nick)) % un_unix(int(86400-(time.time() - karma_get_limit(room,nick)[2])),'%s/%s'%(room,nick))
			else:
				stat = cur_execute_fetchone('select last from karma_commiters where room=%s and jid=%s and karmajid=%s',(room,jid,karmajid))
				karma_valid, karma_time = None, int(time.time())
				if stat == None: karma_valid = True
				elif karma_time - int(stat[0]) >= GT('karma_timeout')[k_acc]: karma_valid = True
				if karma_valid:
					if k_acc < 7:
						k_log = cur_execute_fetchone('select log from karma_limits where room=%s and jid=%s',(room,jid))
						k_size = get_config(room,'karma_limit_size')
						if ''.join(re.findall('[-0-9, []]*', k_size)) != k_size: k_size = karma_size_wrong(room)
						if len(json.loads(k_size)) != 2: k_size = karma_size_wrong(room)
						k_size = json.loads(k_size)
						k_limit = [k_size[0],k_size[1]][k_acc >= 4]
						k_val = k_limit
						if k_log:
							k_log = json.loads(k_log[0])
							for tmp in k_log:
								if time.time() - tmp < 86400: k_val -= 1
							k_log = str([karma_time] + k_log[:k_limit-1])
							cur_execute('update karma_limits set log=%s where room=%s and jid=%s',(k_log,room,jid))
						else: cur_execute('insert into karma_limits values (%s,%s,%s)',(room,jid,'[%s]' % karma_time))
					if stat: cur_execute('update karma_commiters set last=%s where room=%s and jid=%s and karmajid=%s',(karma_time,room,jid,karmajid))
					else: cur_execute('insert into karma_commiters values (%s,%s,%s,%s)',(room,jid,karmajid,karma_time))
					stat = cur_execute_fetchone('select karma from karma where room=%s and jid=%s',(room,karmajid))
					if stat:
						stat = stat[0]+value
						cur_execute('delete from karma where room=%s and jid=%s',(room,karmajid))
					else: stat = value
					cur_execute('insert into karma values (%s,%s,%s)',(room,karmajid,stat))
					msg = L('You changes %s\'s karma to %s. Next time to change across: %s','%s/%s'%(room,nick)) % (text,karma_val(stat),un_unix(GT('karma_timeout')[k_acc],'%s/%s'%(room,nick)))
					pprint('karma change in %s for %s to %s' % (room,text,stat),'green')
					am = None
					if get_config(room,'karma_action'):
						kmass = karma_correct(room)
						for t in kmass:
							if t[0] <= 0 and stat <= t[0]:
								am = (room,text,t[1])
								break
							elif t[0] > 0 and stat >= t[0]: am = (room,text,t[1])
						if am:
							karma_action_do(*am)
							pprint('karma action in %s for %s is %s' % am,'bright_green')
				else: msg = L('Time from last change %s\'s karma is very small. Please wait %s','%s/%s'%(room,nick)) % (text,un_unix(int(stat[0])+GT('karma_timeout')[k_acc]-karma_time,'%s/%s'%(room,nick)))
				if get_config(room,'karma_limit'):
					k_val = karma_get_limit(room,nick)[0]
					if k_val >= 0: msg += '. ' + L('Karma limit is %s','%s/%s'%(room,nick)) % [L('over','%s/%s'%(room,nick)), k_val][k_val > 0]
		else: msg = L('You can\'t change karma!','%s/%s'%(room,nick))
	send_msg(type, room, nick, msg)

def karma_check(room,jid,nick,type,text):
	if getRoom(jid) == getRoom(selfjid): return
	if len(unicode(text)) < 5: return
	while len(text) and text[-1:] == ' ': text = text[:-1]
	if text[-3:] == ' +1':
		karma_change(room,jid,nick,type,text,1)
		return True
	elif text[-3:] == ' -1':
		karma_change(room,jid,nick,type,text,-1)
		return True

def karma_clear_log(room,jid,nick,type,arr):
	global last_karma
	if type == 'unavailable': last_karma.pop('%s/%s' % (room,jid), None)

global execute, message_control,presence_control

presence_control = [karma_clear_log]

message_act_control = [karma_check]

execute = [(3, 'karma', karma, 2, 'Karma.\nkarma [show] nick\nkarma top+|- [count]\nFor change karma: nick: +1\nnick: -1')]

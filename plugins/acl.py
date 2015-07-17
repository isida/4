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

acl_acts = ['msg','prs','prs_change','prs_join','role','role_change','role_join','aff','aff_change','aff_join',
			'nick','nick_change','nick_join','all','all_change','all_join','jid','jidfull','res','age','ver','vcard']
acl_actions = ['show','del','clear'] + acl_acts

acl_ver_tmp = {}
acl_vcard_tmp = {}

acl_actions.sort()

def acl_show(jid,nick,text):
	a = cur_execute_fetchall('select * from acl where jid=%s and action ilike %s order by level,action',(jid,text))
	if len(a):
		msg = L('Acl:','%s/%s'%(jid,nick))
		for tmp in a:
			if text == '%': t4 = tmp[4].replace('\n',' // ')
			else: t4 = tmp[4].replace('\n','\n    ')
			if tmp[6] == 9:
				if tmp[5]: st,tp = '\n[%s] %s %s %s -> %s', (disp_time(tmp[5],'%s/%s'%(jid,nick)),) + tmp[1:4] + (t4,)
				else: st,tp = '\n%s %s %s -> %s', tmp[1:4] + (t4,)
			else:
				if tmp[5]: st,tp = '\n%s | [%s] %s %s %s -> %s', (L(unlevl[tmp[6]],'%s/%s'%(jid,nick)),disp_time(tmp[5],'%s/%s'%(jid,nick)),) + tmp[1:4] + (t4,)
				else: st,tp = '\n%s | %s %s %s -> %s', (L(unlevl[tmp[6]],'%s/%s'%(jid,nick)),) + tmp[1:4] + (t4,)
			msg += st % tp
	else: msg = L('Acl not found','%s/%s'%(jid,nick))
	return msg

def acl_add_del(jid,nick,text,flag):
	global conn
	time_mass,atime = {'s':1,'m':60,'h':3600,'d':86400,'w':604800,'M':2592000,'y':31536000},0
	silent,level = False,9
	try:
		while text[0][0] == '/':
			if text[0] == '/silent': silent = True
			else:
				try: atime = int(time.time()) + int(text[0][1:-1]) * time_mass[text[0][-1:]]
				except: return L('Time format error!','%s/%s'%(jid,nick))
			text = text[1:]
	except: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	if text[0].isdigit():
		level = int(text[0])
		if level <= 0: level = 9
		elif level > 9: level = 9
		text = text[1:]
	ttext = ' '.join(text)
	if operator.xor(ttext.count('${EXP}') <= 1,ttext.count('${/EXP}') <= 1) and flag: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	elif ttext.find('${EXP}',ttext.find('${/EXP}')) > 0 and flag: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	elif '${EXP}' in ttext and '${/EXP}' in ttext:
		try: re.compile(ttext.split('${EXP}',1)[1].split('${/EXP}',1)[0].replace('%20','\ ').replace('*','*?'))
		except: return L('Error in RegExp!','%s/%s'%(jid,nick))
	try:
		acl_cmd = text[0]
		text = text[1:]
	except: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	if not acl_cmd in acl_acts: msg = L('Items: %s','%s/%s'%(jid,nick)) % ', '.join(acl_acts)
	else:
		try:
			if text[0].lower() in ['sub','!sub','exp','!exp','cexp','!cexp','=','!=','<','>','<=','>=']: acl_sub_act,text = text[0].lower(),text[1:]
			else: acl_sub_act = '='
		except: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
		if acl_cmd != 'age' and acl_sub_act in ['<','>','<=','>=']: return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
		if acl_sub_act in ['=','!=','sub','!sub']: text[0] = text[0].replace('%20',' ')
		else: text[0] = text[0].replace('%20','\ ')
		if acl_cmd == 'age' and not text[0].isdigit(): return L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
		if acl_sub_act in ['exp','!exp','cexp','!cexp']:
			try: re.compile(text[0].replace('*','*?'))
			except: return L('Error in RegExp!','%s/%s'%(jid,nick))
		if flag and len(text) >= 2:
			no_command = True
			for tmp in comms:
				if tmp[1] == text[1]:
					no_command = False
					break
			if no_command: return L('Unknown command: %s','%s/%s'%(jid,nick)) % text[1]
		tmp = cur_execute_fetchall('select * from acl where jid=%s and action=%s and type=%s and text=%s and level=%s',(jid,acl_cmd, acl_sub_act, text[0], level))
		if tmp:
			cur_execute('delete from acl where jid=%s and action=%s and type=%s and text=%s and level=%s',(jid,acl_cmd, acl_sub_act, text[0], level))
			msg = [L('Removed:','%s/%s'%(jid,nick)),L('Updated:','%s/%s'%(jid,nick))][flag]
		else: msg = [L('Not found:','%s/%s'%(jid,nick)),L('Added:','%s/%s'%(jid,nick))][flag]
		if flag: cur_execute('insert into acl values (%s,%s,%s,%s,%s,%s,%s)', (jid, acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ '), atime, level))
		if level == 9:
			if atime: msg += ' [%s] %s %s %s -> %s' % (disp_time(atime,'%s/%s'%(jid,nick)),acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
			else: msg += ' %s %s %s -> %s' % (acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
		else:
			if atime: msg += ' %s | [%s] %s %s %s -> %s' % (L(unlevl[level],'%s/%s'%(jid,nick)), disp_time(atime,'%s/%s'%(jid,nick)),acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
			else: msg += ' %s | %s %s %s -> %s' % (L(unlevl[level],'%s/%s'%(jid,nick)), acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ ').replace('\n',' // '))
		if not reduce_spaces_all(msg).split('->',1)[1]: msg = msg.split('->',1)[0]
		if flag and acl_cmd != 'msg':
			mb = [t[1:] for t in megabase if t[0] == jid and getRoom(t[4]) != getRoom(Settings['jid'])]
			a = [(acl_cmd, acl_sub_act, text[0], ' '.join(text[1:]).replace('%20','\ '), 0, level)]
			was_joined = True
			for t in mb:
				room, realjid, nick = jid, t[3], t[0]
				mass = cur_execute_fetchone('select message from age where jid=%s and room=%s and nick=%s',(getRoom(realjid),room,nick))[0].split('\n',4)
				mass = (mass[4], mass[0], mass[1])
				acl_selector(a,room,realjid,nick,mass,was_joined)
	if silent: return L('done','%s/%s'%(jid,nick))
	else: return msg

def acl_add(jid,nick,text): return acl_add_del(jid,nick,text,True)

def acl_del(jid,nick,text): return acl_add_del(jid,nick,text,False)

def acl_clear(room,nick):
	if get_level(room,nick)[0] < 8: return L('You have no rights to do it!','%s/%s'%(room,nick))
	acl_back = cur_execute_fetchall('select * from acl where jid=%s',(room,))
	if acl_back:
		fname = back_folder % '%s_%s.acl' % (unicode(room),''.join(['%02d' % t for t in time.localtime()[:6]]))
		writefile(fname,json.dumps(acl_back))
	cur_execute('delete from acl where jid=%s',(room,))
	return L('ACL cleared. Removed %s action(s).','%s/%s'%(room,nick)) % len(acl_back)

def muc_acl(type, jid, nick, text):
	text = text.replace('\ ','%20').replace(' // ','\n').replace(' \/\/ ',' // ').split(' ')
	if len(text) >= 3 and text[2] == '->': text[2] = ''
	elif len(text) >= 4 and text[3] == '->': text[3] = ''
	elif text[0].isdigit() and len(text) >= 5 and text[4] == '->': text[4] = ''
	elif text[0].lower() == 'del' and len(text) >= 5 and text[4] == '->': text[4] = ''
	while '' in text: text.remove('')
	if len(text): acl_cmd = text[0]
	else: acl_cmd = '!'
	if not acl_cmd in acl_actions and acl_cmd[0] != '/' and not acl_cmd.isdigit(): msg = L('Items: %s','%s/%s'%(jid,nick)) % ', '.join(acl_actions)
	elif acl_cmd == 'clear': msg = acl_clear(jid,nick)
	elif acl_cmd == 'show':
		try: t = text[1]
		except: t = '%'
		msg = acl_show(jid,nick,t)
	elif acl_cmd == 'del': msg = acl_del(jid,nick,text[1:])
	else: msg = acl_add(jid,nick,text)
	send_msg(type, jid, nick, msg)

def acl_action(cmd,nick,jid,room,text):
	global last_command
	if len(last_command):
		if last_command[6] == Settings['jid']: last_command = []
	cmd = cmd.replace('${NICK}',nick).replace('${JID}',jid).replace('${SERVER}',getServer(jid))
	if text and '${EXP}' in cmd and '${/EXP}' in cmd:
		regex = cmd.split('${EXP}',1)[1].split('${/EXP}',1)[0]
		mt = re.findall(regex, text, re.S|re.I|re.U)
		if mt != []: txt = ''.join(mt[0])
		else: txt = ''
		cmd = cmd.split('${EXP}',1)[0] + txt + cmd.split('${/EXP}',1)[1]
	nowname = get_xnick(room)
	return com_parser(7, nowname, 'groupchat', room, nick, cmd, Settings['jid'])

def acl_message(room,jid,nick,type,text):
	global conn
	#if not no_comm: return
	lvl = get_level(room,nick)[0]
	if lvl < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	a = cur_execute_fetchall('select action,type,text,command,time,level from acl where jid=%s and (action=%s or action ilike %s) order by level',(room,'msg','all%'))
	no_comm = True
	if a:
		acl_ma = get_config(room,'acl_multiaction')
		for tmp in a:
			if tmp[5] == 9 or lvl == tmp[5]:
				if tmp[4] <= time.time() and tmp[4]: cur_execute('delete from acl where jid=%s and action=%s and type=%s and text=%s',(room,tmp[0],tmp[1],tmp[2]))
				was_match = False
				if tmp[1] in ['exp','!exp']:
					if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),text,re.S|re.I|re.U): was_match = True
					elif re.findall(tmp[2].replace('*','*?'),text,re.S|re.I|re.U): was_match = True
				elif tmp[1] in ['cexp','!cexp']:
					if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),text,re.S|re.U): was_match = True
					elif re.findall(tmp[2].replace('*','*?'),text,re.S|re.U): was_match = True
				elif tmp[1] in ['sub','!sub']:
					if tmp[1][0] == '!' and not tmp[2].lower() in text.lower(): was_match = True
					elif tmp[2].lower() in text.lower(): was_match = True
				elif tmp[1] in ['=','!=']:
					if tmp[1][0] == '!' and text.lower() != tmp[2].lower(): was_match = True
					elif text.lower() == tmp[2].lower(): was_match = True
				if was_match:
					no_comm = acl_action(tmp[3],nick,jid,room,text)
					if not acl_ma: break

	return not no_comm

def bool_compare(a,b,c):
	a,c = int(a),int(c)
	return (b == '=' and a == c)\
		or (b == '<' and a < c)\
		or (b == '>' and a > c)\
		or (b == '<=' and a >= c)\
		or (b == '>=' and a >= c)

def acl_presence(room,jid,nick,type,mass):
	global iq_request,acl_ver_tmp,acl_vcard_tmp
	#if get_level(room,nick)[0] < 0: return
	if getRoom(jid) == getRoom(Settings['jid']): return
	was_joined = not mass[7] or is_start
	if type == 'error': return
	elif type == 'unavailable':
		try: acl_ver_tmp.pop('%s/%s' % (room,nick))
		except: pass
		try: acl_vcard_tmp.pop('%s/%s' % (room,nick))
		except: pass
		return
	# actions only on joins
	#if was_joined: return
	a = cur_execute_fetchall('select action,type,text,command,time,level from acl where jid=%s and (action ilike %s or action ilike %s or action ilike %s or action ilike %s or action ilike %s or action ilike %s or action=%s or action=%s or action=%s or action=%s or action=%s) order by level',(room,'prs%','nick%','all%','role%','aff%','jid','jidfull','res','age','ver','vcard'))
	if a: acl_selector(a,room,jid,nick,mass,was_joined)

def acl_selector(a,room,jid,nick,mass,was_joined):
	global iq_request,acl_ver_tmp,acl_vcard_tmp
	lvl = get_level(room,nick)[0]
	for tmp in a:
		if (tmp[5] == 9 or lvl == tmp[5]) and tmp[0] == 'age':
			r_age = cur_execute_fetchone('select sum(%s-time+age) from age where room=%s and jid=%s',(int(time.time()),room,getRoom(jid)))[0]
			if not r_age: r_age = 0
			break

	r_ver,r_vcard = None,None

	for tmp in a:
		if (tmp[5] == 9 or lvl == tmp[5]) and tmp[0] == 'ver' and was_joined:
			try:
				r_ver = acl_ver_tmp['%s/%s' % (room,nick)]
				break
			except:
				iqid,who = get_id(), '%s/%s' % (room,nick)
				i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_VERSION},[])])
				iq_request[iqid]=(time.time(),acl_version_async,[a, nick, jid, room, mass[0], lvl],xmpp.NS_VERSION)
				sender(i)
				pprint('*** ACL version request for [%s] %s/%s' % (tmp[5],room,nick),'purple')
				break

	for tmp in a:
		if (tmp[5] == 9 or lvl == tmp[5]) and tmp[0] == 'vcard' and was_joined:
			try:
				r_vcard = acl_vcard_tmp['%s/%s' % (room,nick)]
				break
			except:
				iqid,who = get_id(), '%s/%s' % (room,nick)
				i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('vCard', {'xmlns': xmpp.NS_VCARD},[])])
				iq_request[iqid]=(time.time(),acl_vcard_async,[a, nick, jid, room, mass[0], lvl],xmpp.NS_VCARD)
				sender(i)
				pprint('*** ACL vcard request for [%s] %s/%s' % (tmp[5],room,nick),'purple')
				break

	acl_ma = get_config(room,'acl_multiaction')
	for tmp in a:
		if tmp[5] == 9 or lvl == tmp[5]:
			itm = ''
			if tmp[4] <= time.time() and tmp[4]: cur_execute('delete from acl where jid=%s and action=%s and type=%s and text=%s',(room,tmp[0],tmp[1],tmp[2]))
			if tmp[0].split('_')[0] == 'prs' and (('_join' in tmp[0] and was_joined) or ('_change' in tmp[0] and not was_joined) or ('_join' not in tmp[0] and '_change' not in tmp[0])): itm = mass[0]
			elif tmp[0].split('_')[0] == 'nick' and (('_join' in tmp[0] and was_joined) or ('_change' in tmp[0] and not was_joined) or ('_join' not in tmp[0] and '_change' not in tmp[0])): itm = nick
			elif tmp[0].split('_')[0] == 'role' and (('_join' in tmp[0] and was_joined) or ('_change' in tmp[0] and not was_joined) or ('_join' not in tmp[0] and '_change' not in tmp[0])): itm = mass[1]
			elif tmp[0].split('_')[0] == 'aff' and (('_join' in tmp[0] and was_joined) or ('_change' in tmp[0] and not was_joined) or ('_join' not in tmp[0] and '_change' not in tmp[0])): itm = mass[2]
			elif tmp[0].split('_')[0] == 'all' and (('_join' in tmp[0] and was_joined) or ('_change' in tmp[0] and not was_joined) or ('_join' not in tmp[0] and '_change' not in tmp[0])): itm = '|'.join((jid,nick,mass[0],mass[1],mass[2]))
			elif tmp[0] == 'jid' and was_joined: itm = getRoom(jid)
			elif tmp[0] == 'jidfull' and was_joined: itm = jid
			elif tmp[0] == 'res' and was_joined: itm = getResourse(jid)
			elif tmp[0] == 'ver' and was_joined and r_ver: itm = r_ver
			elif tmp[0] == 'vcard' and was_joined and r_vcard: itm = r_vcard
			elif tmp[0] == 'age' and was_joined and bool_compare(r_age,tmp[1],tmp[2]):
				acl_action(tmp[3],nick,jid,room,None)
				if not acl_ma: break
			if itm:
				was_match = False
				if tmp[1] in ['exp','!exp']:
					if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
					elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
				elif tmp[1] in ['cexp','!cexp']:
					if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
					elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
				elif tmp[1] in ['sub','!sub']:
					if tmp[1][0] == '!' and tmp[2].lower() not in itm.lower(): was_match = True
					elif tmp[2].lower() in itm.lower(): was_match = True
				elif tmp[1] in ['=','!=']:
					if tmp[1][0] == '!' and not (itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),mass[0].lower()))): was_match = True
					elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),mass[0].lower())): was_match = True
				if was_match:
					acl_action(tmp[3],nick,jid,room,None)
					if not acl_ma: break

def acl_version_async(a, nick, jid, room, mass, lvl, is_answ):
	global acl_ver_tmp
	itm = is_answ[1][0]
	acl_ver_tmp['%s/%s' % (room,nick)] = itm.replace('\r','[LF]').replace('\n','[CR]').replace('\t','[TAB]')
	for tmp in a:
		if tmp[0] == 'ver' and (tmp[5] == 9 or lvl == tmp[5]):
			was_match = False
			if tmp[1] in ['exp','!exp']:
				if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
				elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
			elif tmp[1] in ['cexp','!cexp']:
				if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
				elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
			elif tmp[1] in ['sub','!sub']:
				if tmp[1][0] == '!' and tmp[2].lower() not in itm.lower(): was_match = True
				elif tmp[2].lower() in itm.lower(): was_match = True
			elif tmp[1] in ['=','!=']:
				if tmp[1][0] == '!' and (itm.lower() != tmp[2].lower() or tmp[0] == 'all' and tmp[2].lower() not in (jid.lower(),nick.lower(),'\n'.join(mass).lower())): was_match = True
				elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),'\n'.join(mass).lower())): was_match = True
			if was_match: acl_action(tmp[3],nick,jid,room,None)

def acl_vcard_async(a, nick, jid, room, mass, lvl, is_answ):
	global acl_vcard_tmp
	try: vc,err = is_answ[1][1].getTag('vCard',namespace=xmpp.NS_VCARD),False
	except: vc,err = is_answ[1][0],True
	if not vc or unicode(vc) == '<vCard xmlns="vcard-temp" />': itm = 'empty'
	elif err: itm = vc[:VCARD_LIMIT_LONG]
	else:
		data = []
		for t in vc.getChildren():
			if t.getChildren():
				cm = []
				for r in t.getChildren():
					if r.getData(): cm.append(('%s.%s' % (t.getName(),r.getName()),unicode(r.getData())))
				data += cm
			elif t.getData(): data.append((t.getName(),t.getData()))
		if data:
			try:
				photo_size = sys.getsizeof(get_value_from_array2(data,'PHOTO.BINVAL').decode('base64'))
				photo_type = get_value_from_array2(data,'PHOTO.TYPE')
				data_photo = '%s, %s' % (photo_type,get_size_human(photo_size))
				data = [t for t in list(data) if t[0] not in ['PHOTO.BINVAL','PHOTO.TYPE']]
				data.append(('PHOTO',data_photo))
			except: pass
			data.sort()
			itm = '\n'.join(['%s:%s' % (t[0],t[1].replace('\r','[LF]').replace('\n','[CR]').replace('\t','[TAB]')) for t in data])
		else: itm = 'empty'

	acl_vcard_tmp['%s/%s' % (room,nick)] = itm
	for tmp in a:
		if tmp[0] == 'vcard' and (tmp[5] == 9 or lvl == tmp[5]):
			was_match = False
			if tmp[1] in ['exp','!exp']:
				if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
				elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.I|re.U): was_match = True
			elif tmp[1] in ['cexp','!cexp']:
				if tmp[1][0] == '!' and not re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
				elif re.findall(tmp[2].replace('*','*?'),itm,re.S|re.U): was_match = True
			elif tmp[1] in ['sub','!sub']:
				if tmp[1][0] == '!' and tmp[2].lower() not in itm.lower(): was_match = True
				elif tmp[2].lower() in itm.lower(): was_match = True
			elif tmp[1] in ['=','!=']:
				if tmp[1][0] == '!' and (itm.lower() != tmp[2].lower() or tmp[0] == 'all' and tmp[2].lower() not in (jid.lower(),nick.lower(),'\n'.join(mass).lower())): was_match = True
				elif itm.lower() == tmp[2].lower() or (tmp[0] == 'all' and tmp[2].lower() in (jid.lower(),nick.lower(),'\n'.join(mass).lower())): was_match = True
			if was_match: acl_action(tmp[3],nick,jid,room,None)

global execute, presence_control, message_act_control

presence_control = [acl_presence]
message_act_control = [acl_message]

execute = [(7, 'acl', muc_acl, 2, 'Actions list.\nacl show - show list\nacl del [/silent] item - remove item from list\nacl [/time] [/silent] msg|prs|role|aff|nick|jid|jidfull|res|age|ver|vcard|all [sub|exp|cexp] pattern command - execute command by condition\nallowed variables in commands: ${NICK}, ${JID}, ${SERVER}, ${EXP} and ${/EXP}\nsub = substring, exp = regular expression, cexp = case sensitive regular expression\ntime format is /number+identificator. s = sec, m = min, d = day, w = week, M = month, y = year. only one identificator allowed!')]

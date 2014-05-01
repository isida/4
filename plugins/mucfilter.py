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

muc_filter_fast_join = {}
muc_filter_last_notify = 0
muc_filter_events = []

def muc_pprint(*param):
	global muc_filter_events,muc_filter_last_notify
	pprint(*param)
	if GT('muc_filter_notify'):
		_notify_count = GT('muc_filter_notify_count')
		muc_filter_events = [time.time()] + muc_filter_events[:_notify_count-1]		
		if len(muc_filter_events) == _notify_count \
				and muc_filter_events[0] - muc_filter_events[-1] < GT('muc_filter_notify_peroid') \
				and muc_filter_last_notify + GT('muc_filter_notify_wait') < time.time():
			pprint('*** MUC-Filter notify event!')
			muc_filter_last_notify = time.time()
			muc_filter_events = []
			_jids = GT('muc_filter_notify_jids').split()
			for t in _jids:
				if t.strip(): send_msg('chat', t.strip(), '', 'MUC-Filter notify event!')

def muc_filter_set(iq,id,room,acclvl,query,towh,al):
	msg_xmpp = iq.getTag('query', namespace=xmpp.NS_MUC_FILTER)
	if msg_xmpp:
		msg,mute,mute_type,mute_room = get_tag(unicode(msg_xmpp),'query'),None,'groupchat',room
		jid = rss_replace(get_tag_item(msg,'message','from'))
		nick = rss_replace(unicode(get_nick_by_jid_res(room,jid)))
		rn = '%s/%s' % (room,nick)
		mute_reason = L('Warning! Your message are blocked by policy of room!',rn)
		if msg[:2] == '<m':
			if '<body>' in msg and '</body>' in msg:
				to_nick = getResourse(get_tag_item(msg,'message','to'))
				tojid = rss_replace(getRoom(get_level(room,to_nick)[1]))
				skip_owner = is_owner(jid)
				gr = getRoom(room)
				type = get_tag_item(msg,'message','type')
				if type == 'chat' and not skip_owner:
					tmp = cur_execute_fetchall('select * from muc_lock where room=%s and jid=%s', (room,tojid))
					if tmp:
						mute,mute_type,mute_room,mute_reason = True,'chat', '%s/%s' % (room,to_nick),L('Warning! This participant don\'t want to receive private messages!',rn)
						muc_pprint('MUC-Filter pmlock: %s/%s [%s] > %s: %s' % (room,nick,jid,to_nick,get_tag(msg,'body')),'brown')
				if skip_owner: pass
				elif get_config(gr,'muc_filter') and not mute:
					body = get_tag(msg,'body')

					# Mute all private messages
					if not mute and msg and type == 'chat' and get_config(gr,'muc_filter_mute_chat'):
						muc_pprint('MUC-Filter lock private: %s/%s [%s] > %s: %s' % (room,nick,jid,to_nick,get_tag(msg,'body')),'brown')
						try: cnt = mute_msg['%s|%s' % (gr,jid)]
						except: cnt = 1
						act = get_config(gr,'muc_filter_mute_repeat_action')
						if act != 'off':
							if cnt >= get_config_int(gr,'muc_filter_mute_repeat'):
								muc_pprint('MUC-Filter mute repeat action (%s): %s %s [%s]' % (act,gr,jid,cnt),'brown')
								msg = muc_filter_action(act,jid,room,L('Muted messages count overflow!',rn))
							else: mute_msg['%s|%s' % (gr,jid)] = cnt + 1
						mute,mute_type,mute_room,mute_reason = True,'chat', '%s/%s' % (room,to_nick),L('You couldn\'t send private messages! Don\'t repeat!',rn)

					# Mute all public messages
					if not mute and msg and type == 'groupchat' and get_config(gr,'muc_filter_mute_groupchat'):
						muc_pprint('MUC-Filter lock public: %s/%s [%s] > %s' % (room,nick,jid,get_tag(msg,'body')),'brown')
						try: cnt = mute_msg['%s|%s' % (gr,jid)]
						except: cnt = 1
						act = get_config(gr,'muc_filter_mute_repeat_action')
						if act != 'off':
							if cnt >= get_config_int(gr,'muc_filter_mute_repeat'):
								muc_pprint('MUC-Filter mute repeat action (%s): %s %s [%s]' % (act,gr,jid,cnt),'brown')
								msg = muc_filter_action(act,jid,room,L('Muted messages count overflow!',rn))
							else: mute_msg['%s|%s' % (gr,jid)] = cnt + 1
						mute,mute_reason = True,L('You couldn\'t send public messages! Don\'t repeat!',rn)
						
					# Mute newbie
					if not mute and msg and get_config(gr,'muc_filter_newbie'):
						in_base = cur_execute_fetchall('select sum(sum) from (select sum(age) from age where jid=%s and room=%s union all select %s-time from age where jid=%s and room=%s and status=0) as sum_age;',(getRoom(jid),gr,int(time.time()),getRoom(jid),gr))
						if not in_base: nmute = True
						else:
							newbie_time = get_config(gr,'muc_filter_newbie_time')
							if newbie_time.isdigit(): newbie_time = int(newbie_time)
							else: newbie_time = 60
							if in_base[0][0] < newbie_time: nmute = True
							else: nmute = False
						if nmute:
							try: cnt = newbie_msg['%s|%s' % (gr,jid)]
							except: cnt = 1
							muc_pprint('MUC-Filter mute newbie: %s %s [%s] %s' % (gr,jid,cnt,body),'brown')
							act = get_config(gr,'muc_filter_newbie_repeat_action')
							if act != 'off':
								if cnt >= get_config_int(gr,'muc_filter_newbie_repeat'):
									muc_pprint('MUC-Filter mute newbie repeat action (%s): %s %s [%s]' % (act,gr,jid,cnt),'brown')
									msg = muc_filter_action(act,jid,room,L('Messages count overflow from newbie!',rn))
								else: newbie_msg['%s|%s' % (gr,jid)] = cnt + 1
							mute,mute_reason = True,L('Your messages are blocked %ssec. after first join! Please, wait quiet!',rn) % newbie_time

					# New Line
					if not mute and msg and get_config(gr,'muc_filter_newline_msg') != 'off':
						act = get_config(gr,'muc_filter_newline_msg')
						try:
							nline_count = get_config_int(gr,'muc_filter_newline_msg_count')
							if not 2 <= nline_count <= 50: raise
						except:
							nline_count = int(config_prefs['muc_filter_newline_msg_count'][3])
							put_config(gr,'muc_filter_newline_msg_count',str(nline_count))
						if body.count('\n') >= nline_count:
							muc_pprint('MUC-Filter msg new line (%s): %s [%s] %s' % (act,jid,room,nick+'|'+body.replace('\n','[LF]')),'brown')
							if act == 'replace':
								body = body.replace('\n',' ')
								msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
							elif act == 'mute': mute,mute_reason = True,L('Blocked by content!',rn)
							else: msg = muc_filter_action(act,jid,room,L('Blocked by content!',rn))

					# Reduce spaces
					if not mute and msg and get_config(gr,'muc_filter_reduce_spaces_msg') and '  ' in body:
						muc_pprint('MUC-Filter msg reduce spaces: %s [%s] %s' % (jid,room,nick+'|'+body),'brown')
						body = reduce_spaces_all(body)
						msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)

					# AD-Block filter
					need_raw = True
					if not mute and msg and get_config(gr,'muc_filter_adblock') != 'off':
						f = []
						for reg in adblock_regexp:
							tmp = re.findall(reg,body,re.S|re.I|re.U)
							if tmp: f = f + tmp
						if f:
							act = get_config(gr,'muc_filter_adblock')
							need_raw = False
							muc_pprint('MUC-Filter msg adblock (%s): %s [%s] %s' % (act,jid,room,body),'brown')
							if act == 'replace':
								for tmp in f: body = body.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
								msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
							elif act == 'mute': mute,mute_reason = True,L('AD-Block!',rn)
							else: msg = muc_filter_action(act,jid,room,L('AD-Block!',rn))

					# Raw AD-Block filter
					if not mute and msg and need_raw and get_config(gr,'muc_filter_adblock_raw') != 'off':
						rawbody = match_for_raw(body,u'[a-zа-я0-9@.]*',gr)
						if rawbody:
							f = []
							for reg in adblock_regexp:
								tmp = re.findall(reg,rawbody,re.S|re.I|re.U)
								if tmp: f = f + tmp
							if f:
								act = get_config(gr,'muc_filter_adblock_raw')
								muc_pprint('MUC-Filter msg raw adblock (%s): %s [%s] %s' % (act,jid,room,body),'brown')
								if act == 'mute': mute,mute_reason = True,L('Raw AD-Block!',rn)
								else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!',rn))

					# Repeat message filter
					if not mute and msg and get_config(gr,'muc_filter_repeat') != 'off':
						grj = getRoom(jid)
						try: lm = last_msg_base[grj]
						except: lm = None
						if lm:
							rep_to = GT('muc_filter_repeat_time')
							try: lmt = last_msg_time_base[grj]
							except: lmt = 0
							if rep_to+lmt > time.time():
								action = False
								if body == lm: action = True
								elif lm in body:
									try: muc_repeat[grj] += 1
									except: muc_repeat[grj] = 1
									if muc_repeat[grj] >= (GT('muc_filter_repeat_count')-1): action = True
								else: muc_repeat[grj] = 0
								if action:
									act = get_config(gr,'muc_filter_repeat')
									muc_pprint('MUC-Filter msg repeat (%s): %s [%s] %s' % (act,jid,room,body),'brown')
									if act == 'mute': mute,mute_reason = True,L('Repeat message block!',rn)
									else: msg = muc_filter_action(act,jid,room,L('Repeat message block!',rn))
							else: muc_repeat[grj] = 0
						last_msg_base[grj] = body
						last_msg_time_base[grj] = time.time()

					# Match filter
					if not mute and msg and get_config(gr,'muc_filter_match') != 'off' and len(body) >= GT('muc_filter_match_view'):
						tbody,warn_match,warn_space = body.split(),0,0
						for tmp in tbody:
							cnt = 0
							for tmp2 in tbody:
								if tmp in tmp2: cnt += 1
							if cnt > GT('muc_filter_match_count'): warn_match += 1
							if not len(tmp): warn_space += 1
						if warn_match > GT('muc_filter_match_warning_match') or warn_space > GT('muc_filter_match_warning_space') or '\n'*GT('muc_filter_match_warning_nn') in body:
							act = get_config(gr,'muc_filter_match')
							muc_pprint('MUC-Filter msg matcher (%s): %s [%s] %s' % (act,jid,room,body),'brown')
							if act == 'mute': mute,mute_reason = True,L('Match message block!',rn)
							else: msg = muc_filter_action(act,jid,room,L('Match message block!',rn))

					# Censor filter
					need_raw = True
					if not mute and msg and get_config(gr,'muc_filter_censor') != 'off' and esc_min2(body) != to_censore(esc_min2(body),gr):
						act = get_config(gr,'muc_filter_censor')
						need_raw = False
						muc_pprint('MUC-Filter msg censor (%s): %s [%s] %s' % (act,jid,room,body),'brown')
						if act == 'replace': msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % esc_max2(to_censore(esc_min2(body),gr)))
						elif act == 'mute': mute,mute_reason = True,L('Blocked by censor!',rn)
						else: msg = muc_filter_action(act,jid,room,L('Blocked by censor!',rn))

					# Raw censor filter
					if not mute and msg and need_raw and get_config(gr,'muc_filter_censor_raw') != 'off':
						rawbody = match_for_raw(body,u'[a-zа-я0-9]*',gr)
						if rawbody and rawbody != to_censore(rawbody,gr):
							act = get_config(gr,'muc_filter_censor_raw')
							muc_pprint('MUC-Filter msg raw censor (%s): %s [%s] %s' % (act,jid,room,body),'brown')
							if act == 'mute': mute,mute_reason = True,L('Blocked by raw censor!',rn)
							else: msg = muc_filter_action(act,jid,room,L('Blocked by raw censor!',rn))

					# Large message filter
					if not mute and msg and get_config(gr,'muc_filter_large') != 'off' and len(body) > GT('muc_filter_large_message_size'):
						act = get_config(gr,'muc_filter_large')
						muc_pprint('MUC-Filter msg large message (%s): %s [%s] %s' % (act,jid,room,body),'brown')
						if act == 'paste' or act == 'truncate':
							url = paste_text(rss_replace(body),room,jid)
							if act == 'truncate': body = u'%s[…] %s' % (body[:GT('muc_filter_large_message_size')],url)
							else: body = L('Large message%s %s',rn) % (u'…',url)
							msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
						elif act == 'mute': mute,mute_reason = True,L('Large message block!',rn)
						else: msg = muc_filter_action(act,jid,room,L('Large message block!',rn))

				if mute: msg = unicode(xmpp.Message(to=jid,body=mute_reason,typ=mute_type,frm=mute_room))
			else: msg = None

		elif msg[:2] == '<p':
			jid = rss_replace(get_tag_item(msg,'presence','from'))
			gr = getRoom(room)
			if server_hash_list.has_key('%s/%s' % (gr,getServer(jid))) or server_hash_list.has_key('%s/%s' % (gr,getRoom(jid))):
				muc_pprint('MUC-Filter drop by previous ban: %s %s' % (room,jid),'brown')
				return True

			tojid = rss_replace(get_tag_item(msg,'presence','to'))
			if is_owner(jid): pass
			elif get_config(gr,'muc_filter') and not mute:
				show = ['online',get_tag(msg,'show')][int('<show>' in msg and '</show>' in msg)]
				if show not in ['chat','online','away','xa','dnd']: msg = msg.replace(get_tag_full(msg,'show'), '<show>online</show>')
				status = ['',get_tag(msg,'status')][int('<status>' in msg and '</status>' in msg)]
				nick = ['',tojid[tojid.find('/')+1:]]['/' in tojid]
				newjoin = True
				for tmp in megabase:
					if tmp[0] == gr and tmp[4] == jid:
						newjoin = False
						break

				# Drop presences without history
				if not mute and newjoin and get_config(gr,'muc_filter_history'):
					try: v = not sum([int(t) for t in msg_xmpp.getTag('presence').getTag('x',attrs={'xmlns':xmpp.NS_MUC}).getTag('history').getAttrs().values()])
					except: v = False
					if v:		
						muc_pprint('MUC-Filter history: %s/%s %s' % (gr,nick,jid),'brown')
						msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by history request!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						if get_config(gr,'muc_filter_history_ban'):
							muc_pprint('MUC-Filter history ban: %s/%s %s' % (gr,nick,jid),'brown')
							sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':jid},[xmpp.Node('reason',{},'Banned by empty history at %s' % timeadd(tuple(time.localtime())))])])]))

				# Fast join filter
				if not mute and newjoin and get_config(gr,'muc_filter_fast_join'):
					_itt = int(time.time())
					if muc_filter_fast_join.has_key(gr):
						_cnt = get_config_int(gr,'muc_filter_fast_join_count')
						_time = get_config_int(gr,'muc_filter_fast_join_time')
						muc_filter_fast_join[gr] = [_itt] + muc_filter_fast_join[gr][:_cnt-1]
						if len(muc_filter_fast_join[gr]) == _cnt and (muc_filter_fast_join[gr][0] - muc_filter_fast_join[gr][-1]) <= _time:
							muc_pprint('MUC-Filter fast join: %s/%s %s' % (gr,nick,jid),'brown')
							msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by fast join! Try again later!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
					else: muc_filter_fast_join[gr] = [_itt]

				# Validate items
				if not mute and msg and get_config(gr,'muc_filter_validate_action') != 'off':
					is_valid = True
					validate_limit = get_config_int(gr,'muc_filter_validate_count')
					validate_count = 0
					id_node,id_ver,id_hash = 'empty','empty','empty'
					if get_config(gr,'muc_filter_validate_nick'):
						iv,vc = validate_nick(nick,validate_limit)
						validate_count += vc
						if validate_count > validate_limit or not iv: is_valid = False
					if is_valid and get_config(gr,'muc_filter_validate_login'):
						iv,vc = validate_nick(getName(jid),validate_limit)
						validate_count += vc
						if validate_count > validate_limit or not iv: is_valid = False
					if is_valid and get_config(gr,'muc_filter_validate_resource'):
						iv,vc = validate_nick(getResourse(jid),validate_limit)
						validate_count += vc
						if validate_count > validate_limit or not iv: is_valid = False
					if is_valid:
						msg_xmpp_tmp = msg_xmpp.getTag('presence')
						caps_error = False
						try: id_node = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
						except: id_node,caps_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
						try: id_ver = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
						except: id_ver,caps_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
						try: id_hash = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("hash")').decode('utf-8')
						except: id_hash,caps_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("hash")'),True
						if caps_error: writefile(slog_folder % 'bad_stanza_%s.txt' % int(time.time()),unicode(msg_xmpp).encode('utf-8'))
						if get_config(gr,'muc_filter_validate_caps_node'):
							iv,vc = validate_nick(id_node,validate_limit)
							validate_count += vc
							if validate_count > validate_limit or not iv: is_valid = False
						if is_valid and get_config(gr,'muc_filter_validate_caps_version') and [len(id_ver),id_hash] in [[24,'md5'],[28,'sha-1']] and not id_ver.endswith('='):
							iv,vc = validate_nick(id_ver,validate_limit)
							validate_count += vc
							if validate_count > validate_limit or not iv: is_valid = False
					if not is_valid:
						act = get_config(gr,'muc_filter_validate_action')
						muc_pprint('MUC-Filter invalid items [%s]: %s/%s %s [%s] %s %s %s' % (act,gr,nick,jid,validate_count,id_node,id_ver,id_hash),'brown')
						msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by validation!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						tmp_server = getServer(jid)
						tmp2_server = '%s/%s' % (gr,tmp_server)
						if act == 'ban' and not server_hash_list.has_key('%s/%s' % (gr,getRoom(jid))):
							server_hash_list['%s/%s' % (gr,getRoom(jid))] = time.time()
							sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':jid},[xmpp.Node('reason',{},'Banned by invalid items at %s' % timeadd(tuple(time.localtime())))])])]))
						elif act == 'ban server' and tmp_server not in get_config(gr,'muc_filter_validate_ban_server_exception').split() and not server_hash_list.has_key(tmp2_server):
							server_hash_list[tmp2_server] = time.time()
							sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':tmp_server},[xmpp.Node('reason',{},'Banned by invalid items at %s' % timeadd(tuple(time.localtime())))])])]))
							tmp_notify = get_config(gr,'muc_filter_validate_ban_server_notify_jid')
							if len(tmp_notify):
								for tmp in tmp_notify.split():
									if len(tmp): send_msg('chat', tmp, '', L('Server %s was banned in %s',rn) % (tmp_server,gr))


				# Lock by caps
				if not mute and msg and get_config(gr,'muc_filter_caps_list') != 'off':
					caps_error = False
					if get_config(gr,'muc_filter_caps_list') == 'white': caps_list,caps_negate = 'muc_filter_caps_white',True
					else: caps_list,caps_negate = 'muc_filter_caps_black',False
					c_list = [t.strip() for t in get_config(gr,caps_list).split('\n') if t and not t.startswith('#')]
					if c_list:
						msg_xmpp_tmp = msg_xmpp.getTag('presence')
						id_node,id_ver = 'error!','error!'
						try: id_node = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
						except: id_node,caps_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
						try: id_ver = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
						except: id_ver,caps_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
						try:
							id_bmver = msg_xmpp_tmp.getAttr('ver').decode('utf-8')
							if id_bmver or id_bmver == '': id_bmver = '%s_' % id_bmver
							else: id_bmver = ''
						except: id_bmver = ''
						c_caps = '%s %s %s' % (id_node,id_ver,id_bmver)
						if caps_matcher(c_caps,c_list) ^ caps_negate:
							muc_pprint('MUC-Filter caps node lock (%s): %s/%s %s %s' % (['black','white'][caps_negate],gr,nick,jid,c_caps),'brown')
							msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by node lock!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
					if caps_error: writefile(slog_folder % 'bad_stanza_%s.txt' % int(time.time()),unicode(msg_xmpp).encode('utf-8'))

				# Hash lock
				if not mute and msg and get_config(gr,'muc_filter_deny_hash'):
					hashes_list = reduce_spaces_all(get_config(gr,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
					if hashes_list:
						msg_xmpp_tmp = msg_xmpp.getTag('presence')
						#id_node = id_ver = id_lang = id_photo = id_avatar = 'error!'
						id_ver,id_lang,id_photo,id_avatar = 'error!','error!','error!','error!'
						hash_error = False
						#try: id_node = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
						#except: id_node,hash_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
						try: id_ver = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
						except: id_ver,hash_error = get_eval_item(msg_xmpp_tmp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
						try:
							id_bmver = msg_xmpp_tmp.getAttr('ver').decode('utf-8')
							if id_bmver or id_bmver == '': id_bmver = '%s_' % id_bmver
							else: id_bmver = ''
						except: id_bmver = ''
						try: id_lang = get_eval_item(msg_xmpp_tmp,'getAttr("xml:lang")').decode('utf-8')
						except: id_lang,hash_error = get_eval_item(msg_xmpp_tmp,'getAttr("xml:lang")'),True
						try: id_photo = get_eval_item(msg_xmpp_tmp,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")').decode('utf-8')
						except: id_photo,hash_error = get_eval_item(msg_xmpp_tmp,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")'),True
						try: id_avatar = get_eval_item(msg_xmpp_tmp,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")').decode('utf-8')
						except: id_avatar,hash_error = get_eval_item(msg_xmpp_tmp,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")'),True

						hash_body = '<'.join([unicode(tmp) for tmp in id_avatar,id_photo,id_ver,id_bmver,id_lang]) + '<<'
						if hash_error:
							writefile(slog_folder % 'bad_stanza_%s.txt' % int(time.time()),unicode(msg_xmpp).encode('utf-8'))
							hash_body = parser(hash_body.decode('utf-8'))

						current_hash = hashlib.md5(hash_body.encode('utf-8')).digest().encode('base64').replace('\n','')
						hashes['%s/%s' % (gr,nick)] = current_hash
						if current_hash in hashes_list:
							muc_pprint('MUC-Filter hash lock: %s/%s %s %s' % (gr,nick,jid,current_hash),'brown')
							msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by hash lock!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
							tmp_server = getServer(jid)
							tmp2_server = '%s/%s' % (gr,tmp_server)
							if get_config(gr,'muc_filter_hash_ban_by_rejoin') and not server_hash.has_key(tmp2_server):
								if user_hash.has_key('%s/%s' % (gr,getRoom(jid))):
									user_hash.pop('%s/%s' % (gr,getRoom(jid)))
									sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':jid},[xmpp.Node('reason',{},'Banned by hash activity at %s' % timeadd(tuple(time.localtime())))])])]))
									muc_pprint('MUC-Filter ban by hash lock: %s/%s' % (gr,nick),'brown')
								else: user_hash['%s/%s' % (gr,getRoom(jid))] = time.time()
							if get_config(gr,'muc_filter_hash_ban_server_by_rejoin'):
								if tmp_server not in get_config(gr,'muc_filter_hash_ban_server_by_rejoin_exception').split():
									tmp_rejoins = get_config_int(gr,'muc_filter_hash_ban_server_by_rejoin_rejoins')
									if server_hash.has_key(tmp2_server): server_hash[tmp2_server] = [time.time()] + server_hash[tmp2_server][:tmp_rejoins-1]
									else: server_hash[tmp2_server] = [time.time()]
									tmp_times = server_hash[tmp2_server]
									if len(tmp_times) == tmp_rejoins and tmp_times[0]-tmp_times[-1] <= get_config_int(gr,'muc_filter_hash_ban_server_by_rejoin_timeout') and not server_hash_list.has_key(tmp2_server):
										server_hash_list[tmp2_server] = time.time()
										sender(xmpp.Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':tmp_server},[xmpp.Node('reason',{},'Banned by hash activity at %s' % timeadd(tuple(time.localtime())))])])]))
										muc_pprint('MUC-Filter server ban by hash lock: %s %s' % (gr,tmp_server),'brown')
										tmp_notify = get_config(gr,'muc_filter_hash_ban_server_by_rejoin_notify_jid')
										if len(tmp_notify):
											for tmp in tmp_notify.split():
												if len(tmp): send_msg('chat', tmp, '', L('Server %s was banned in %s',rn) % (tmp_server,gr))
						else: pprint('User hash: %s %s/%s %s' % (current_hash,gr,nick,jid),'white')

				# Blacklist
				if not mute and msg and get_config(gr,'muc_filter_blacklist'):
						bl_jid = get_config(gr,'muc_filter_blacklist_rules_jid')
						try: re.compile(bl_jid)
						except: bl_jid = None
						bl_nick = get_config(gr,'muc_filter_blacklist_rules_nick')
						try: re.compile(bl_nick)
						except: bl_nick = None
						is_bl = None
						if bl_jid and re.findall(bl_jid,jid,re.S|re.I|re.U): is_bl = True
						if not nick or (not is_bl and bl_nick and re.findall(bl_nick,nick,re.S|re.I|re.U)): is_bl = True
						if is_bl:
							muc_pprint('MUC-Filter blacklist: %s/%s %s' % (gr,nick,jid),'brown')
							msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by blacklist!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True

				# Whitelist
				if not mute and msg and get_config(gr,'muc_filter_whitelist') and newjoin:
					in_base = cur_execute_fetchone('select jid from age where room=%s and jid=%s',(gr,getRoom(jid)))
					if not in_base:
						muc_pprint('MUC-Filter whitelist: %s/%s %s' % (gr,nick,jid),'brown')
						msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by whitelist!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True

				# AD-Block filter
				need_raw = True
				if not mute and msg and get_config(gr,'muc_filter_adblock_prs') != 'off':
					fs,fn = [],[]
					for reg in adblock_regexp:
						tmps = [None,re.findall(reg,status,re.S|re.I|re.U)][status != '']
						tmpn = [None,re.findall(reg,nick,re.S|re.I|re.U)][nick != '']
						if tmps: fs = fs + tmps
						if tmpn: fn = fn + tmpn
					if fs:
						need_raw = False
						act = get_config(gr,'muc_filter_adblock_prs')
						muc_pprint('MUC-Filter adblock prs status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
						if act == 'replace':
							for tmp in fs: status = status.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
							msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status)
						elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('AD-Block!',rn))
					if fn and msg:
						need_raw = False
						act = get_config(gr,'muc_filter_adblock_prs')
						muc_pprint('MUC-Filter adblock prs nick (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
						if act == 'replace':
							for tmp in fn: nick = nick.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
							msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],nick))
						elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('AD-Block!',rn))

				# Raw AD-Block filter
				if not mute and msg and need_raw and get_config(gr,'muc_filter_adblock_prs_raw') != 'off':
					rawstatus = match_for_raw(status,u'[a-zа-я0-9@.]*',gr)
					rawnick = match_for_raw(nick,u'[a-zа-я0-9@.]*',gr)
					fs,fn = [],[]
					for reg in adblock_regexp:
						tmps = [None,re.findall(reg,rawstatus,re.S|re.I|re.U)][status != '']
						tmpn = [None,re.findall(reg,rawnick,re.S|re.I|re.U)][nick != '']
						if tmps: fs = fs + tmps
						if tmpn: fn = fn + tmpn
					if rawstatus and fs:
						act = get_config(gr,'muc_filter_adblock_prs_raw')
						muc_pprint('MUC-Filter raw adblock prs status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
						if newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!',rn))
					if rawnick and fn and msg:
						act = get_config(gr,'muc_filter_adblock_prs_raw')
						muc_pprint('MUC-Filter raw adblock prs nick (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
						if newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!',rn))

				# New Line
				if not mute and msg and get_config(gr,'muc_filter_newline') != 'off':
					act = get_config(gr,'muc_filter_newline')
					try:
						nline_count = get_config_int(gr,'muc_filter_newline_count')
						if not 2 <= nline_count <= 50: raise
					except:
						nline_count = int(config_prefs['muc_filter_newline_count'][3])
						put_config(gr,'muc_filter_newline_count',str(nline_count))
					if status.count('\n') >= nline_count:
						muc_pprint('MUC-Filter prs new line (%s): %s [%s] %s' % (act,jid,room,nick+'|'+status.replace('\n','[CR]').replace('\r','[LF]')),'brown')
						if act == 'replace':
							status = reduce_spaces_all(status.replace('\n',' ').replace('\r',' '))
							msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status)
						elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by content!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('Blocked by content!',rn))

				# Reduce spaces
				if not mute and msg and get_config(gr,'muc_filter_reduce_spaces_prs') and ('  ' in status or '  ' in nick):
					muc_pprint('MUC-Filter prs reduce spaces: %s [%s] %s' % (jid,room,nick+'|'+status),'brown')
					if len(status):
						status = reduce_spaces_all(status)
						msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status).replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],reduce_spaces_all(esc_max2(nick))))
					else: msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],reduce_spaces_all(esc_max2(nick))))

				# Censor filter
				need_raw = True
				if not mute and msg and get_config(gr,'muc_filter_censor_prs') != 'off' and '%s|%s' % (esc_min2(status),esc_min2(nick)) != to_censore('%s|%s' % (esc_min2(status),esc_min2(nick)),gr):
					act = get_config(gr,'muc_filter_censor_prs')
					need_raw = False
					muc_pprint('MUC-Filter prs censor (%s): %s [%s] %s' % (act,jid,room,'%s|%s' % (status,nick)),'brown')
					if act == 'replace':
						if len(status):
							status = esc_max2(to_censore(esc_min2(status),gr))
							msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status).replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],to_censore(esc_max2(nick),gr)))
						else: msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],to_censore(esc_max2(nick),gr)))
					elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by censor!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
					elif act == 'mute': msg,mute = None,True
					else: msg = muc_filter_action(act,jid,room,L('Blocked by censor!',rn))

				# Raw censor filter
				if not mute and msg and need_raw and get_config(gr,'muc_filter_censor_prs_raw') != 'off':
					rawstatus = match_for_raw(status,u'[a-zа-я0-9]*',gr)
					rawnick = match_for_raw(nick,u'[a-zа-я0-9]*',gr)
					if (rawstatus or rawnick) and '%s|%s' % (rawstatus,rawnick) != to_censore('%s|%s' % (rawstatus,rawnick),gr):
						act = get_config(gr,'muc_filter_censor_prs_raw')
						muc_pprint('MUC-Filter prs raw censor (%s): %s [%s] %s' % (act,jid,room,nick+'|'+status),'brown')
						if newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by censor!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
						elif act == 'mute': msg,mute = None,True
						else: msg = muc_filter_action(act,jid,room,L('Blocked by raw censor!',rn))

				# Large status filter
				if not mute and msg and get_config(gr,'muc_filter_large_status') != 'off' and len(esc_min2(status)) > GT('muc_filter_large_status_size'):
					act = get_config(gr,'muc_filter_large_status')
					muc_pprint('MUC-Filter large status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
					if act == 'truncate': msg = msg.replace(get_tag_full(msg,'status'),u'<status>%s…</status>' % esc_max2(esc_min2(status)[:GT('muc_filter_large_status_size')]))
					elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Large status block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
					elif act == 'mute': msg,mute = None,True
					else: msg = muc_filter_action(act,jid,room,L('Large status block!',rn))

				# Large nick filter
				if not mute and msg and get_config(gr,'muc_filter_large_nick') != 'off' and len(esc_min2(nick)) > GT('muc_filter_large_nick_size'):
					act = get_config(gr,'muc_filter_large_nick')
					if act == 'truncate': msg = msg.replace(esc_max2(tojid),u'%s/%s…' % (tojid.split('/',1)[0],esc_max2(esc_min2(nick)[:GT('muc_filter_large_nick_size')])))
					elif newjoin: msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Large nick block!',rn)])])])).replace('replace_it',get_tag(msg,'presence')),True
					elif act == 'mute': msg,mute = None,True
					else: msg = muc_filter_action(act,jid,room,L('Large nick block!',rn))

				# Rejoin filter
				if not mute and msg and get_config(gr,'muc_filter_rejoin') and newjoin:
					ttojid = '%s|%s' % (getRoom(tojid),getRoom(jid))
					try: muc_rejoins[ttojid] = [muc_rejoins[ttojid],muc_rejoins[ttojid][1:]][len(muc_rejoins[ttojid])==GT('muc_filter_rejoin_count')] + [int(time.time())]
					except: muc_rejoins[ttojid] = []
					if len(muc_rejoins[ttojid]) == GT('muc_filter_rejoin_count'):
						tmo = muc_rejoins[ttojid][GT('muc_filter_rejoin_count')-1] - muc_rejoins[ttojid][0]
						if tmo < GT('muc_filter_rejoin_timeout'):
							msg,mute = unicode(xmpp.Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',xmpp.Node('error', {'type': 'auth','code':'403'}, payload=[xmpp.Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),xmpp.Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('To many rejoins! Wait %s sec.',rn) % GT('muc_filter_rejoin_timeout')])])])).replace('replace_it',get_tag(msg,'presence')),True
							muc_pprint('MUC-Filter rejoin: %s [%s] %s' % (jid,room,nick),'brown')

				# Status filter
				if not mute and msg and get_config(gr,'muc_filter_repeat_prs') != 'off' and not newjoin:
					ttojid = '%s|%s' % (getRoom(tojid),getRoom(jid))
					try: muc_statuses[ttojid] = [muc_statuses[ttojid],muc_statuses[ttojid][1:]][len(muc_statuses[ttojid])==GT('muc_filter_status_count')] + [int(time.time())]
					except: muc_statuses[ttojid] = []
					if len(muc_statuses[ttojid]) == GT('muc_filter_status_count'):
						tmo = muc_statuses[ttojid][GT('muc_filter_status_count')-1] - muc_statuses[ttojid][0]
						if tmo < GT('muc_filter_status_timeout'):
							act = get_config(gr,'muc_filter_repeat_prs')
							muc_pprint('MUC-Filter status (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
							if act == 'mute': msg,mute = None,True
							else: msg = muc_filter_action(act,jid,room,L('Status-flood block!',rn))

		if msg:
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setTag('query',namespace=xmpp.NS_MUC_FILTER).setTagData(tag='message', val='')
			try: return unicode(i).replace('<message />',msg)
			except: pass

	return None

global iq_hook

iq_hook = [[200,'set',muc_filter_set]]

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

# translate: FN,NICKNAME,N.FAMILY,N.GIVEN,N.MIDDLE,ADR.LOCALITY,ADR.REGION,ADR.PCODE,ADR.CTRY,ADR.STREET,TEL.NUMBER,EMAIL.USERID,EMAIL,JABBERID,ROLE,BDAY,URL,DESC,ROLE,ORG.ORGNAME,ORG.ORGUNIT,GEO.LAT,GEO.LON,TITLE,PHOTO,uptime,seconds,users/registered,users,users/online,contacts/online,contacts,contacts/total,messages/in,messages,messages/out,memory-usage,KB,users/all-hosts/total,users/all-hosts/online,users/total

VCARD_LIMIT_LONG = 256
VCARD_LIMIT_SHORT = 128
iq_ping_minimal = GT('timeout')

def iq_iq_get(iq,id,room,acclvl,query,towh,al):
	if iq.getTag(name='query', namespace=xmpp.NS_VERSION) and GT('iq_version_enable'):
		pprint('*** iq:version from %s' % unicode(room),'magenta')
		i=xmpp.Iq(to=room, typ='result')
		i.setAttr(key='id', val=id)
		i.setQueryNS(namespace=xmpp.NS_VERSION)
		i.getTag('query').setTagData(tag='name', val=botName)
		i.getTag('query').setTagData(tag='version', val=botVersion)
		i.getTag('query').setTagData(tag='os', val=botOs)
		return i

	elif iq.getTag(name='query', namespace=xmpp.NS_TIME) and GT('iq_time_enable'):
		pprint('*** iq:time from %s' % unicode(room),'magenta')
		t_utc,t_tz,t_display = nice_time(time.time(),room)
		i=xmpp.Iq(to=room, typ='result')
		i.setAttr(key='id', val=id)
		i.setQueryNS(namespace=xmpp.NS_TIME)
		i.getTag('query').setTagData(tag='utc', val=t_utc)
		i.getTag('query').setTagData(tag='tz', val=t_tz)
		i.getTag('query').setTagData(tag='display', val=t_display)
		return i

	elif iq.getTag(name='time', namespace=xmpp.NS_URN_TIME) and GT('iq_time_enable'):
		pprint('*** iq:urn:time from %s' % unicode(room),'magenta')
		if timeofset in [-12,-11,-10]: t_tz = '-%s:00' % timeofset
		elif timeofset in range(-9,-1): t_tz = '-0%s:00' % timeofset
		elif timeofset in range(0,9): t_tz = '+0%s:00' % timeofset
		else: t_tz = '+%s:00' % timeofset
		i=xmpp.Iq(to=room, typ='result')
		i.setAttr(key='id', val=id)
		i.setTag('time',namespace=xmpp.NS_URN_TIME)
		i.getTag('time').setTagData(tag='tzo', val=t_tz)
		i.getTag('time').setTagData(tag='utc', val=str(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
		return i

	elif iq.getTag(name='ping', namespace=xmpp.NS_URN_PING) and GT('iq_ping_enable'):
		pprint('*** iq:urn:ping from %s' % unicode(room),'magenta')
		i=xmpp.Iq(to=room, typ='result')
		i.setAttr(key='id', val=id)
		return i

	elif iq.getTag(name='query', namespace=xmpp.NS_LAST) and GT('iq_uptime_enable'):
		pprint('*** iq:uptime from %s' % unicode(room),'magenta')
		i=xmpp.Iq(to=room, typ='result')
		i.setAttr(key='id', val=id)
		i.setTag('query',namespace=xmpp.NS_LAST,attrs={'seconds':str(int(time.time())-starttime)})
		i.setTagData('query','%s (%s) [%s]' % (Settings['message'],Settings['status'],Settings['priority']))
		return i
	return None

def get_who_iq(text,jid,nick):
	if text == '': who = '%s/%s' % (getRoom(jid),nick)
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = '%s/%s' % (getRoom(jid),text)
				break
	return who

def get_caps(room,nick):
	try:
		(id_node,id_ver,id_bmver) = capses['%s/%s' % (room,nick)].split('\n')
		if id_bmver: msg = '%s %s (%s)' % (id_node,id_ver,id_bmver)
		else: msg = '%s %s' % (id_node,id_ver)
	except: msg = None
	return msg

def noiq_caps(type, jid, nick, text):
	text = [text,nick][text == '']
	msg = get_caps(jid,text)
	if not msg: msg = L('I can\'t get caps of %s','%s/%s'%(jid,nick)) % text
	elif len(msg) == msg.count(' ')+msg.count('\n'): msg = L('%s has empty caps!','%s/%s'%(jid,nick)) % text
	send_msg(type, jid, nick, msg)

def iq_vcard(type, jid, nick, text):
	global iq_request
	if '\n' in text: text,args = text.split('\n',1)
	else: args = ''
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('vCard', {'xmlns': xmpp.NS_VCARD},[])])
	iq_request[iqid]=(time.time(),vcard_async,[type, jid, nick, text, args],xmpp.NS_VCARD)
	sender(i)

def vcard_async(type, jid, nick, text, args, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		try: vc,err = isa[1].getTag('vCard',namespace=xmpp.NS_VCARD),False
		except: vc,err = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick)),True
		if not vc or unicode(vc) == '<vCard xmlns="vcard-temp" />': msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),L('Empty!','%s/%s'%(jid,nick)))
		elif err: msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),vc[:VCARD_LIMIT_LONG])
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
					data_photo = L('type %s, %s','%s/%s'%(jid,nick)) % (photo_type,get_size_human(photo_size))
					data = [t for t in list(data) if t[0] not in ['PHOTO.BINVAL','PHOTO.TYPE']]
					data.append(('PHOTO',data_photo))
				except: pass
				args = args.lower()
				if not args:
					dd = get_array_from_array2(data,['NICKNAME','FN','BDAY','URL','PHOTO','DESC'])
					if dd: msg = '%s\n%s' % (L('vCard:','%s/%s'%(jid,nick)),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_LONG].strip(),t[1].strip()][len(t[1])<VCARD_LIMIT_LONG]) for t in dd]))
					else: msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),L('Not found!','%s/%s'%(jid,nick)))
				elif args == 'all': msg = '%s\n%s' % (L('vCard:','%s/%s'%(jid,nick)),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_SHORT].strip(),t[1].strip()][len(t[1])<VCARD_LIMIT_SHORT]) for t in data]))
				elif args == 'show':
					dd = []
					for t in data:
						if t[0] not in dd: dd.append(t[0])
					msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),', '.join([[t.capitalize(),'%s (%s)' % (t.capitalize(),L(t))][L(t)!=t] for t in dd]))
				else:
					args,dd = args.split('|'),[]
					for t in args:
						if ':' in t: val,loc = t.split(':',1)
						else: val,loc = t,t.upper()
						val = val.upper()
						dv = get_array_from_array2(data,(val))
						if dv: dd += [[loc,dv[0][1]]]
					if dd: msg = '%s\n%s' % (L('vCard:','%s/%s'%(jid,nick)),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_LONG],t[1]][len(t[1])<VCARD_LIMIT_LONG]) for t in dd]))
					else: msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),L('Not found!','%s/%s'%(jid,nick)))
			else: msg = '%s %s' % (L('vCard:','%s/%s'%(jid,nick)),L('Empty!','%s/%s'%(jid,nick)))
	send_msg(type, jid, nick, msg)

def iq_uptime(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_LAST},[])])
	iq_request[iqid]=(time.time(),uptime_async,[type, jid, nick, text],xmpp.NS_LAST)
	sender(i)

def uptime_async(type, jid, nick, text, is_answ):
	isa = is_answ[1][0]
	try:
		msg = L('Uptime: %s','%s/%s'%(jid,nick)) % un_unix(int(get_tag_item(isa,'query','seconds')),'%s/%s'%(jid,nick))
		up_stat = esc_min(get_tag(isa,'query'))
		if len(up_stat): msg = '%s // %s' % (msg,up_stat)
	except: msg = L('I can\'t do it','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def urn_ping(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('ping', {'xmlns': xmpp.NS_URN_PING},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text],xmpp.NS_URN_PING)
	sender(i)

def ping(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_VERSION},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text],xmpp.NS_VERSION)
	sender(i)

def ping_async(type, jid, nick, text, is_answ):
	global iq_ping_minimal
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error' and isa[0] == 'remote-server-not-found': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		p_digits = GT('ping_digits')
		original_ping = float(is_answ[0])
		if iq_ping_minimal > original_ping: iq_ping_minimal = original_ping
		fixed_ping = round(original_ping - iq_ping_minimal,p_digits)
		if fixed_ping <= 0: fixed_ping = original_ping
		f = '%'+'.0%sf' % p_digits
		if text in ['',nick]: msg = L('Ping from you %s sec.','%s/%s'%(jid,nick)) % f % fixed_ping
		else: msg = L('Ping from %s %s sec.','%s/%s'%(jid,nick)) % (text, f % fixed_ping)
	send_msg(type, jid, nick, msg)

def iq_time(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, None)

def iq_time_raw(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, True)

def iq_time_get(type, jid, nick, text, mode):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_TIME},[])])
	iq_request[iqid]=(time.time(),time_async,[type, jid, nick, text, mode],xmpp.NS_TIME)
	sender(i)

def time_async(type, jid, nick, text, mode, is_answ):
	isa = is_answ[1]
	if len(isa) == 3:
		msg = isa[0]
		if mode: msg += ', Raw time: %s, TimeZone: %s' % (isa[1],isa[2])
	else: msg = ' '.join(isa)
	send_msg(type, jid, nick, msg)

def iq_utime(type, jid, nick, text):
	iq_utime_get(type, jid, nick, text, None)

def iq_utime_raw(type, jid, nick, text):
	iq_utime_get(type, jid, nick, text, True)

def iq_utime_get(type, jid, nick, text, mode):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('time', {'xmlns': xmpp.NS_URN_TIME},[])])
	iq_request[iqid]=(time.time(),utime_async,[type, jid, nick, text, mode],xmpp.NS_URN_TIME)
	sender(i)

def utime_async(type, jid, nick, text, mode, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		try:
			ttup = isa[0].replace('T','-').replace('Z','').replace(':','-').split('-')+['0','0',str(tuple(time.localtime())[8])]
			lt = time.localtime(time.mktime([int(tmp.split('.',1)[0]) for tmp in ttup])+(int(isa[1].split(':')[0])*60+int(isa[1].split(':')[1]))*60)
			
			timeofset = float(isa[1].replace(':','.'))
			if timeofset < 0: t_gmt = 'GMT%s' % int(timeofset)
			else: t_gmt = 'GMT+%s' % int(timeofset)
			if timeofset%1: t_gmt += ':%02d' % int((timeofset%1*60/100) * 100)
			
			msg = '%02d:%02d:%02d, %02d.%s\'%s, %s, %s' % (lt[3],lt[4],lt[5],lt[2],L(wmonth[lt[1]-1],'%s/%s'%(jid,nick)),lt[0],L(wday[lt[6]],'%s/%s'%(jid,nick)),t_gmt)
			if mode: msg = '%s | %s %s' % (msg,isa[0],isa[1])
		except: msg = '%s %s' % (L('Unknown server answer!','%s/%s'%(jid,nick)),isa[0])
	send_msg(type, jid, nick, msg)

def iq_version(type, jid, nick, text): iq_version_raw(type, jid, nick, text, False)

def iq_version_caps(type, jid, nick, text): iq_version_raw(type, jid, nick, text, True)

def iq_version_raw(type, jid, nick, text, with_caps):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_VERSION},[])])
	iq_request[iqid]=(time.time(),version_async,[type, jid, nick, text, with_caps],xmpp.NS_VERSION)
	sender(i)

def version_async(type, jid, nick, text, with_caps, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else: msg = isa[0]
	if with_caps:
		caps = get_caps(jid,[text,nick][text == ''])
		if caps: msg += ' || %s' % caps
	send_msg(type, jid, nick, msg)

def iq_stats(type, jid, nick, text):
	global iq_request
	if text == '':
		send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))
		return
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_STATS},[])])
	iq_request[iqid]=(time.time(),stats_async_features,[type, jid, nick, text],xmpp.NS_STATS)
	sender(i)

def stats_async_features(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error':
		msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
		send_msg(type, jid, nick, msg)
	else:
		try: stats_list = [t.getAttr('name') for t in isa[1].getTag('query',namespace=xmpp.NS_STATS).getTags('stat')]
		except: stats_list = []
		if stats_list:
			iqid = get_id()
			i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_STATS},[xmpp.Node('stat', {'name':t},[]) for t in stats_list])])
			iq_request[iqid]=(time.time(),stats_async,[type, jid, nick, text],xmpp.NS_STATS)
			sender(i)
		else: send_msg(type, jid, nick, L('Unavailable!','%s/%s'%(jid,nick)))

def stats_async(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		try: stats_list = [[L(t.getAttr('name')),L(t.getAttr('value')),L(t.getAttr('units'))] for t in isa[1].getTag('query',namespace=xmpp.NS_STATS).getTags('stat')]
		except: stats_list = []
		if stats_list:
			stats_list = ['%s: %s' % (t[0].capitalize(),t[1]) if t[2] in t[0] else '%s: %s %s' % (t[0].capitalize(),t[1],t[2]) for t in stats_list]
			msg = L('Server statistic: %s\n%s','%s/%s'%(jid,nick)) % (text,'\n'.join(stats_list))
		else: msg = L('Unavailable!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute, iq_hook

iq_hook = [[50,'get',iq_iq_get]]

execute = [(3, 'ver', iq_version, 2, 'Client version.', ['nick','jid','server']),
		   (3, 'ver+', iq_version_caps, 2, 'Client version with caps.', ['nick']),
		   (3, 'caps', noiq_caps, 2, 'Show caps node and version of client.', ['nick']),
		   (3, 'ping_old', ping, 2, 'Ping - reply time. You can ping nick in room, jid, server or transport.', ['nick','jid','server']),
		   (3, 'ping', urn_ping, 2, 'Ping - reply time. You can ping nick in room, jid, server or transport.', ['nick','jid','server']),
		   (3, 'time_old', iq_time, 2, 'Client side time.', ['nick','jid']),
		   (3, 'time', iq_utime, 2, 'Client side time.', ['nick','jid']),
		   (3, 'time_old_raw', iq_time_raw, 2, 'Client side time + raw time format.', ['nick','jid']),
		   (3, 'time_raw', iq_utime_raw, 2, 'Client side time + raw time format.', ['nick','jid']),
		   (3, 'stats', iq_stats, 2, 'Users server statistic.', ['nick','jid','server']),
		   (3, 'vcard_raw', iq_vcard, 2, 'vCard query. Recomends make command base alias for query needs info.\nvcard_raw [nick] - query generic info\nvcard_raw nick\nshow - show available fields\nvcard_raw nick\n[field:name|field:name] - show requested fields from vcard.', ['nick','jid','server']),
		   (3, 'uptime', iq_uptime, 2, 'Server or jid uptime.', ['nick','jid','server'])]

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

backup_async = {}

def getMucItems(jid,affil,ns,back_id):
	iqid = get_id()
	if ns == xmpp.NS_MUC_ADMIN: i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':affil})])])
	else: i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [xmpp.Node('query', {'xmlns': ns},[])])
	iq_request[iqid]=(time.time(),getMucItems_async,[ns,affil,back_id],ns)
	sender(i)

def getMucItems_async(ns,affil,back_id,iq_stanza):
	global backup_async
	iq_stanza = iq_stanza[1][0]
	if ns == xmpp.NS_MUC_ADMIN: backup_async[back_id][affil] = [[tmp.getAttr('jid'),['',tmp.getTagData('reason')][tmp.getTagData('reason') != None]] for tmp in iq_stanza.getTag('query',namespace=xmpp.NS_MUC_ADMIN).getTags('item')]
	else: backup_async[back_id]['room_config'] = [[tmp.getAttr('var'),tmp.getAttr('type'),tmp.getTagData('value')] for tmp in iq_stanza.getTag('query',namespace=xmpp.NS_MUC_OWNER).getTag('x',namespace=xmpp.NS_DATA).getTags('field')]

def make_stanzas_array(raw_back,jid,affil):
	stanza_array = []
	try: make_stanza_jid_count = get_config_int(jid,'make_stanza_jid_count')
	except: make_stanza_jid_count = 1
	for tmp in range(0,len(raw_back),make_stanza_jid_count):
		i = xmpp.Iq(typ='set',to=jid,xmlns=xmpp.NS_CLIENT)
		i.setTag('query',namespace=xmpp.NS_MUC_ADMIN)
		for t in raw_back[tmp:tmp+make_stanza_jid_count]:
			i.getTag('query',namespace=xmpp.NS_MUC_ADMIN).\
					setTag('item',attrs={'affiliation':affil,'jid':t[0]}).\
					setTagData('reason',t[1])
		stanza_array.append(i)
	return stanza_array

def conf_backup(type, jid, nick, text):
	global backup_async,conn
	if len(text):
		text = text.split(' ')
		mode = text[0]

		if mode == 'show':
			a = os.listdir(back_folder % '')
			b = []
			for c in a:
				if not c.endswith('.txt') and not c.endswith('.back'): b.append((c,os.path.getmtime(back_folder % c)))
			if len(b): msg = '%s %s' % (L('Available copies:','%s/%s'%(jid,nick)), ', '.join(['%s (%s)' % (c[0],disp_time(c[1],'%s/%s'%(jid,nick))) for c in b]))
			else: msg = L('Backup copies not found.','%s/%s'%(jid,nick))
		elif mode == 'now':

			if get_xtype(jid) != 'owner': msg = L('I need an owner affiliation for backup settings!','%s/%s'%(jid,nick))
			else:
				back_id = get_id()
				backup_async[back_id] = {}
				getMucItems(jid,'outcast',xmpp.NS_MUC_ADMIN,back_id)
				getMucItems(jid,'member',xmpp.NS_MUC_ADMIN,back_id)
				getMucItems(jid,'admin',xmpp.NS_MUC_ADMIN,back_id)
				getMucItems(jid,'owner',xmpp.NS_MUC_ADMIN,back_id)
				getMucItems(jid,'',xmpp.NS_MUC_OWNER,back_id)
				bst = GT('backup_sleep_time')
				while len(backup_async[back_id]) != 5 and not game_over: time.sleep(bst)
				iqid = get_id()
				i = xmpp.Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'admin', 'jid':getRoom(str(selfjid))},[])])])
				sender(i)
				backup_async[back_id]['alias'] = cur_execute_fetchall('select match ,cmd from alias where room=%s',(jid,))
				backup_async[back_id]['bot_config'] = cur_execute_fetchall('select option ,value from config_conf where room=%s',(jid,))
				backup_async[back_id]['acl'] = cur_execute_fetchall('select action,type,text,command,time,level from acl where jid=%s',(jid,))
				backup_async[back_id]['rss'] = cur_execute_fetchall('select url, update ,type,time,hash from feed where room=%s',(jid,))

				msg = L('Copying completed!','%s/%s'%(jid,nick))
				msg += L('\nOwners: %s | Admins: %s | Members: %s | Banned: %s','%s/%s'%(jid,nick)) % (\
					len(backup_async[back_id]['owner'])-1,\
					len(backup_async[back_id]['admin'])+1,\
					len(backup_async[back_id]['member']),\
					len(backup_async[back_id]['outcast']))

				msg += L('\nRoom config: %s | Bot config: %s | Aliases: %s | Acl\'s: %s | RSS: %s','%s/%s'%(jid,nick)) % (\
					len(backup_async[back_id]['room_config']),\
					len(backup_async[back_id]['bot_config']),\
					len(backup_async[back_id]['alias']),\
					len(backup_async[back_id]['acl']),\
					len(backup_async[back_id]['rss']))

				writefile(back_folder % unicode(jid),json.dumps(backup_async[back_id]))

		elif mode == 'restore':
			if len(text)>1:
				if text[1] in os.listdir(back_folder % ''):
					if text[1].endswith('.acl'):
						raw_back = json.loads(readfile(back_folder % unicode(text[1])))
						cnt = 0
						for tmp in raw_back:
							isit = cur_execute_fetchall('select action,type,text,command,time from acl where jid=%s and action=%s and type=%s and text=%s and level=%s',(jid,tmp[0],tmp[1],tmp[2],tmp[5]))
							if not isit:
								cur_execute('insert into acl values (%s,%s,%s,%s,%s,%s,%s)', tmp)
								cnt += 1
						msg = L('Restored %s action(s).','%s/%s'%(jid,nick)) % cnt
					elif get_xtype(jid) != 'owner': msg = L('I need an owner affiliation for restore settings!','%s/%s'%(jid,nick))
					else:
						bst = GT('backup_sleep_time')
						raw_back=json.loads(readfile(back_folder % unicode(text[1])))
						for tmp in ['outcast','member','admin','owner']:
							for t in make_stanzas_array(raw_back[tmp],jid,tmp):
								sender(t)
								time.sleep(bst)
						i = xmpp.Iq(typ='set',to=jid,xmlns=xmpp.NS_CLIENT)
						i.setTag('query',namespace=xmpp.NS_MUC_OWNER)
						i.getTag('query',namespace=xmpp.NS_MUC_OWNER).setTag('x',namespace=xmpp.NS_DATA).setAttr('type','submit')
						for tmp in raw_back['room_config']:
							i.getTag('query',namespace=xmpp.NS_MUC_OWNER).getTag('x',namespace=xmpp.NS_DATA).\
								setTag('field',attrs={'var':tmp[0],'type':tmp[1]}).\
								setTagData('value',tmp[2])
						sender(i)
						time.sleep(bst)
						sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'admin', 'jid':getRoom(unicode(selfjid))},[])])]))
						time.sleep(bst)
						cur_execute_fetchall('delete from config_conf where room=%s',(jid,))
						for tmp in raw_back['bot_config']: cur_execute('insert into config_conf (room, option ,value) values (%s,%s,%s)',(jid,tmp[0],tmp[1]))
						for tmp in raw_back['alias']:
							cur_execute('delete from alias where room=%s and match =%s',(jid,tmp[0]))
							cur_execute('insert into alias (room, match ,cmd) values (%s,%s,%s)',(jid,tmp[0],tmp[1]))
						for tmp in raw_back['acl']:
							isit = cur_execute_fetchall('select action,type,text,command,time from acl where jid=%s and action=%s and type=%s and text=%s and level=%s',(jid,tmp[0],tmp[1],tmp[2],tmp[5]))
							if not isit: cur_execute('insert into acl values (%s,%s,%s,%s,%s,%s,%s)', tuple([jid]+list(tmp)))
						for tmp in raw_back['rss']:
							isit = cur_execute_fetchone('select * from feed where room=%s and url=%s',(jid,tmp[0]))
							if not isit: cur_execute('insert into feed (url, update ,type,time,room,hash) values (%s,%s,%s,%s,%s,%s)',(tmp[0],tmp[1],tmp[2],tmp[3],jid,tmp[4]))
						msg = L('Restore completed.','%s/%s'%(jid,nick))
						msg += L('\nOwners: %s | Admins: %s | Members: %s | Banned: %s','%s/%s'%(jid,nick)) % (\
							len(raw_back['owner'])-1,\
							len(raw_back['admin'])+1,\
							len(raw_back['member']),\
							len(raw_back['outcast']))

						msg += L('\nRoom config: %s | Bot config: %s | Aliases: %s | Acl\'s: %s | RSS: %s','%s/%s'%(jid,nick)) % (\
							len(raw_back['room_config']),\
							len(raw_back['bot_config']),\
							len(raw_back['alias']),\
							len(raw_back['acl']),\
							len(raw_back['rss']))
				else: msg = L('Copy not found. Use key "show" for lisen available copies.','%s/%s'%(jid,nick))
			else: msg = L('What do you want to restore?','%s/%s'%(jid,nick))
		else: msg = L('Unknown item!','%s/%s'%(jid,nick))
	else: msg = 'backup now|show|restore'
	send_msg(type, jid, nick, msg)

global execute

execute = [(8, 'backup', conf_backup, 2, 'Backup/restore conference settings.\nbackup show|now|restore\nshow - show available copies\nnow - backup current conference\nrestore name_conference - restore settings name_conference in current conference')]

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

def reban(type, jid, nick, text):
	try: lim = int(text)
	except:
		send_msg(type, jid, nick, L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick)))
		return
	global banbase,iq_request
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast'})])])
	iq_request[iqid]=(time.time(),reban_async,[type, jid, nick, lim],xmpp.NS_MUC_ADMIN)
	sender(i)

def reban_async(type, jid, nick, lim, iq_stanza):
	isa = iq_stanza[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		_trusted = get_config(getRoom(jid),'trusted_servers').split()
		_jids = [tmp.getAttr('jid') for tmp in iq_stanza[1][0].getTag('query',namespace=xmpp.NS_MUC_ADMIN).getTags('item')]
		_srv_count = {}
		for t in _jids:
			if '@' in t:
				_t = t.split('@',1)[1]
				if _t not in _trusted: _srv_count[_t] = _srv_count[_t] + 1 if _srv_count.has_key(_t) else 1
		_servers = [t for t in _jids if '@' not in t]
		_new_servers = [t for t in _srv_count.keys() if _srv_count[t] >= lim and t not in _servers]
		_need_remove = [t for t in _jids if '@' in t and t.split('@',1)[1] in _servers + _new_servers]
		_new_servers.sort()

		_limit = get_config_int(getRoom(jid),'make_stanza_jid_count')
		nodes = []
		for t in _new_servers:
			reason = [xmpp.Node('reason',{},'Rebanned as dangerous! Found jids: %s' % _srv_count[t])]
			nodes.append(xmpp.Node('item',{'affiliation':'outcast', 'jid':t},reason))
			if len(nodes) >= _limit:
				sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},nodes)]))
				nodes = []
		if nodes: sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},nodes)]))
		nodes = []
		for t in _need_remove:
			nodes.append(xmpp.Node('item',{'affiliation':'none', 'jid':t},[]))
			if len(nodes) >= _limit:
				sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},nodes)]))
				nodes = []
		if nodes: sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},nodes)]))
		msg = L('Unbaned jids: %s\nBanned servers: %s .. %s','%s/%s'%(jid,nick)) % (len(_need_remove), len(_new_servers), ', '.join(_new_servers))
	send_msg(type, jid, nick, msg)

def inban(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'outcast', L('Total banned: %s','%s/%s'%(jid,nick)))
def inowner(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'owner', L('Total owners: %s','%s/%s'%(jid,nick)))
def inadmin(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'admin', L('Total admins: %s','%s/%s'%(jid,nick)))
def inmember(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'member', L('Total members: %s','%s/%s'%(jid,nick)))

def inlist_raw(type, jid, nick, text, affil, message):
	global banbase,iq_request
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':affil})])])
	iq_request[iqid]=(time.time(),inlist_raw_async,[type, jid, nick, text, message],xmpp.NS_MUC_ADMIN)
	sender(i)

def inlist_raw_async(type, jid, nick, text, message, iq_stanza):
	isa = iq_stanza[1]
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		bb = [[tmp.getAttr('jid'),['',tmp.getTagData('reason')][tmp.getTagData('reason') != None]] for tmp in iq_stanza[1][0].getTag('query',namespace=xmpp.NS_MUC_ADMIN).getTags('item')]
		bb.sort()
		msg = message % len(bb)
		if text != '':
			text = text.strip().split()
			if len(text) == 1: text,nt = text[0], 0
			elif text[0] == '!': text,nt = ' '.join(text[1:]), 1
			elif text[0] == '=': text,nt = ' '.join(text[1:]), 2
			else: text,nt = ' '.join(text[1:]), False
			msg += ', '
			mmsg, cnt = '', 1
			for i in bb:
				if [text.lower() in i[0].lower() or text.lower() in i[1].lower(), text.lower() not in i[0].lower(),text.lower() == i[0].lower() or text.lower() == i[1].lower()][nt]:
					mmsg += '\n%s. %s' % (cnt,i[0])
					if len(i[1]): mmsg += ' - %s' % i[1]
					cnt += 1
			if len(mmsg): msg += L('Found:','%s/%s'%(jid,nick)) + ' %s%s' % (mmsg.count('\n'),mmsg)
			else: msg += L('no matches!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(7, 'inban', inban, 2, 'Search in outcast list of conference.'),
	 (7, 'inmember', inmember, 2, 'Search in members list of conference.'),
	 (7, 'inadmin', inadmin, 2, 'Search in admins list of conference.'),
	 (7, 'inowner', inowner, 2, 'Search in owners list of conference.'),
	 (8, 'reban', reban, 2, 'Cleen up outcast list. Replace different jids from same server by one server jid\nreban <count>')]

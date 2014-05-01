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

def vendor_by_mac(type, jid, nick, text):
	text = text.strip().replace('-','').replace(':','').replace(' ','')[:6].upper()
	if text and len(text) == 6:
		result = html_encode(load_page('http://standards.ieee.org/cgi-bin/ouisearch?%s' % text))
		r = re.findall('\(hex\)(.*?)\n',result,re.S|re.I)
		if 'Sorry!' in result and not r: msg = L('Not found!','%s/%s'%(jid,nick))
		else: msg = r[0].strip().upper()
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def net_ping(type, jid, nick, text):
	text = text.strip().lower().encode('idna')
	if '.' in text and len(text) > 4 and re.match(r'[-0-9a-z.]+\Z', text, re.U+re.I): msg = deidna(shell_execute('ping -c4 %s' % text,'%s/%s'%(jid,nick)))
	else: msg = L('Smoke help about command!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def get_tld(type, jid, nick, text):
	if len(text) >= 2:
		tld = readfile(tld_list).decode('utf-8')
		tld = tld.split('\n')
		msg = L('Not found!','%s/%s'%(jid,nick))
		for tl in tld:
			if tl.split('\t')[0].lower()==text.lower():
				msg = '.'+tl.replace('\t',' - ',1).replace('\t','\n')
				break
	else: msg = L('What do you want to find?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def get_dns(type, jid, nick, text):
	is_ip = None
	if text.count('.') == 3:
		is_ip = True
		for ii in text:
			if not nmbrs.count(ii):
				is_ip = None
				break
	if is_ip:
		try: msg = socket.gethostbyaddr(text)[0]
		except: msg = L('I can\'t resolve it','%s/%s'%(jid,nick))
	else:
		try:
			ans = socket.gethostbyname_ex(text.encode('idna'))[2]
			msg = text+' - '
			for an in ans: msg += an + ' | '
			msg = msg[:-2]
		except: msg = L('I can\'t resolve it','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'host '+text)

def srv_raw_check(type, jid, nick, text):
	text = enidna_raw(text)
	text = ''.join(re.findall(u'[-a-z0-9\.\_\?\#\=\@\%\ \+]+',text,re.S|re.I)[0])
	send_msg(type, jid, nick, deidna(shell_execute(text,'%s/%s'%(jid,nick))))

def chkserver(type, jid, nick, text):
	for a in ':;&/|\\\n\t\r': text = text.replace(a,' ')
	t = re.findall(u'[-a-zа-я0-9._?#=@%]+',text,re.S|re.I|re.U)
	if len(t) >= 2:
		port = []
		for a in t:
			if a.isdigit(): port.append(a)
		for a in port: t.remove(a)
		if len(t)==1 and len(port)>=1:
			t = t[0]
			port.sort()
			msg = shell_execute('nmap %s -p%s -P0 -T5' % (t.encode('idna'),','.join(port)),'%s/%s'%(jid,nick))
			try: msg = '%s\n%s' % (t.encode('idna'),reduce_spaces_all(re.findall('SERVICE(.*)Nmap',msg,re.S|re.U)[0][1:-2]))
			except:
				try:
					msg = ''
					for a in port:
						sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						try:
							sock.connect((t.encode('idna'),int(a)))
							s = L('on','%s/%s'%(jid,nick))
						except: s = L('off','%s/%s'%(jid,nick))
						msg += '\n%s %s' % (a,s)
						sock.close()
					msg = '%s%s' % (t,msg)
				except: msg = '%s - %s' % (t,L('unknown','%s/%s'%(jid,nick)))
			msg = L('Port status at %s','%s/%s'%(jid,nick)) % msg
		else: msg = L('What?','%s/%s'%(jid,nick))
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(6, 'nslookup', srv_nslookup, 2, 'Command nslookup'),
		   (6, 'host', srv_host, 2, 'Command host'),
		   (6, 'dig', srv_dig, 2, 'Command dig'),
		   (4, 'port', chkserver, 2, 'Check port activity\nport server port1 [port2 ...]'),
		   (4, 'net_ping', net_ping, 2, 'Net Ping.\nnet_ping ip|domain'),
		   (3, 'dns', get_dns, 2, 'DNS resolver.'),
		   (3, 'tld', get_tld, 2, 'Search domain zones TLD.'),
		   (3, 'mac', vendor_by_mac, 2, 'Show vendor of device by mac')]

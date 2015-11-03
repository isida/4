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

# translate: random,smart,full,partial,on,off,kick,ban,replace,mute,visitor,truncate,paste,chat,online,away,xa,dnd,on start,on shutdown,by time,black,white,without highlight,all,ban server,Loading...,Mon,Tue,Wed,Thu,Fri,Sat,Sun,_Jan,_Feb,_Mar,_Apr,_May,_Jun,_Jul,_Aug,_Sep,_Oct,_Nov,_Dec,no limit,visitor/none,visitor/member,participant/none,participant/member,moderator/none,moderator/member,moderator/admin,moderator/owner,bot owner,You should be at least %s to do it.,You must be a %s to do it.,absent,Bad request,Conflict,Feature not implemented,Forbidden,Gone,Internal server error,Item not found,Jid malformed,Not acceptable,Not allowed,Not authorized,Payment required,Recipient unavailable,Redirect,Registration required,Remote server not found,Remote server timeout,Resource constraint,Service unavailable,Subscription required,Undefined condition,Unexpected request

rlmas_min = (('&','&amp;'),('\"','&quot;'),('\'','&apos;'),('<','&lt;'),('>','&gt;'))

rlmas = rlmas_min + (('~','&tilde;'),('\t','&nbsp;'*8))

lmass = (('\n','<br>'),('\n','<br />'),('\n','<br/>'),('\n','\n\r'),('','<![CDATA['),('',']]>'),
		('','&shy;'),('','&ensp;'),('','&emsp;'),('','&thinsp;'),('','&zwnj;'),('','&zwj;'))

rmass = (('&','&amp;'),('\"','&quot;'),('\'','&apos;'),('~','&tilde;'),(' ','&nbsp;'),
		('<','&lt;'),('>','&gt;'),(u'¡','&iexcl;'),(u'¢','&cent;'),(u'£','&pound;'),
		(u'¤','&curren;'),(u'¥','&yen;'),(u'¦','&brvbar;'),(u'§','&sect;'),(u'¨','&uml;'),(u'©','&copy;'),(u'ª','&ordf;'),
		(u'«','&laquo;'),(u'¬','&not;'),(u'®','&reg;'),(u'¯','&macr;'),(u'°','&deg;'),(u'±','&plusmn;'),
		(u'²','&sup2;'),(u'³','&sup3;'),(u'´','&acute;'),(u'µ','&micro;'),(u'¶','&para;'),(u'·','&middot;'),(u'¸','&cedil;'),
		(u'¹','&sup1;'),(u'º','&ordm;'),(u'»','&raquo;'),(u'¼','&frac14;'),(u'½','&frac12;'),(u'¾','&frac34;'),(u'¿','&iquest;'),
		(u'×','&times;'),(u'÷','&divide;'),(u'À','&Agrave;'),(u'Á','&Aacute;'),(u'Â','&Acirc;'),(u'Ã','&Atilde;'),(u'Ä','&Auml;'),
		(u'Å','&Aring;'),(u'Æ','&AElig;'),(u'Ç','&Ccedil;'),(u'È','&Egrave;'),(u'É','&Eacute;'),(u'Ê','&Ecirc;'),(u'Ë','&Euml;'),
		(u'Ì','&Igrave;'),(u'Í','&Iacute;'),(u'Î','&Icirc;'),(u'Ï','&Iuml;'),(u'Ð','&ETH;'),(u'Ñ','&Ntilde;'),(u'Ò','&Ograve;'),
		(u'Ó','&Oacute;'),(u'Ô','&Ocirc;'),(u'Õ','&Otilde;'),(u'Ö','&Ouml;'),(u'Ø','&Oslash;'),(u'Ù','&Ugrave;'),(u'Ú','&Uacute;'),
		(u'Û','&Ucirc;'),(u'Ü','&Uuml;'),(u'Ý','&Yacute;'),(u'Þ','&THORN;'),(u'ß','&szlig;'),(u'à','&agrave;'),(u'á','&aacute;'),
		(u'â','&acirc;'),(u'ã','&atilde;'),(u'ä','&auml;'),(u'å','&aring;'),(u'æ','&aelig;'),(u'ç','&ccedil;'),(u'è','&egrave;'),
		(u'é','&eacute;'),(u'ê','&ecirc;'),(u'ë','&euml;'),(u'ì','&igrave;'),(u'í','&iacute;'),(u'î','&icirc;'),(u'ï','&iuml;'),
		(u'ð','&eth;'),(u'ñ','&ntilde;'),(u'ò','&ograve;'),(u'ó','&oacute;'),(u'ô','&ocirc;'),(u'õ','&otilde;'),(u'ö','&ouml;'),
		(u'ø','&oslash;'),(u'ù','&ugrave;'),(u'ú','&uacute;'),(u'û','&ucirc;'),(u'ü','&uuml;'),(u'ý','&yacute;'),(u'þ','&thorn;'),
		(u'ÿ','&yuml;'),(u'∀','&forall;'),(u'∂','&part;'),(u'∃','&exists;'),(u'∅','&empty;'),(u'∇','&nabla;'),(u'∈','&isin;'),
		(u'∉','&notin;'),(u'∋','&ni;'),(u'∏','&prod;'),(u'∑','&sum;'),(u'−','&minus;'),(u'∗','&lowast;'),(u'√','&radic;'),
		(u'∝','&prop;'),(u'∞','&infin;'),(u'∠','&ang;'),(u'∧','&and;'),(u'∨','&or;'),(u'∩','&cap;'),(u'∪','&cup;'),
		(u'∫','&int;'),(u'∴','&there4;'),(u'∼','&sim;'),(u'≅','&cong;'),(u'≈','&asymp;'),(u'≠','&ne;'),(u'≡','&equiv;'),
		(u'≤','&le;'),(u'≥','&ge;'),(u'⊂','&sub;'),(u'⊃','&sup;'),(u'⊄','&nsub;'),(u'⊆','&sube;'),(u'⊇','&supe;'),
		(u'⊕','&oplus;'),(u'⊗','&otimes;'),(u'⊥','&perp;'),(u'⋅','&sdot;'),(u'Α','&Alpha;'),(u'Β','&Beta;'),(u'Γ','&Gamma;'),
		(u'Δ','&Delta;'),(u'Ε','&Epsilon;'),(u'Ζ','&Zeta;'),(u'Η','&Eta;'),(u'Θ','&Theta;'),(u'Ι','&Iota;'),(u'Κ','&Kappa;'),
		(u'Λ','&Lambda;'),(u'Μ','&Mu;'),(u'Ν','&Nu;'),(u'Ξ','&Xi;'),(u'Ο','&Omicron;'),(u'Π','&Pi;'),(u'Ρ','&Rho;'),
		(u'Σ','&Sigma;'),(u'Τ','&Tau;'),(u'Υ','&Upsilon;'),(u'Φ','&Phi;'),(u'Χ','&Chi;'),(u'Ψ','&Psi;'),(u'Ω','&Omega;'),
		(u'α','&alpha;'),(u'β','&beta;'),(u'γ','&gamma;'),(u'δ','&delta;'),(u'ε','&epsilon;'),(u'ζ','&zeta;'),(u'η','&eta;'),
		(u'θ','&theta;'),(u'ι','&iota;'),(u'κ','&kappa;'),(u'λ','&lambda;'),(u'μ','&mu;'),(u'ν','&nu;'),(u'ξ','&xi;'),
		(u'ο','&omicron;'),(u'π','&pi;'),(u'ρ','&rho;'),(u'ς','&sigmaf;'),(u'σ','&sigma;'),(u'τ','&tau;'),(u'υ','&upsilon;'),
		(u'φ','&phi;'),(u'χ','&chi;'),(u'ψ','&psi;'),(u'ω','&omega;'),(u'ϑ','&thetasym;'),(u'ϒ','&upsih;'),(u'ϖ','&piv;'),
		(u'Œ','&OElig;'),(u'œ','&oelig;'),(u'Š','&Scaron;'),(u'š','&scaron;'),(u'Ÿ','&Yuml;'),(u'ƒ','&fnof;'),(u'ˆ','&circ;'),
		(u'‎','&lrm;'),(u'‏','&rlm;'),(u'–','&ndash;'),(u'—','&mdash;'),(u'‘','&lsquo;'),(u'’','&rsquo;'),(u'‚','&sbquo;'),
		(u'“','&ldquo;'),(u'”','&rdquo;'),(u'„','&bdquo;'),(u'†','&dagger;'),(u'‡','&Dagger;'),(u'•','&bull;'),(u'…','&hellip;'),
		(u'‰','&permil;'),(u'′','&prime;'),(u'″','&Prime;'),(u'‹','&lsaquo;'),(u'›','&rsaquo;'),(u'‾','&oline;'),(u'€','&euro;'),
		(u'™','&trade;'),(u'←','&larr;'),(u'↑','&uarr;'),(u'→','&rarr;'),(u'↓','&darr;'),(u'↔','&harr;'),(u'↵','&crarr;'),
		(u'⌈','&lceil;'),(u'⌉','&rceil;'),(u'⌊','&lfloor;'),(u'⌋','&rfloor'),(u'◊','&loz;'),(u'♠','&spades;'),(u'♣','&clubs;'),
		(u'♥','&hearts;'),(u'♦','&diams;'))

levl = {'no|limit':0,'visitor|none':1,'visitor|member':2,'participant|none':3,'participant|member':4,
		'moderator|none':5,'moderator|member':6,'moderator|admin':7,'moderator|owner':8,'bot|owner':9}

unlevl = ['no limit','visitor/none','visitor/member','participant/none','participant/member',
		  'moderator/none','moderator/member','moderator/admin','moderator/owner','bot owner']

unlevltxt = ['You should be at least %s to do it.','You must be a %s to do it.']

unlevlnum = [0,0,0,0,0,0,0,0,0,1]

presence_error = {'401':L('Password required'),
				  '403':L('Forbidden'),
				  '407':L('Members-only')}

msg_status_codes = {'102':L('Room now shows unavailable members.'),
					'103':L('Room now does not show unavailable members.'),
					'104':L('Room\'s configuration changed.'),
					'171':L('Logs at server side are enabled.'),
					'172':L('Room now is non-anonymous.'),
					'173':L('Room now is semi-anonymous.'),
					'174':L('Room now is fully-anonymous.')}

wday = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
wmonth = ['_Jan','_Feb','_Mar','_Apr','_May','_Jun','_Jul','_Aug','_Sep','_Oct','_Nov','_Dec']

two_en = ['aa', 'aq', 'bc', 'bd', 'bf', 'bg', 'bh', 'bk', 'bn', 'bp', 'bq', 'bw', 'bx', 'bz', 'cb', 'cd', 'cf', 'cg', 'cj', \
		  'cm', 'cn', 'cp', 'cs', 'cv', 'cw', 'cx', 'cz', 'db', 'dc', 'dh', 'dj', 'dp', 'dq', 'dt', 'dx', 'dz', 'ej', 'fb', \
		  'fc', 'fd', 'fg', 'fh', 'fj', 'fk', 'fm', 'fn', 'fp', 'fq', 'fs', 'fv', 'fx', 'fz', 'gb', 'gc', 'gf', 'gj', 'gk', \
		  'gp', 'gq', 'gv', 'gw', 'gx', 'gz', 'hc', 'hg', 'hh', 'hj', 'hk', 'hp', 'hq', 'hs', 'hv', 'hx', 'hz', 'ih', 'ii', \
		  'ij', 'iq', 'iw', 'iy', 'jb', 'jc', 'jd', 'jf', 'jg', 'jh', 'jj', 'jk', 'jl', 'jm', 'jn', 'jq', 'jr', 'js', 'jt', \
		  'jv', 'jw', 'jx', 'jy', 'jz', 'kb', 'kc', 'kd', 'kj', 'kk', 'km', 'kp', 'kq', 'kr', 'ks', 'kt', 'kv', 'kx', 'kz', \
		  'lh', 'lj', 'ln', 'lq', 'lx', 'lz', 'mc', 'md', 'mg', 'mh', 'mj', 'mk', 'mq', 'mv', 'mw', 'mx', 'mz', 'nb', 'nr', \
		  'oq', 'pc', 'pf', 'pj', 'pk', 'pq', 'pv', 'px', 'pz', 'qa', 'qb', 'qc', 'qd', 'qe', 'qf', 'qg', 'qh', 'qi', 'qj', \
		  'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt', 'qv', 'qw', 'qx', 'qy', 'qz', 'rj', 'rq', 'rx', 'rz', \
		  'sj', 'sv', 'sx', 'sz', 'tb', 'td', 'tg', 'tj', 'tk', 'tq', 'tv', 'tx', 'tz', 'uh', 'uj', 'uo', 'uq', 'uu', 'uv', \
		  'uw', 'ux', 'vb', 'vc', 'vd', 'vf', 'vg', 'vh', 'vj', 'vk', 'vl', 'vm', 'vn', 'vp', 'vq', 'vr', 'vs', 'vt', 'vu', \
		  'vv', 'vw', 'vx', 'vz', 'wb', 'wc', 'wg', 'wj', 'wm', 'wp', 'wq', 'wt', 'wu', 'wv', 'wx', 'wz', 'xb', 'xd', 'xg', \
		  'xj', 'xk', 'xl', 'xn', 'xo', 'xq', 'xr', 'xs', 'xu', 'xv', 'xw', 'xx', 'xz', 'yc', 'yd', 'yf', 'yg', 'yj', 'yk', \
		  'yn', 'yq', 'yu', 'yv', 'yx', 'yy', 'yz', 'zb', 'zc', 'zd', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk', 'zm', 'zn', 'zp', \
		  'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw', 'zx']

def non_case_sort(arr):
	tmp = [[t.lower(),t] for t in arr]
	tmp.sort()
	return [t[1] for t in tmp]
		  
def get_size_human(mt):
	if mt < 1024: return '%sb' % int(mt)
	for t in ['Kb','Mb','Gb']:
		mt = mt / 1024.0
		if mt < 1024: break
	return '%.2f%s' % (mt,t)

def is_owner(jid): return cur_execute_fetchone('select * from bot_owner where jid=%s',(getRoom(jid),)) != None

def validate_nick(nick,count):
		nick = nick.lower()
		pairs = 0
		for t in re.findall('\s+[^\s]*', ' ' + nick):
			pairs += sum([t.count(k) for k in two_en])
		return pairs-len(nick.split()) < count, pairs

def get_xnick(jid):
	tmp = cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%getRoom(jid),))
	if tmp: return getResourse(tmp[0])
	else: return Settings['nickname']

def get_xtype(jid):
	jid,xtype = getRoom(jid),'owner'
	nowname = get_xnick(jid)
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	return xtype

def clean_user_and_server_hash():
	global user_hash, server_hash, server_hash_list
	timing = {}
	for tmp in user_hash.keys():
		try:
			tm = user_hash[tmp]
			gr = getRoom(tmp)
			try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
			except: tmo = 3600
			if timing.has_key(gr): tmo = timing[gr]
			else: timing[gr] = tmo
			if time.time() > tm + tmo: user_hash.pop(tmp)
		except: pass
	for tmp in server_hash_list.keys():
		tm = server_hash_list[tmp]
		gr = getRoom(tmp)
		try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
		except: tmo = 3600
		if timing.has_key(gr): tmo = timing[gr]
		else: timing[gr] = tmo
		if time.time() > tm + tmo: server_hash_list.pop(tmp)
	for tmp in server_hash.keys():
		try:
			tm = server_hash[tmp][0]
			gr = getRoom(tmp)
			try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
			except: tmo = 3600
			if timing.has_key(gr): tmo = timing[gr]
			else: timing[gr] = tmo
			if time.time() > tm + tmo: server_hash.pop(tmp)
		except: pass

def ddos_info(type, room, nick, text):
	global ddos_ignore
	text = reduce_spaces_all(text.lower()).split()
	if text == []: text = ['']
	if text[0] in ['','show']:
		tmas = []
		for tmp in ddos_ignore.keys(): tmas.append('%s/%s [%s] %s' % (ddos_ignore[tmp][0],ddos_ignore[tmp][1],tmp,un_unix(ddos_ignore[tmp][2]-time.time(),'%s/%s'%(jid,nick))))
		if tmas: msg = L('Ignore list: %s','%s/%s'%(jid,nick)) % '; '.join(tmas)
		else: msg = L('List is empty.','%s/%s'%(jid,nick))
	elif text[0] in ['del','remove'] and len(text) > 1:
		if ddos_ignore.has_key(text[1]):
			try:
				ddos_ignore.pop(text[1])
				msg = L('Removed: %s','%s/%s'%(jid,nick)) % text[1]
			except: msg = L('Not found: %s','%s/%s'%(jid,nick)) % text[1]
		else: msg = L('Not found: %s','%s/%s'%(jid,nick)) % text[1]
	else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	send_msg(type, room, nick, msg)

def atempt_to_shutdown(critical):
	if not critical:
		pprint('Close age base','dark_gray')
		close_age()
	if thread_type:
		try: garbage_collector_timer.cancel()
		except: pass
	if base_type not in ['sqlite3','mysql']:
		conn.commit()
		conn.close()
	flush_stats()

def atempt_to_shutdown_with_reason(text,sleep_time,exit_type,critical):
	pprint(text,'red')
	send_presence_all(text)
	atempt_to_shutdown(critical)
	if sleep_time: time.sleep(sleep_time)
	sys.exit(exit_type)

def deidna(text):
	def repl(t): return t.group().lower().decode('idna')
	return re.sub(r'(xn--[-0-9a-z_]*)',repl,text,flags=re.S|re.I|re.U)

def enidna(text):
	idn = re.findall(u'http[s]?://([-0-9a-zа-я._]*)',text,flags=re.S|re.I|re.U)
	if idn: text = text.replace(idn[0],idn[0].lower().encode('idna'))
	return text.encode('utf-8')

def enidna_raw(text):
	def repl(t): return t.group().lower().encode('idna')
	return re.sub(u'([а-я][-0-9а-я_]*)',repl,text,flags=re.S|re.I|re.U)

def get_level(cjid, cnick):
	access_mode = -2
	jid = 'None'
	for base in megabase:
		if base[1] == cnick and base[0].lower()==cjid:
			jid = base[4]
			j_affl = base[3]
			if j_affl in ['admin','owner']: j_role = 'moderator'
			else: j_role = base[2]
			if '%s|%s' % (j_role,j_affl) in levl:
				access_mode = levl['%s|%s' % (j_role,j_affl)]
				break
	if cur_execute_fetchone('select pattern from bot_ignore where %s ilike pattern',(getRoom(jid.lower()),)): access_mode = -1
	rjid = getRoom(jid)
	if is_owner(rjid): access_mode = 9
	if jid == 'None' and is_owner(cjid): access_mode = 9
	return (access_mode, jid)

def show_syslogs(type, jid, nick, text):
	tmp = text.strip().split(' ', 1)
	lsz, txt = 10, ''
	if len(tmp) == 1:
		try: lsz = int(tmp[0])
		except: txt = tmp[0]
	elif len(tmp) == 2:
		try: lsz, txt = int(tmp[0]), tmp[1]
		except: txt = text
	lsz += 1
	lsz = 1 if lsz <= 0 else (last_logs_size if lsz > last_logs_size else lsz)
	msg = '\n'.join([tmp for tmp in last_logs_store if txt in tmp.lower() or txt in tmp][1:lsz][::-1])
	if msg:
		send_msg(type, jid, nick, L('Last syslogs:\n%s','%s/%s'%(jid,nick)) % msg)
	else:
		send_msg(type, jid, nick, L('Syslogs not found','%s/%s'%(jid,nick)))

def show_syslogs_search(type, jid, nick, text):
	if '\n' in text: text,value = text.lower().split('\n',1)
	else: text,value = text.lower(),''
	if not text.strip():
		send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))
		return
	if value:
		try: _ = re.compile(value)
		except:
			send_msg(type, jid, nick, L('Error in RegExp!','%s/%s'%(jid,nick)))
			return
	try: _ = re.compile(text)
	except:
		send_msg(type, jid, nick, L('Error in RegExp!','%s/%s'%(jid,nick)))
		return
	files = [t for t in os.listdir(slog_folder % '') if re.findall('^[0-9]{8}\.txt$',t)]
	files.sort()
	if not value: files = files[-1:]
	matches = []
	for t in files:
		if not value or (value and re.findall(value,t.split('.')[0])):
			m = [f for f in readfile(slog_folder % t).decode('utf-8').split('\n') if ' [9] syslogs_search' not in f and re.findall(text,f,re.S|re.I|re.U)]
			if m:
				if value: matches.append('*** %s%s%s%s-%s%s-%s%s ***' % tuple(t.split('.')[0]))
				matches += m
	if matches: msg = L('Last syslogs: %s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join(matches)
	else: msg = L('Not found!','%s/%s'%(jid,nick))
	if len(msg) > msg_limit*5-4: msg = u'[…]%s' % msg[-msg_limit*5+4:]
	send_msg(type, jid, nick, msg)

def set_locale(type, jid, nick, text):
	global CURRENT_LOCALE
	if len(text) >= 2:
		text = text.lower()
		lf = loc_folder % text
		if os.path.isfile(lf) or text == 'en':
			PT('bot_locale',text)
			msg = L('Locale set to: %s','%s/%s'%(jid,nick)) % text
			CURRENT_LOCALE = text
		else: msg = L('Locale not found!','%s/%s'%(jid,nick))
	else: msg = L('Current locale: %s','%s/%s'%(jid,nick)) % GT('bot_locale')
	send_msg(type, jid, nick, msg)

def shell_execute(*cmd):
	if len(cmd) == 2: rn = cmd[1]
	else: rn = ''
	cmd = cmd[0]
	if GT('paranoia_mode'): result = L('Command temporary blocked!',rn)
	else:
		tmp_file = '%s.tmp' % int(time.time())
		try:
			error_answ = os.system('%s > %s' % (cmd.encode('utf-8'),tmp_file))
			if not error_answ:
				try: body = readfile(tmp_file)
				except: body = L('Command execution error.',rn)
				if len(body):
					enc = chardet.detect(body)['encoding']
					result = remove_sub_space(unicode(body,enc))
				else: result = L('ok')
			else: result = L('Command execution error.',rn)
		except Exception, SM:
			try: SM = str(SM)
			except: SM = unicode(SM)
			result = L('I can\'t execute it! Error: %s',rn) % SM
		try: os.remove(tmp_file)
		except: pass
	return result

def concat(list): return ''.join(list)

def get_affiliation(jid,nick):
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nick:
			xtype = base[3]
			break
	return xtype

def comm_on_off(type, jid, nick, text):
	text = text.strip().lower().split()
	if text:
		cmd = text[0]
		cmds = text[1:]
		if cmd == 'on':
			if not cmds: msg = L('What enable?','%s/%s'%(jid,nick))
			else:
				not_found,enabled,already = [],[],[]
				for t in cmds:
					if not [True for c in comms if c[1]==t]: not_found.append(t)
					elif cur_execute_fetchone('select cmd from commonoff where room=%s and cmd=%s;',(jid,t)):
						cur_execute('delete from commonoff where room=%s and cmd=%s;',(jid,t))
						enabled.append(t)
					else: already.append(t)
				msg = []
				if enabled: msg.append(L('Enabled commands: %s','%s/%s'%(jid,nick)) % ', '.join(enabled))
				if already: msg.append(L('Not disabled commands: %s','%s/%s'%(jid,nick)) % ', '.join(already))
				if not_found: msg.append(L('Commands not found: %s','%s/%s'%(jid,nick)) % ', '.join(not_found))
				msg = '\n'.join(msg)
		elif cmd == 'off':
			if not cmds: msg = L('What disable?','%s/%s'%(jid,nick))
			else:
				not_found,disabled,already = [],[],[]
				for t in cmds:
					if not [True for c in comms if c[1]==t]: not_found.append(t)
					elif cur_execute_fetchone('select cmd from commonoff where room=%s and cmd=%s;',(jid,t)): already.append(t)
					else:
						cur_execute('insert into commonoff values (%s,%s);',(jid,t))
						disabled.append(t)
				msg = []
				if disabled: msg.append(L('Disabled commands: %s','%s/%s'%(jid,nick)) % ', '.join(disabled))
				if already: msg.append(L('Commands disabled before: %s','%s/%s'%(jid,nick)) % ', '.join(already))
				if not_found: msg.append(L('Commands not found: %s','%s/%s'%(jid,nick)) % ', '.join(not_found))
				msg = '\n'.join(msg)
		else: msg = L('Unknown item!','%s/%s'%(jid,nick))
	else:
		cmd = cur_execute_fetchall('select cmd from commonoff where room=%s;',(jid,))
		if cmd: msg = L('Disabled commands: %s','%s/%s'%(jid,nick)) % ', '.join([t[0] for t in cmd])
		else: msg = L('Disabled commands not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def reduce_spaces_all(text):
	text,t = text.strip(),''
	if len(text):
		for tmp in text:
			if tmp != ' ' or t[-1] != ' ': t += tmp
	return t

def status(type, jid, nick, text):
	if text == '': text = nick
	is_found = None
	for tmp in megabase:
		if tmp[0] == jid and tmp[1] == text:
			is_found = True
			break
	if is_found:
		realjid = getRoom(get_level(jid,text)[1])
		stat = cur_execute_fetchone('select message,status from age where jid=%s and room=%s and nick=%s',(realjid,jid,text))
		if stat:
			if stat[1]: msg = L('leave this room.','%s/%s'%(jid,nick))
			else:
				stat = stat[0].split('\n',4)
				if stat[3] != 'None': msg = stat[3]
				else: msg = 'online'
				if stat[4] != 'None': msg += ' ('+stat[4]+')'
				if stat[2] != 'None': msg += ' ['+stat[2]+'] '
				else: msg += ' [0] '
				if stat[0] != 'None' and stat[1] != 'None': msg += stat[0]+'/'+stat[1]
			if text != nick: msg = text + ' - '+msg
		else: msg = L('Not found!','%s/%s'%(jid,nick))
	else: msg = L('I can\'t see %s here...','%s/%s'%(jid,nick)) % text
	send_msg(type, jid, nick, msg)

def replacer(msg):
	def repl(t): return '%s\n' % re.findall('<div.*?>(.*?)</div>',t.group(0),re.S|re.I|re.U)[0]
	msg = rss_replace(msg)
	msg = re.sub(r'(<div.*?>).*?(</div>)',repl,msg,flags=re.S|re.I|re.U)
	for tmp in [['<br/>','\n'],['<br />','\n']]: msg = msg.replace(*tmp)
	msg = rss_del_html(msg)
	msg = rss_replace(msg)
	msg = rss_del_nn(msg)
	return msg.replace('...',u'…')

def vcs_info(type, jid, nick):
	if os.path.isfile(ul):
		try: msg = L('Last update:\n%s','%s/%s'%(jid,nick)) % readfile(ul).decode('utf-8').replace('\n\n','\n')
		except: msg = L('Error!','%s/%s'%(jid,nick))
	else: msg = L('File %s not found!','%s/%s'%(jid,nick)) % ul
	while msg[-1] in ['\n',' ']: msg = msg[:-1]
	if msg.count('\n') == 1: msg = msg.replace('\n',' ')
	send_msg(type, jid, nick, msg[:msg_limit])

def unhtml_raw(page,mode):
	for a in range(0,page.count('<style')):
		ttag = get_tag_full(page,'style')
		page = page.replace(ttag,'')

	for a in range(0,page.count('<script')):
		ttag = get_tag_full(page,'script')
		page = page.replace(ttag,'')

	page = rss_replace(page)
	if mode: page = replace_ltgt(page)
	else: page = rss_repl_html(page)
	page = rss_replace(page)
	page = rss_del_nn(page)
	page = page.replace('\n ','')
	return page

def unhtml(page): return unhtml_raw(page,None)

def unhtml_hard(page): return unhtml_raw(page,True)

def alias(type, jid, nick, text):
	text = text.strip()
	while '  ' in text: text = text.replace('  ',' ')
	mode = text.lower().split(' ',1)[0].strip(' ')
	try: cmd = text.split(' ',1)[1].split('=',1)[0].strip(' ')
	except: cmd = ''
	try: cbody = text.split(' ',1)[1].split('=',1)[1].strip(' ')
	except: cbody = ''
	msg = L('Mode %s not detected!','%s/%s'%(jid,nick)) % mode
	if mode in ['add','add_global']:
		am,amm = get_level(jid,nick)[0],-1
		tcmd = cbody.split(' ',1)[0].lower()
		for tmp in comms:
			if tmp[1] == tcmd:
				amm = tmp[0]
				break
		if amm < 0: msg = L('Command not found: %s','%s/%s'%(jid,nick)) % tcmd
		elif mode == 'add' and amm > am: msg = L('Not allowed create alias for: %s','%s/%s'%(jid,nick)) % tcmd
		elif mode == 'add_global' and am != 9: msg = L('Not allowed create global alias for: %s','%s/%s'%(jid,nick)) % tcmd
		else:
			gjid = jid if mode == 'add' else '*'
			fl = cur_execute_fetchone('select match from alias where room=%s and match =%s',(gjid,cmd))
			if fl:
				cur_execute('delete from alias where room=%s and match =%s',(gjid,cmd))
				msg = L('Updated:','%s/%s'%(jid,nick))
			else: msg = L('Added:','%s/%s'%(jid,nick))
			cur_execute('insert into alias values (%s,%s,%s)',(gjid,cmd,cbody))
			msg = '%s %s=%s' % (msg,cmd,cbody)
	if mode in ['del','del_global']:
		gjid = jid if mode == 'del' else '*'
		msg = L('Unable to remove %s','%s/%s'%(jid,nick)) % cmd
		fl = cur_execute_fetchone('select cmd from alias where room=%s and match =%s',(gjid,cmd))
		if fl:
			am,amm = get_level(jid,nick)[0],-1
			tcmd = fl[0].split(' ',1)[0].lower()
			for tmp in comms:
				if tmp[1] == tcmd:
					amm = tmp[0]
					break
			if mode == 'del' and amm > am: msg = L('Not allowed remove alias for: %s','%s/%s'%(jid,nick)) % tcmd
			elif mode == 'del_global' and am != 9: msg = L('Not allowed remove global alias for: %s','%s/%s'%(jid,nick)) % tcmd
			else:
				cur_execute('delete from alias where room=%s and match =%s',(gjid,cmd))
				msg = L('Removed: %s','%s/%s'%(jid,nick)) % cmd
	if mode=='show':
		if cmd == '':
			fl = cur_execute_fetchall('select match ,room from alias where room=%s or room=%s order by match ',(jid,'*'))
			if fl:
				aln = ', '.join([t[0] for t in fl if t[1] != '*'])
				alg = ', '.join([t[0] for t in fl if t[1] == '*'])
				if aln: msg = L('Aliases: %s','%s/%s'%(jid,nick)) % aln
				if alg:
					if aln: msg += '\n%s' % L('Global aliases: %s','%s/%s'%(jid,nick)) % alg
					else: msg = L('Global aliases: %s','%s/%s'%(jid,nick)) % alg
			else: msg = L('Aliases not found!','%s/%s'%(jid,nick))
		else:
			fl = cur_execute_fetchall('select match ,cmd,room from alias where (room=%s or room=%s) and match ilike %s order by match ',(jid,'*','%%%s%%'%cmd))
			if fl:
				aln = '\n'.join(['%s = %s' % (t[0],t[1]) for t in fl if t[2] != '*'])
				alg = '\n'.join(['%s = %s' % (t[0],t[1]) for t in fl if t[2] == '*'])
				if aln: msg = L('Aliases: %s','%s/%s'%(jid,nick)) % '\n%s' % aln
				if alg:
					if aln: msg += '\n%s' % L('Global aliases: %s','%s/%s'%(jid,nick)) % '\n%s' % alg
					else: msg = L('Global aliases: %s','%s/%s'%(jid,nick)) % '\n%s' % alg
			else: msg = L('Aliases not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def un_unix(*val):
	if len(val) == 2: rn = val[1]
	else: rn = ''
	val = val[0]
	tt = map(lambda q,a: q-a, time.gmtime(val), time.gmtime(0))[:6]
	ret = '%02d:%02d:%02d' % tuple(tt[3:6])
	if sum(tt[:3]):
		day_h,day_l = tt[2]/10%10,tt[2] % 10
		if day_h == 1: ret = L('%s days, %s',rn) % (tt[2],ret)
		else:
			if day_l in xrange(5,10): ret = L('%s days, %s',rn) % (tt[2],ret)
			elif day_l in xrange(2,5): ret = L('%s Days, %s',rn).lower() % (tt[2],ret)
			elif day_l == 1: ret = L('%s day, %s',rn) % (tt[2],ret)
	if sum(tt[:2]):
		if tt[1] in xrange(5,13): ret = L('%s months, %s',rn) % (tt[1],ret)
		elif tt[1] in xrange(2,5): ret = L('%s Months, %s',rn).lower() % (tt[1],ret)
		elif tt[1] == 1: ret = L('%s month, %s',rn) % (tt[1],ret)
	if tt[0]:
		ty = tt[0] % 100
		if ty >= 20: ty = ty % 10
		if ty in [0]+range(5,21): ret = L('%s years, %s',rn) % (tt[0],ret)
		elif ty in xrange(2,5): ret = L('%s Years, %s',rn).lower() % (tt[0],ret)
		else: ret = L('%s year, %s',rn) % (tt[0],ret)
	return ret

def close_age_null():
	cur_execute("delete from age where jid ilike '<temporary>%'")
	ccu = cur_execute_fetchall('select * from age where status=0 order by room')
	cur_execute('delete from age where status=0')
	for ab in ccu: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ab[0],ab[1],ab[2],ab[3],ab[4],1,ab[6],ab[7],ab[1].lower()))

def close_age():
	cur_execute('delete from age where jid ilike %s',('<temporary>%',))
	ccu = cur_execute_fetchall('select * from age where status=%s order by room',(0,))
	cur_execute('delete from age where status=%s', (0,))
	tt = int(time.time())
	for ab in ccu: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1,ab[6],ab[7],ab[1].lower()))

def sfind(mass,stri):
	for a in mass:
		if stri in a: return a
	return ''

def get_local_prefix(jid):
	lprefix = get_config(getRoom(jid),'prefix')
	if lprefix == None: return prefix
	return lprefix

def get_prefix(lprefix):
	if lprefix != '': return lprefix
	else: return 'absent'

def set_prefix(type, jid, nick, text):
	access_mode = get_level(jid,nick)[0]
	if access_mode >= 7:
		lprefix = get_config(getRoom(jid),'prefix')
		if text.lower() == 'none': lprefix = ''
		elif text.lower() == 'del': lprefix = prefix
		elif text != '': lprefix = text
		if lprefix == None: lprefix = prefix
		put_config(getRoom(jid),'prefix',lprefix)
		prf = L(get_prefix(lprefix),'%s/%s'%(jid,nick))
	else: prf = L(get_prefix(get_local_prefix(jid)),'%s/%s'%(jid,nick))
	send_msg(type, jid, nick, L('Command prefix: %s','%s/%s'%(jid,nick)) % prf)

def uptime(type, jid, nick): send_msg(type, jid, nick, L('Uptime: %s, Last session: %s','%s/%s'%(jid,nick)) % (un_unix(int(time.time()-starttime),'%s/%s'%(jid,nick)), un_unix(int(time.time())-sesstime,'%s/%s'%(jid,nick))))

def show_error(type, jid, nick, text):
	if text.lower() == 'clear': writefile(LOG_FILENAME,'')
	try: cmd = int(text)
	except: cmd = 1
	if os.path.isfile(LOG_FILENAME) and text.lower() != 'clear':
		log = readfile(LOG_FILENAME).decode('UTF')
		log = log.split('ERROR:')
		lll = len(log)
		if cmd > lll: cmd = lll
		msg = L('Total Error(s): %s\n','%s/%s'%(jid,nick)) % (lll-1)
		if text != '':
			for aa in range(lll-cmd,lll): msg += log[aa]+'\n'
		else: msg += ' '
		msg = msg[:-2]
	else: msg = L('No Errors','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def get_nick_by_jid(room, jid):
	for tmp in megabase:
		if tmp[0] == room and getRoom(tmp[4]) == jid: return tmp[1]
	return None

def get_jid_by_nick(room, nick):
	for tmp in megabase:
		if tmp[0] == room and tmp[1] == nick: return getRoom(tmp[4])
	return ''

def get_nick_by_jid_res(room, jid):
	for tmp in megabase:
		if tmp[0] == room and tmp[4] == jid: return tmp[1]
	return None

def info_lang(type, jid, nick, text):
	if get_config(getRoom(jid),'set_default_locale') != 'off': msg = L('In current MUC used %s locale for all users.','%s/%s'%(jid,nick)) % get_config(getRoom(jid),'set_default_locale').upper()
	else:
		if not text: text = nick
		if users_locale.has_key('%s/%s'%(jid,text)):
			cur_lang = users_locale['%s/%s'%(jid,text)]
			if locales.has_key(cur_lang): msg = L('For %s i\'ll use locale: %s','%s/%s'%(jid,nick)) % (text,cur_lang.upper())
			else: msg = L('For %s detected unknown locale: %s. Used default locale: %s','%s/%s'%(jid,nick)) % (text,cur_lang.upper(),CURRENT_LOCALE.upper())
		else: msg = L('Locale for %s not found! Used default locale: %s','%s/%s'%(jid,nick)) % (text,CURRENT_LOCALE.upper())
	send_msg(type, jid, nick, msg)

def info_whois(type, jid, nick, text):
	if text != '': msg = raw_who(jid,nick,text)
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def info_access(type, jid, nick):
	msg = raw_who(jid,nick,nick)
	send_msg(type, jid, nick, msg)

def raw_who(room,nick,text):
	access_mode = get_level(room,text)[0]
	if access_mode == -2: msg = L('Who do you need?','%s/%s'%(room,nick))
	else:
		realjid = get_level(room,text)[1]
		msg = L('Access level: %s','%s/%s'%(room,nick)) % access_mode
		msg += ', ' + [L('Ignored','%s/%s'%(room,nick)),L('Minimal','%s/%s'%(room,nick)),L('Visitor','%s/%s'%(room,nick)),L('Visitor and Member','%s/%s'%(room,nick)),L('Participant','%s/%s'%(room,nick)),L('Member','%s/%s'%(room,nick)), L('Moderator','%s/%s'%(room,nick)),L('Moderator and member','%s/%s'%(room,nick)),L('Admin','%s/%s'%(room,nick)),L('Owner','%s/%s'%(room,nick)),L('Bot\'s owner','%s/%s'%(room,nick))][access_mode+1]
		if realjid != 'None':
			msg = L('%s, jid detected','%s/%s'%(room,nick)) % msg
			if ddos_ignore.has_key(getRoom(realjid)): msg = '%s, %s' % (msg,L('temporary ignored (%s)','%s/%s'%(room,nick)) % un_unix(ddos_ignore[getRoom(realjid)][2]-time.time(),'%s/%s'%(room,nick)))
	return msg

def info_comm(type, jid, nick):
	access_mode,tmp = get_level(jid,nick)[0],[]
	for i in comms:
		if access_mode >= i[0]: tmp.append((i[0],i[1]))
	tmp.sort()
	msg = ''
	for j in range(0,access_mode+1):
		cm = [t[1] for t in tmp if t[0] == j]
		if cm: msg += u'\n• %s … %s' % (j,', '.join(cm))
	msg = L('Total commands: %s | Prefix: %s | Your access level: %s | Available commands: %s%s','%s/%s'%(jid,nick)) % (len(comms), L(get_prefix(get_local_prefix(jid)),'%s/%s'%(jid,nick)), access_mode, len(tmp), msg)
	send_msg(type, jid, nick, msg)

def helpme(type, jid, nick, text):
	text = text.strip().lower()
	if text == 'about': msg = u'Isida Jabber Bot | © 2oo9-%s Disabler Production Lab. | http://isida-bot.com' % str(time.localtime()[0]).replace('0','o')
	elif text in ['donation','donations']: msg = L('Send donation to: %sBest regards, %s','%s/%s'%(jid,nick)) % ('\nYandexMoney: 41001384336826\nWMZ: Z392970180590\nWMR: R378494692310\nWME: E164241657651\n','Disabler')
	elif text in [L('access','%s/%s'%(jid,nick)),'access']: msg = L('Bot has next access levels:\n-1 - ignored\n0 - minimal access\n1 - at least visitor and none\n2 - at least visitor and member\n3 - at least participant and none\n4 - at least participant and member\n5 - at least moderator and none\n6 - at least moderator and member\n7 - at least moderator and admin\n8 - at least moderator and owner\n9 - bot owner','%s/%s'%(jid,nick))
	elif len(text) > 1:
		tm,cm = [],[]
		for tmp in comms:
			if '\r' in tmp[4]: help_descr = L('Plugin %s. %s','%s/%s'%(jid,nick)) % (tmp[4].split('\r')[0],L(tmp[4].split('\r',1)[1],'%s/%s'%(jid,nick)))
			else: help_descr = L(tmp[4],'%s/%s'%(jid,nick))
			if tmp[1] == text:
				cm = (tmp[1],tmp[0],help_descr)
				break
			elif text in tmp[1].lower() or text in help_descr.lower(): tm.append((tmp[0], tmp[1], help_descr))
		if cm: msg = '%s. ' % cm[0].capitalize() + L('Access level: %s. %s','%s/%s'%(jid,nick)) % ('%s [%s]' % (cm[1],L(unlevl[int(cm[1])],'%s/%s'%(jid,nick))),cm[2])
		elif len(tm) == 1: msg = '%s. ' % tm[0][1].capitalize() + L('Access level: %s. %s','%s/%s'%(jid,nick)) % (tm[0][0],tm[0][2])
		elif not len(tm+cm): msg = L('"%s" not found','%s/%s'%(jid,nick)) % text
		else:
			tm.sort()
			msg = L('Prefix: %s, Available help for commands:\n','%s/%s'%(jid,nick)) % L(get_prefix(get_local_prefix(jid)),'%s/%s'%(jid,nick))
			for i in range(0,10):
				tmsg = []
				for tmp in tm:
					if tmp[0] == i and tmp[2] != '': tmsg.append(unicode(tmp[1]))
				if len(tmsg): msg += u'[%s]…%s\n' % (i,', '.join(tmsg))
	else: msg = L('%s Help for command: help command | Commands list: commands','%s/%s'%(jid,nick)) % (u'Isida Jabber Bot | http://isida-bot.com | © 2oo9-'+str(time.localtime()[0]).replace('0','o')+' Disabler Production Lab. |')
	send_msg(type, jid, nick, msg)

def bot_rejoin(type, jid, nick, text):
	global lastserver, lastnick
	text=unicode(text)
	if not text: text = jid
	if '\n' in text: text, passwd = text.split('\n', 1)
	else: passwd = ''
	if '@' not in text: text = '%s@%s' % (text,lastserver)
	if '/' not in text: text = '%s/%s' % (text,lastnick)
	lastserver = getServer(text.lower())
	lastnick = getResourse(text)
	if cur_execute_fetchall('select * from conference where room ilike %s;', ('%s/%%'%getRoom(text),)):
		sm = L('Rejoin by %s','%s/%s'%(jid,nick)) % nick
		leave(text, sm)
		time.sleep(1)
		zz = join(text, passwd)
		while unicode(zz)[:3] == '409':
			time.sleep(1)
			text += '_'
			zz = join(text, passwd)
		time.sleep(1)
		if zz != None:
			try:
				send_msg(type, jid, nick, zz['CAPTCHA'])
				answered, Error = None, None
				while not answered and not game_over:
					if is_start:
						cyc = cl.Process(1)
						if str(cyc) == 'None': cycles_unused += 1
						elif int(str(cyc)): cycles_used += 1
						else: cycles_unused += 1
					time.sleep(1)
					for tmp in pres_answer:
						if tmp[0]==zz['ID']:
							Error = tmp[1]
							pres_answer.remove(tmp)
							answered = True
							break
				if Error: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % Error)
				else:
					cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
					cur_execute('insert into conference values (%s,%s)',(text,passwd))
			except: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % zz)
		else:
			cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
			cur_execute('insert into conference values (%s,%s)',(text,passwd))
	else: send_msg(type, jid, nick, L('I have never been in %s','%s/%s'%(jid,nick)) % getRoom(text))

def bot_join(type, jid, nick, text):
	global lastserver, lastnick, pres_answer
	text = unicode(text)
	if not text or ' ' in getRoom(text): send_msg(type, jid, nick, L('Wrong arguments!','%s/%s'%(jid,nick)))
	else:
		if '\n' in text: text, passwd = text.split('\n', 1)
		else: passwd = ''
		if '@' not in text: text = '%s@%s' % (text,lastserver)
		if '/' not in text: text = '%s/%s' % (text,lastnick)
		old_text = '%s\n%s' % (text, passwd) if passwd else text
		if cur_execute_fetchone('select * from blacklist where room=%s', (getRoom(text),)): send_msg(type, jid, nick, L('Denied!','%s/%s'%(jid,nick)))
		else:
			lastserver = getServer(text.lower())
			lastnick = getResourse(text)
			lroom = text.lower().split('/')[0]
			cnf = cur_execute_fetchall('select * from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
			if not cnf:
				zz = join(text, passwd)
				while unicode(zz)[:3] == '409':
					time.sleep(1)
					text += '_'
					zz = join(text, passwd)
				if zz != None:
					try:
						send_msg(type, jid, nick, zz['CAPTCHA'])
						answered, Error = None, None
						while not answered and not game_over:
							if is_start:
								cyc = cl.Process(1)
								if str(cyc) == 'None': cycles_unused += 1
								elif int(str(cyc)): cycles_used += 1
								else: cycles_unused += 1
							time.sleep(1)
							for tmp in pres_answer:
								if tmp[0]==zz['ID']:
									Error = tmp[1]
									pres_answer.remove(tmp)
									answered = True
									break
						if Error: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % Error)
						else:
							cur_execute('insert into conference values (%s,%s)',(text,passwd))
							send_msg(type, jid, nick, L('Joined to %s','%s/%s'%(jid,nick)) % text)
					except: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % zz)
				else:
					cur_execute('insert into conference values (%s,%s)',(text,passwd))
					send_msg(type, jid, nick, L('Joined to %s','%s/%s'%(jid,nick)) % text)
			elif cur_execute_fetchone('select * from conference where room=%s;', (text,)): send_msg(type, jid, nick, L('I\'m already in %s with nick %s','%s/%s'%(jid,nick)) % (lroom, lastnick))
			else:
				zz = join(text, passwd)
				while unicode(zz)[:3] == '409':
					time.sleep(0.1)
					text += '_'
					zz = join(text, passwd)
				if zz != None:
					try:
						send_msg(type, jid, nick, zz['CAPTCHA'])
						answered, Error = None, None
						while not answered and not game_over:
							if is_start:
								cyc = cl.Process(1)
								if str(cyc) == 'None': cycles_unused += 1
								elif int(str(cyc)): cycles_used += 1
								else: cycles_unused += 1
							time.sleep(1)
							for tmp in pres_answer:
								if tmp[0]==zz['ID']:
									Error = tmp[1]
									pres_answer.remove(tmp)
									answered = True
									break
						if Error: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % Error)
						else:
							cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
							cur_execute('insert into conference values (%s,%s)',(text,passwd))
							send_msg(type, jid, nick, L('Joined to %s','%s/%s'%(jid,nick)) % text)
					except: send_msg(type, jid, nick, L('Error! %s','%s/%s'%(jid,nick)) % zz)
				else:
					cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
					cur_execute('insert into conference values (%s,%s)',(text,passwd))
					#time.sleep(1)
					#send_msg(type, jid, nick, L('Changed nick in %s to %s','%s/%s'%(jid,nick)) % (lroom,getResourse(text)))

def bot_leave(type, jid, nick, text):
	global lastserver
	domain = getServer(Settings['jid'])
	cnf = cur_execute_fetchall('select * from conference;')
	if len(cnf) == 1: send_msg(type, jid, nick, L('I can\'t leave last room!','%s/%s'%(jid,nick)))
	else:
		if text == '': text = jid
		if '@' not in text: text = '%s@%s' % (text,lastserver)
		if '\n' in text: text, _ = text.split('\n', 1)
		lastserver = getServer(text)
		text=unicode(text)
		lroom = text
		if is_owner(jid): nick = getName(jid)
		cnf = cur_execute_fetchall('select * from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
		if cnf:
			cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(text),))
			send_msg(type, jid, nick, L('Leave room %s','%s/%s'%(jid,nick)) % text)
			sm = L('Leave room by %s','%s/%s'%(jid,nick)) % nick
			leave(getRoom(text), sm)
			cur_execute('delete from hiden_rooms where room=%s',(getRoom(text),))
		else: send_msg(type, jid, nick, L('I have never been in %s','%s/%s'%(jid,nick)) % lroom)

def conf_limit(type, jid, nick, text):
	global msg_limit
	if text!='':
		try: msg_limit = int(text)
		except: msg_limit = default_msg_limit
	send_msg(type, jid, nick, L('Temporary message size limit %s','%s/%s'%(jid,nick)) % str(msg_limit))

def bot_plugin(type, jid, nick, text):
	global plname, plugins, execute, gtimer, gpresence, gmassage, giq_hook
	text = text.split()
	opt = text[0] if text else ''
	try: name = '%s.py' % text[1]
	except: name = ''
	msg = L('Wrong arguments!','%s/%s'%(jid,nick))
	pl_ignore = getFile(pliname,[])

	if opt == 'add' and os.path.isfile(pl_folder % name):
		if name in pl_ignore:
			pl_ignore.remove(name)
			writefile(pliname,str(pl_ignore))
		if name not in plugins: plugins.append(name)
		presence_control,message_control,message_act_control,iq_control,timer,execute,iq_hook = [],[],[],[],[],[],[]
		execfile(pl_folder % name)
		tmsg = ''
		for cm in execute:
			tmsg += '%s[%s], ' % (cm[1],cm[0])
			comms.append((cm[0],cm[1],cm[2],cm[3],L('Plugin %s. %s','%s/%s'%(jid,nick)) % (name[:-3],cm[4])))
		msg = L('Loaded plugin: %s','%s/%s'%(jid,nick)) % name[:-3]
		if tmsg: msg += L('\nAdd commands: %s','%s/%s'%(jid,nick)) % tmsg[:-2]
		for tmr in timer: gtimer.append(tmr)
		for tmp in presence_control: gpresence.append(tmp)
		for tmp in message_control: gmessage.append(tmp)
		for tmp in message_act_control: gactmessage.append(tmp)
		for tmp in iq_hook: giq_hook.append(tmp)
		giq_hook.sort()

	elif opt == 'del' and name in plugins:
		if name not in pl_ignore:
			pl_ignore.append(name)
			writefile(pliname,str(pl_ignore))
		plugins.remove(name)
		presence_control,message_control,message_act_control,iq_control,timer,execute,iq_hook = [],[],[],[],[],[],[]
		execfile(pl_folder % name)
		tmsg = ''
		for cm in execute:
			tmsg += '%s[%s], ' % (cm[1],cm[0])
			for i in comms:
				if i[1] == cm[1]: comms.remove(i)
		msg = L('Unloaded plugin: %s','%s/%s'%(jid,nick)) % name[:-3]
		if tmsg: msg += L('\nDel commands: %s','%s/%s'%(jid,nick)) % tmsg[:-2]
		for tmr in timer: gtimer.remove(tmr)
		for tmp in presence_control: gpresence.remove(tmp)
		for tmp in message_control: gmessage.remove(tmp)
		for tmp in message_act_control: gactmessage.remove(tmp)
		for tmp in iq_hook: giq_hook.remove(tmp)
		giq_hook.sort()

	elif opt == 'local':
		a = os.listdir(pl_folder % '')
		b = []
		for c in a:
			if c[-3:] == '.py' and c[0] != '.' and c != 'main.py': b.append(c[:-3].decode('utf-8'))
		b.sort()
		msg = L('Available plugins: %s','%s/%s'%(jid,nick)) % ', '.join(b)
		if len(pl_ignore):
			b = []
			for tmp in pl_ignore: b.append(tmp[:-3])
			msg += L('\nIgnored plugins: %s','%s/%s'%(jid,nick)) % ', '.join(b)

	elif opt == 'show':

		msg = L('Active plugins: %s','%s/%s'%(jid,nick)) % ', '.join([t[:-3] for t in plugins])
		msg[:-2]
		if len(pl_ignore):
			b = []
			for tmp in pl_ignore: b.append(tmp[:-3])
			msg += L('\nIgnored plugins: %s','%s/%s'%(jid,nick)) % ', '.join(b)

	plugins.sort()
	send_msg(type, jid, nick, msg)

def owner(type, jid, nick, text):
	global god
	text = text.lower().strip()
	do = text.split(' ',1)[0]
	try: nnick = text.split(' ',1)[1].lower()
	except:
		if do != 'show':
			send_msg(type, jid, nick, L('Wrong arguments!','%s/%s'%(jid,nick)))
			return
	if do == 'add':
		own = cur_execute_fetchone('select * from bot_owner where jid=%s',(nnick,))
		if not own:
			if '@' in nnick:
				j = xmpp.Presence(nnick, 'subscribed')
				j.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':capsNode,'ver':capsHash,'hash':'sha-1'})
				sender(j)
				j = xmpp.Presence(nnick, 'subscribe')
				j.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':capsNode,'ver':capsHash,'hash':'sha-1'})
				sender(j)
				msg = L('Append: %s','%s/%s'%(jid,nick)) % nnick
				cur_execute('insert into bot_owner values (%s)',(nnick,))
			else: msg = L('Wrong jid!','%s/%s'%(jid,nick))
		else: msg = L('%s is alredy in list!','%s/%s'%(jid,nick)) % nnick
	elif do == 'del':
		own = cur_execute_fetchone('select * from bot_owner where jid=%s',(nnick,))
		if own and nnick != god:
			cur_execute('delete from bot_owner where jid=%s',(nnick,))
			j = xmpp.Presence(nnick, 'unsubscribe')
			j.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':capsNode,'ver':capsHash,'hash':'sha-1'})
			sender(j)
			j = xmpp.Presence(nnick, 'unsubscribed')
			j.setTag('c', namespace=xmpp.NS_CAPS, attrs={'node':capsNode,'ver':capsHash,'hash':'sha-1'})
			sender(j)
			msg = L('Removed: %s','%s/%s'%(jid,nick)) % nnick
		else: msg = L('Not found!','%s/%s'%(jid,nick))
	elif do == 'show':
		own = cur_execute_fetchall('select * from bot_owner order by jid')
		msg = L('Bot owner(s): %s','%s/%s'%(jid,nick)) % ', '.join([t[0] for t in own])
	else: msg = L('Wrong arguments!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def ignore(type, jid, nick, text):
	global god
	text = text.lower().strip()
	do = text.split(' ',1)[0]
	try: nnick = text.split(' ',1)[1].lower()
	except:
		if do != 'show':
			send_msg(type, jid, nick, L('Wrong arguments!','%s/%s'%(jid,nick)))
			return
	if do == 'add':
		ign = cur_execute_fetchone('select * from bot_ignore where pattern=%s;',(nnick,))
		if not ign:
			cur_execute('insert into bot_ignore values (%s)',(nnick,))
			msg = L('Append: %s','%s/%s'%(jid,nick)) % nnick
		else: msg = L('%s alredy in list!','%s/%s'%(jid,nick)) % nnick
	elif do == 'del':
		ign = cur_execute_fetchone('select * from bot_ignore where pattern=%s and pattern!=%s;',(nnick,god))
		if ign:
			cur_execute('delete from bot_ignore where pattern=%s',(nnick,))
			msg = L('Removed: %s','%s/%s'%(jid,nick)) % nnick
		else: msg = L('Not found!','%s/%s'%(jid,nick))
	elif do == 'show':
		ign = cur_execute_fetchall('select * from bot_ignore order by pattern;')
		if ign: msg = ', '.join([t[0] for t in ign])
		else: msg = L('Empty!','%s/%s'%(jid,nick))
		msg = L('Ignore list: %s','%s/%s'%(jid,nick)) % msg
	else: msg = L('Wrong arguments!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def info_where(type, jid, nick):
	cnf = cur_execute_fetchall("select room from conference where split_part(room,'/',1) not in (select room from hiden_rooms as hrr);")
	len_cnf = cur_execute_fetchone('select count(*) from conference;')[0]
	hr_count = cur_execute_fetchone('select count(*) from hiden_rooms;')[0]
	msg = L('Active conference(s): %s','%s/%s'%(jid,nick)) % len_cnf
	wbase = []
	for jjid in cnf:
		cnt,rjid = 0,getRoom(jjid[0])
		for mega in megabase:
			if mega[0] == rjid: cnt += 1
		wbase.append((cnt, jjid[0]))
	wbase.sort(reverse=True)
	msg = '%s\n%s' % (msg,'\n'.join(['%s. %s [%s]' % (i[0]+1,i[1][1].split('\n')[0],i[1][0]) for i in enumerate(wbase)]))
	if hr_count: msg += L('\nHidden conference(s): %s','%s/%s'%(jid,nick)) % hr_count
	send_msg(type, jid, nick, msg)

def info_where_plus(type, jid, nick):
	cnf = cur_execute_fetchall("select room from conference where split_part(room,'/',1) not in (select room from hiden_rooms as hrr);")
	len_cnf = cur_execute_fetchone('select count(*) from conference;')[0]
	hr_count = cur_execute_fetchone('select count(*) from hiden_rooms;')[0]
	msg = L('Active conference(s): %s','%s/%s'%(jid,nick)) % len_cnf
	wbase = []
	for jjid in cnf:
		cnt,rjid,ra = 0,getRoom(jjid[0]),L('unknown','%s/%s'%(jid,nick))
		for mega in megabase:
			if mega[0] == rjid:
				cnt += 1
				if '%s/%s' % tuple(mega[0:2]) == jjid[0]: ra = L("%s/%s" % tuple(mega[2:4]))
		wbase.append((cnt, jjid[0], ra))
	wbase.sort(reverse=True)
	msg = '%s\n%s' % (msg,'\n'.join(['%s. %s (%s) [%s]' % (i[0]+1,i[1][1].split('\n')[0],i[1][2],i[1][0]) for i in enumerate(wbase)]))
	if hr_count: msg += L('\nHidden conference(s): %s','%s/%s'%(jid,nick)) % hr_count
	send_msg(type, jid, nick, msg)

def info(type, jid, nick):
	msg = L('Conference(s): %s (for more info use \'where\' command)\n','%s/%s'%(jid,nick)) % cur_execute_fetchone('select count(*) from conference;')[0]
	msg += L('Server: %s | Nick: %s\n','%s/%s'%(jid,nick)) % (lastserver,lastnick)
	msg += L('Message size limit: %s\n','%s/%s'%(jid,nick)) % msg_limit
	msg += L('Local time: %s\n','%s/%s'%(jid,nick)) % timeadd(tuple(time.localtime()))
	msg += L('Uptime: %s, Last session: %s','%s/%s'%(jid,nick)) % (un_unix(int(time.time()-starttime),'%s/%s'%(jid,nick)), un_unix(int(time.time())-sesstime,'%s/%s'%(jid,nick)))
	floods = get_config(getRoom(jid),'flood')
	censors = get_config(getRoom(jid),'censor')
	msg += L('\nFlood: %s | Censor: %s | Prefix: %s','%s/%s'%(jid,nick)) % (onoff(floods),onoff(censors),L(get_prefix(get_local_prefix(jid)),'%s/%s'%(jid,nick)))
	msg += L('\nExecuted threads: %s | Error(s): %s','%s/%s'%(jid,nick)) % (th_cnt,thread_error_count)
	msg += L('\nMessage in: %s | out: %s','%s/%s'%(jid,nick)) % (message_in,message_out)
	msg += L('\nPresence in: %s | out: %s','%s/%s'%(jid,nick)) % (presence_in,presence_out)
	msg += L('\nIq in: %s | out: %s','%s/%s'%(jid,nick)) % (iq_in,iq_out)
	msg += L('\nUnknown out: %s','%s/%s'%(jid,nick)) % unknown_out
	msg += L('\nCycles used: %s | unused: %s','%s/%s'%(jid,nick)) % (cycles_used,cycles_unused)
	if not GT('paranoia_mode'):
		try:
			memstat = tuple([get_size_human(int(t)*1024.0) for t in shell_execute('ps -o vsz,rss -p %s' % os.getpid(),'%s/%s'%(jid,nick)).split()[2:]])
			if not memstat or len(memstat) != 2: raise
		except: memstat = (L('Unknown','%s/%s'%(jid,nick)),L('Unknown','%s/%s'%(jid,nick)))
		msg += L('\nRAM for bot: %s (virtual), %s (real)','%s/%s'%(jid,nick)) % memstat
		if base_type == 'pgsql':
			try:
				memstat = tuple([get_size_human(int(t)*1024.0) for t in shell_execute('ps u -U postgres | grep "%s %s %s"' % (base_name,base_user,base_host)).split()[4:6]])
				if not memstat or len(memstat) != 2: raise
			except: memstat = (L('Unknown','%s/%s'%(jid,nick)),L('Unknown','%s/%s'%(jid,nick)))
			msg += L('\nRAM for database: %s (virtual), %s (real)','%s/%s'%(jid,nick)) % memstat
		elif base_type == 'mysql':
			# TODO: add detect ram usage for mysql base!
			memstat = (L('Unknown','%s/%s'%(jid,nick)),L('Unknown','%s/%s'%(jid,nick)))
			msg += L('\nRAM for database: %s (virtual), %s (real)','%s/%s'%(jid,nick)) % memstat
		elif base_type == 'sqlite3': msg += L('\nDatabase size: %s','%s/%s'%(jid,nick)) % get_size_human(os.path.getsize(sqlite_base))
	send_msg(type, jid, nick, msg)

def info_base(type, jid, nick):
	msg = L('What need find?','%s/%s'%(jid,nick))
	if nick != '':
		msg = ''
		fl = 1
		for base in megabase:
			if base[1] == (nick) and base[0].lower() == jid:
				msg = L('I see you as %s/%s','%s/%s'%(jid,nick)) % (base[2],base[3])
				break
	send_msg(type, jid, nick, msg)

def real_search_owner(type, jid, nick, text):
	if text:
		msg = L('Found:','%s/%s'%(jid,nick))
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if text.lower() in mega2.lower():
						msg += '\n%s - %s/%s' % (mega1[1],mega1[2],mega1[3])
						if mega1[4] != 'None': msg += ' (%s)' % mega1[4]
						msg += ' %s' % mega1[0]
						fl = 0
						break
		if fl: msg = L('\'%s\' not found!','%s/%s'%(jid,nick)) % text
	else: msg = L('What need find?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def real_search(type, jid, nick, text):
	if text:
		msg = L('Found:','%s/%s'%(jid,nick))
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if text.lower() in mega2.lower():
						msg += u'\n%s - %s/%s %s' % (mega1[1],mega1[2],mega1[3],mega1[0])
						fl = 0
						break
		if fl: msg = L('\'%s\' not found!','%s/%s'%(jid,nick)) % text
	else: msg = L('What do you need to find?','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def unescape(text):
	def fixup(m):
		text = m.group(0)
		if text[:2] == '&#':
			try:
				if text[:3] == '&#x': return unichr(int(text[3:-1], 16))
				else: return unichr(int(text[2:-1]))
			except ValueError: pass
		else:
			try: text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError: pass
		return text
	return re.sub('&#?\w+;', fixup, text)

def html_escape(text):
	def link(text): return '<a href="%s">%s</a>' % (text.group(0),text.group(0))
	#def email(text): return '<a href="mailto:%s">%s</a>' % (text.group(0),text.group(0))
	def brnbsp(text): return '<br/>' + '&nbsp;' * len(text.group(0))
	def nbsp(text): return '&nbsp;' * len(text.group(0))
	for tmp in (('&','&amp;'),('<','&lt;'),('>','&gt;'),('~','&tilde;'),('\t','&nbsp;'*8)): text = text.replace(tmp[0],tmp[1])
	text = re.sub(u'^(\ +)',nbsp,text)
	text = re.sub(u'http[s]?://[-a-zA-Z0-9а-яА-Я._/?&#=;@%:()+]+',link,text)
	#text = re.sub(u'[-a-zA-Z._0-9?:а-яА-Я]+@[-a-zA-Z._0-9а-яА-Я/?:]+',email,text)
	text = text.replace('\n','<br/>')
	text = re.sub('<br/>\ +',brnbsp,text)
	#for tmp in (('\"','&quot;'),('\'','&apos;')): text = text.replace(tmp[0],tmp[1])
	return text

def esc_max2(ms):
	for tmp in rlmas_min: ms = ms.replace(tmp[0],tmp[1])
	return ms

def esc_min2(ms):
	for tmp in rlmas_min: ms = ms.replace(tmp[1],tmp[0])
	return ms

def esc_min(ms):
	for tmp in rmass: ms = ms.replace(tmp[1],tmp[0])
	return ms

def rss_replace(ms):
	for tmp in lmass: ms = ms.replace(tmp[1],tmp[0])
	return unescape(esc_min(ms))

def rss_repl_del_html(ms,item):
	DS,SP,T = '<%s>','/%s',re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in T:
			if (tmp[:3] == '!--' and tmp[-2:] == '--') or tmp[-1:] == '/':
				pattern = DS % tmp
				pos = ms.find(pattern)
				ms = ms[:pos] + item + ms[pos+len(pattern):]
	T = re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in range(0,len(T)-1):
			pos = None
			TT = T[tmp].split(' ')[0]
			if TT and TT[0] != '/':
				try: pos = T.index(SP % TT,tmp)
				except: pass
				if pos:
					pat1,pat2 = DS % T[tmp],DS % T[pos]
					pos1 = ms.find(pat1)
					pos2 = ms.find(pat2,pos1)
					ms = ms[:pos1] + item + ms[pos1+len(pat1):pos2] + item + ms[pos2+len(pat2):]
	for tmp in ('hr','br','li','ul','img','dt','dd','p'):
		T = re.findall('<%s.*?>' % tmp, ms, re.S)
		for tmp1 in T: ms = ms.replace(tmp1,item,1)
	return ms

def rss_repl_html(ms): return rss_repl_del_html(ms,' ')

def rss_del_html(ms): return rss_repl_del_html(ms,'')

def remove_replace_ltgt(text,item):
	T = re.findall('<.*?>', text, re.S)
	for tmp in T: text = text.replace(tmp,item,1)
	return text

def replace_ltgt(text): return remove_replace_ltgt(text,' ')

def rss_del_nn(ms):
	ms = ms.replace('\r',' ').replace('\t',' ')
	while '\n ' in ms: ms = ms.replace('\n ','\n')
	while len(ms) and (ms[0] == '\n' or ms[0] == ' '): ms = ms[1:]
	while '\n\n' in ms: ms = ms.replace('\n\n','\n')
	while '  ' in ms: ms = ms.replace('  ',' ')
	while u'\n\n•' in ms: ms = ms.replace(u'\n\n•',u'\n•')
	while u'• \n' in ms: ms = ms.replace(u'• \n',u'• ')
	return ms.strip()

def html_encode(body):
	encidx = re.findall('encoding=["\'&]*(.*?)["\'& ]{1}',body[:1024])
	if encidx: enc = encidx[0]
	else:
		encidx = re.findall('charset=["\'&]*(.*?)["\'& ]{1}',body[:1024])
		if encidx: enc = encidx[0]
		else: enc = chardet.detect(body)['encoding']
	if body == None: body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while splitter in body: splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'): ttext+=tmp2
					else: ttext+='?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try: return smart_encode(body,enc)
		except: return L('Encoding error!')

def rss_flush(jid,link,break_point):
	tstop = cur_execute_fetchone('select hash from feed where room=%s and url=%s',(jid,link))
	if tstop: tstop = tstop[0] if base_type == 'pgsql' else eval(tstop[0])
	else: tstop = []
	if not break_point: break_point = tstop
	cur_execute('update feed set time=%s, hash=%s where room=%s and url=%s',(int(time.time()),break_point if base_type == 'pgsql' else str(break_point),jid,link))
	return tstop

def smart_concat(text):
	#while ' \n' in text: text = text.replace(' \n','\n')
	#while '\n ' in text: text = text.replace('\n ','\n')
	text = [' ']+text.split('\n')
	tmp = 1
	while tmp < len(text):
		if not (' ' in text[tmp] or '/' in text[tmp] or '.' in text[tmp] or '\\' in text[tmp]): text = text[:tmp-1]+[text[tmp-1]+' '+text[tmp]]+text[tmp+1:]
		else: tmp += 1
	return '\n'.join(text)

def rss(type, jid, nick, text):
	msg = 'rss show|add|del|clear|new|get'
	nosend = None
	text = text.split(' ')
	tl = len(text)
	if tl < 5: text.append('!')
	mode = text[0].lower() # show | add | del | clear | new | get
	if mode == 'add' and tl < 4: msg,mode = 'rss add [http://]url timeH|M [full|body|head][-url]',''
	elif mode == 'del' and tl < 2: msg,mode = 'rss del [http://]url',''
	elif mode == 'new' and tl < 4: msg,mode = 'rss new [http://]url max_feed_humber [full|body|head][-url]',''
	elif mode == 'get' and tl < 4: msg,mode = 'rss get [http://]url max_feed_humber [full|body|head][-url]',''
	if mode == 'clear':
		if get_level(jid,nick)[0] == 9 and tl > 1: tjid = text[1]
		else: tjid = jid
		msg = L('All RSS was cleared!','%s/%s'%(jid,nick))
		cur_execute('delete from feed where room=%s',(tjid,))
	elif mode == 'all':
		feedbase = cur_execute_fetchall('select * from feed;')
		msg = L('No RSS found!','%s/%s'%(jid,nick))
		if feedbase:
			msg = L('All schedule feeds:','%s/%s'%(jid,nick))
			for rs in feedbase:
				msg += '\n%s\t%s (%s) %s' % (getName(rs[4]),rs[0],rs[1],rs[2])
				try: msg += ' - %s' % disp_time(rs[3],'%s/%s'%(jid,nick))
				except: msg += ' - Unknown'
	elif mode == 'show':
		feedbase = cur_execute_fetchall('select * from feed where room=%s;',(jid,))
		msg = L('No RSS found!','%s/%s'%(jid,nick))
		if feedbase:
			msg = ''
			for rs in feedbase:
				msg += '\n%s (%s) %s' % tuple(rs[0:3])
				try: msg += ' - %s' % disp_time(rs[3],'%s/%s'%(jid,nick))
				except: msg += ' - Unknown'
			if len(msg): msg = L('Schedule feeds for %s:%s','%s/%s'%(jid,nick)) % (jid,msg)
			else: msg = L('Schedule feeds for %s not found!','%s/%s'%(jid,nick)) % jid
	elif mode == 'add':
		mdd = ['full','body','head']
		if text[3].split('-')[0] not in mdd:
			send_msg(type, jid, nick, L('Mode %s not detected!','%s/%s'%(jid,nick)) % text[3])
			return
		link = text[1]
		if not re.findall('^http(s?)://',link[:10]): link = 'http://%s' % link
		cur_execute('delete from feed where room=%s and url=%s;',(jid,link))
		timetype = text[2][-1:].lower()
		if not timetype in ('h','m'): timetype = 'h'
		try: ofset = int(text[2][:-1])
		except: ofset = 4
		if timetype == 'm' and ofset < GT('rss_min_time_limit'): timetype = '%sm' % GT('rss_min_time_limit')
		else: timetype = str(ofset)+timetype
		cur_execute('insert into feed values (%s,%s,%s,%s,%s,%s,%s);',(link, timetype, text[3], int(time.time()), getRoom(jid),[] if base_type == 'pgsql' else '[]',''))
		msg = L('Add feed to schedule: %s (%s) %s','%s/%s'%(jid,nick)) % (link,timetype,text[3])
		rss(type, jid, nick, 'get %s 1 %s' % (link,text[3]))
	elif mode == 'del':
		link = text[1]
		if not re.findall('^http(s?)://',link[:10]): link = 'http://%s' % link
		msg = L('Can\'t find in schedule: %s','%s/%s'%(jid,nick)) % link
		fdb = cur_execute_fetchall('select * from feed where room=%s and url=%s;',(jid,link))
		if fdb:
			cur_execute('delete from feed where room=%s and url=%s;',(jid,link))
			msg = L('Delete feed from schedule: %s','%s/%s'%(jid,nick)) % link
	elif mode in ['new','get']:
		link = text[1]
		if not re.findall('^http(s?)://',link[:10]): link = 'http://%s' % link
		if cur_execute_fetchone('select * from feed where room=%s and url=%s;',(jid,link)):			
			body, result = get_opener(enidna(link))
			modified,need_update_feed = '',True
			if result:
				modified = body.headers.get('last-modified',None)
				if not modified: modified = get_tag(load_page_size(link, 1024),'updated')
			if modified:
				changed = cur_execute_fetchone('select changed from feed where room=%s and url=%s;',(jid,link))[0]
				if modified == changed: need_update_feed = False
				else: cur_execute('update feed set changed=%s where room=%s and url=%s',(modified,jid,link))
			is_rss_aton = 0
			if need_update_feed:
				try:
					req = urllib2.Request(link.encode('utf-8'))
					req.add_header('User-Agent',GT('user_agent'))
					feed = urllib2.urlopen(url=req,timeout=GT('rss_get_timeout')).read(GT('size_overflow'))
				except: feed = L('Unable to access server!','%s/%s'%(jid,nick))
				fc = feed[:256]
				if '<?xml version=' in fc:
					if '<feed' in fc:
						is_rss_aton = 2
						t_feed = feed.split('<title>')
						feed = t_feed[0]
						for tmp in t_feed[1:]:
							tm = tmp.split('</title>',1)
							if ord(tm[0][-1]) == 208: tm[0] = tm[0][:-1] + '...'
							feed += '<title>%s</title>%s' % tuple(tm)
					elif '<rss' in fc or '<rdf' in fc: is_rss_aton = 1
					feed = html_encode(feed)
					feed = re.sub('(<span.*?>.*?</span>)','',feed)
					feed = re.sub('(<div.*?>)','',feed)
					feed = re.sub('(</div>)','',feed)
			else: feed = L('New feeds not found!','%s/%s'%(jid,nick))
			if is_rss_aton and feed != L('Encoding error!','%s/%s'%(jid,nick)) and feed != L('Unable to access server!','%s/%s'%(jid,nick)):
				if is_rss_aton == 1:
					if '<item>' in feed: fd = feed.split('<item>')
					else: fd = feed.split('<item ')
					feed = [fd[0]]
					for tmp in fd[1:]: feed.append(tmp.split('</item>')[0])
				else:
					if '<entry>' in feed: fd = feed.split('<entry>')
					else: fd = feed.split('<entry ')
					feed = [fd[0]]
					for tmp in fd[1:]: feed.append(tmp.split('</entry>')[0])
				if len(text) > 2 and text[2].isdigit(): lng = int(text[2])
				else: lng = len(feed)-1
				if len(feed)-1 <= lng: lng = len(feed)-1
				if lng > GT('rss_max_feed_limit'): lng = GT('rss_max_feed_limit')
				elif len < 1: lng = 1
				if len(text) > 3: submode = text[3]
				else: submode = 'full'
				msg = L('Feeds for','%s/%s'%(jid,nick))+' '
				if 'url' in submode.split('-'): submode,urlmode = submode.split('-')[0],True
				else:
					urlmode = None
					msg += link+' '
				msg += get_tag(feed[0],'title')
				try:
					break_point = []
					for tmp in feed[1:GT('rss_max_feed_limit')+1]:
						ttitle = get_tag(tmp,'title').replace('&lt;br&gt;','\n')
						break_point.append(hashlib.md5(ttitle.encode('utf-8')).hexdigest())
					tstop = rss_flush(jid,link,break_point)
					t_msg, new_count = [], 0
					for mmsg in feed[1:GT('rss_max_feed_limit')+1]:
						ttitle = get_tag(mmsg,'title').replace('&lt;br&gt;','\n')
						if mode == 'get' or not (hashlib.md5(ttitle.encode('utf-8')).hexdigest() in tstop):
							if is_rss_aton == 1: tbody,turl = get_tag(mmsg,'description').replace('&lt;br&gt;','\n'),get_tag(mmsg,'link')
							else:
								tbody = get_tag(mmsg,'content').replace('&lt;br&gt;','\n')
								try:
									tu1 = mmsg.find('href=\"',mmsg.index('<link'))+6
									tu2 = mmsg.find('\"',tu1)
									turl = mmsg[tu1:tu2].replace('&lt;br&gt;','\n')
								except: turl = 'URL %s' % L('Not found!','%s/%s'%(jid,nick))
							tsubj,tmsg,tlink = '','',''
							if submode == 'full': tsubj,tmsg = replacer(ttitle),replacer(tbody.replace('<li>',u'\n♦ ').replace('</li>',''))
							elif submode == 'body': tmsg = replacer(tbody.replace('<li>',u'\n♦ ').replace('</li>',''))
							elif submode == 'head': tsubj = replacer(ttitle)
							else: return
							if urlmode: tlink = urllib.unquote(turl.encode('utf8')).decode('utf8','ignore')
							t_msg.append((tsubj.replace('\n','; '),smart_concat(tmsg),tlink))
							new_count += 1
							if new_count >= lng: break
					if new_count:
						t_msg.reverse()
						tmp = ''
						for tm in t_msg: tmp += '!'.join(tm)
						if len(tmp+msg)+len(t_msg)*12 >= msg_limit:
							over = 100 * msg_limit / (len(tmp+msg)+len(t_msg)*12.0) # overflow in persent
							tt_msg = []
							for tm in t_msg:
								tsubj,tmsg,tlink = tm
								cut = int(len(tsubj+tmsg+tlink)/100*over)
								if cut < len(tlink): tsubj,tmsg,tlink = u'%s[…]' % tsubj[:cut],'',''
								elif cut < len(tsubj+tlink): tsubj,tmsg = u'%s[…]' % tsubj[:cut-len(tlink)],''
								else: tmsg = u'%s[…]' % tmsg[:cut-len(tlink+tsubj)]
								tt_msg.append((tsubj,tmsg,tlink))
							t_msg = tt_msg
						tmp = ''
						for tm in t_msg:
							if submode == 'full': tmp += u'\n• %s\n%s' % tm[0:2]
							elif submode == 'body': tmp += u'\n• %s' % tm[1]
							elif submode == 'head': tmp += u'\n• %s' % tm[0]
							if len(tm[2]): tmp += '\n'+tm[2]
						msg = unhtml(msg+tmp)
					elif mode == 'new':
						if text[4] == 'silent': nosend = True
						else: msg = L('New feeds not found!','%s/%s'%(jid,nick))
				except Exception,SM:
					rss_flush(jid,link,None)
					if text[4] == 'silent': nosend = True
					else: msg = L('Error! %s','%s/%s'%(jid,nick)) % SM
			else:
				rss_flush(jid,link,None)
				if text[4] == 'silent': nosend = True
				else:
					if need_update_feed:
						if feed in [L('Encoding error!','%s/%s'%(jid,nick)),L('Unable to access server!','%s/%s'%(jid,nick))]: title = feed
						else: title = html_encode(get_tag(feed,'title'))
						msg = L('Bad url or rss/atom not found at %s - %s','%s/%s'%(jid,nick)) % (link,title)
					else: msg = feed
		else: msg = L('Not found!','%s/%s'%(jid,nick))
	if not nosend: send_msg(type, jid, nick, msg)

def configure(type, jid, nick, text):
	text = text.lower().replace('\n',' ').replace('\r',' ').replace('\t',' ')
	while '  ' in text: text = text.replace('  ',' ')
	text = text.split(' ',1)
	to_conf = text[0]
	param = text[1] if len(text) == 2 else ''
	if to_conf in ['show','item','items','it','sh']:
		if param in ['status','info','st']:
			tmp = config_prefs.keys()
			tmp.sort()
			msg = ''
			for t in tmp: msg += '\n[%s] - ' % t + L(config_prefs[t][0],'%s/%s'%(jid,nick)) % onoff(get_config(getRoom(jid),t))
			msg = L('Current status: %s','%s/%s'%(jid,nick)) % msg
		elif param in config_prefs: msg = L(config_prefs[param][0],'%s/%s'%(jid,nick)) % onoff(get_config(getRoom(jid),param))
		else:
			tmp = config_prefs.keys()
			tmp.sort()
			msg = L('Available items: %s','%s/%s'%(jid,nick)) % ', '.join(tmp)
	elif to_conf == 'help' or not to_conf:
		if param in config_prefs: msg = L(config_prefs[param][1],'%s/%s'%(jid,nick))
		elif not param:
			tmp = config_prefs.keys()
			tmp.sort()
			msg = L('Available items: %s','%s/%s'%(jid,nick)) % ', '.join(tmp)
		else:
			cps = config_prefs.keys()
			cps.sort()
			tmp = [cp for cp in cps if param in cp]
			if tmp:
				msg = L('Available items: %s','%s/%s'%(jid,nick)) % ', '.join(tmp)
			else:
				msg = L('Help for %s not found!','%s/%s'%(jid,nick)) % param
	elif to_conf in config_prefs:
		if param.lower() in ['show','item','items','it','sh']:
			msg = ''
			if config_prefs[to_conf][2]:
				for tmp in config_prefs[to_conf][2]: msg += ['%s (%s), ' % (onoff_no_tr(tmp),onoff(tmp)),'%s, ' % onoff_no_tr(tmp)][onoff_no_tr(tmp) == onoff(tmp)]
			else: msg += L('text field','%s/%s'%(jid,nick)) + '  '
			msg = L('Available items: %s','%s/%s'%(jid,nick)) % msg[:-2]
		elif param == '': msg = L(config_prefs[to_conf][0],'%s/%s'%(jid,nick)) % onoff(get_config(getRoom(jid),to_conf))
		else:
			if not config_prefs[to_conf][2]: ssta = param
			else:
				ssta = get_config(getRoom(jid),to_conf)
				if (param.lower() in [L('on','%s/%s'%(jid,nick)),'on','true']) and not param in config_prefs[to_conf][2]: param = True
				elif (param.lower() in [L('off','%s/%s'%(jid,nick)),'off','false','none']) and not param in config_prefs[to_conf][2]: param = False
				else: param = param.lower()
				if param in config_prefs[to_conf][2]: ssta = param
				else: ssta = ''
			if len(str(ssta)):
				put_config(getRoom(jid),to_conf,ssta)
				msg = L(config_prefs[to_conf][0],'%s/%s'%(jid,nick)) % onoff(ssta)
			else: msg = L('Unknown item!','%s/%s'%(jid,nick))
	else: msg = L('Unknown item!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def muc_filter_lock(type, jid, nick, text):
	realjid = getRoom(get_level(jid,nick)[1])
	tmp = cur_execute_fetchall('select * from muc_lock where room=%s and jid=%s', (jid,realjid))
	if text in ['on','off']:
		if tmp: cur_execute('delete from muc_lock where room=%s and jid=%s', (jid,realjid))
		if text == 'on':
			cur_execute('insert into muc_lock values (%s,%s)', (jid, realjid))
			st = L('on','%s/%s'%(jid,nick))
		else: st = L('off','%s/%s'%(jid,nick))
	elif tmp: st = L('on','%s/%s'%(jid,nick))
	else: st = L('off','%s/%s'%(jid,nick))
	msg = L('Ignore messages from unaffiliated participants in private - %s','%s/%s'%(jid,nick)) % st
	send_msg(type, jid, nick, msg)

def get_opener(page_name, parameters=None):
	socket.setdefaulttimeout(GT('rss_get_timeout'))
	try:
		proxy_support = urllib2.ProxyHandler({'http' : 'http://%(user)s:%(password)s@%(host)s:%(port)d' % http_proxy})
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		urllib2.install_opener(opener)
	except: opener = urllib2.build_opener(urllib2.HTTPHandler)
	opener.addheaders = [('User-agent', GT('user_agent'))]
	if parameters: page_name += urllib.urlencode(parameters)
	try: data, result = opener.open(page_name), True
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		data, result = L('Error! %s') % SM.replace('>','').replace('<','').capitalize(), False
	return data, result

def load_page_size(page_name, page_size, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result: return data.read(page_size)
	else: return data

def load_page(page_name, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result: return data.read(GT('size_overflow'))
	else: return data

config_prefs = {'url_title': ['Url title is %s', 'Automatic show title of urls in conference', [True,False], False],
				'content_length': ['Content length %s', 'Automatic show lenght of content in conference', [True,False], False],
				'censor': ['Censor is %s', 'Censor', [True,False], False],
				#'censor_message': ['Censor message is %s', 'Censor message', None, censor_text],
				'censor_warning': ['Censor warning is %s', 'Warning for moderators and higher' ,[True,False], False],
				'censor_action_member': ['Censor action for member is %s', 'Censor action for member', ['off','visitor','kick','ban'], 'off'],
				'censor_action_non_member': ['Censor action for non member is %s', 'Censor action for non member', ['off','visitor','kick','ban'], 'off'],
				'censor_custom': ['Custom censor is %s', 'Custom censor', [True,False], False],
				'censor_custom_rules': ['Custom rules for censor is %s', 'Custom rules for censor', None, '\n'],
				'parse_define': ['Parse define is %s', 'Automatic parse definition via google', ['off','full','partial'], 'off'],
				'clear_answer':['Clear notification by %s','Clear notification by presence or message', ['presence','message'],'presence'],
				'smiles':['Smiles in logs is %s', 'Smiles in logs', ['off'] + smiles_dirs, 'off'],
				'autoturn': ['Autoturn layout of text is %s', 'Turn text from one layout to another.', [True,False], False],
				'make_stanza_jid_count':['Jid\'s per stanza for affiliations in backup is %s','Count of jid\'s per stanza for affiliations change in backup',None,'100'],
				'acl_multiaction': ['ACL multiaction is %s', 'Execute more than one action per pass in ACL.', [True,False], False],
				'paste_xhtml_images': ['Paste xhtml images %s', 'Detect and paste xhtml images in messages', [True,False], True],
				#'use_default_locale': ['Use default locale %s', 'Ignore locale settings and use default bot locale', [True,False], False],
				'set_default_locale': ['Set default locale %s', 'Ignore users locale and use one locale for all users in room', ['off','en'] + [tmp[:-4] for tmp in os.listdir(loc_folder[:-6]) if tmp[-4:]=='.txt'], 'off'],
				'store_users_url': ['Store Users URL %s', 'Store Users URL', [True,False], True],
				'trusted_servers': ['Trusted servers %s', 'Servers list marked as trusted. They are excluded from any actions with servers', None, ''],
				'visitor_action': ['Action for visitors is %s', 'Action for visitors', ['off','kick','ban'], 'off'],
				'visitor_action_time': ['Time for visitors action %s', 'Time for visitors action', None, '1800'],
				'ai': ['AI is %s', 'AI parser for messages', [True,False], True],

				# MUC-Filter messages

				'muc_filter': ['Muc filter is %s', 'Message filter for participants', [True,False], False],
				'muc_filter_mute_chat': ['Mute all private messages %s', 'Mute all private messages', [True,False], False],
				'muc_filter_mute_groupchat': ['Mute all public messages %s', 'Mute all public messages', [True,False], False],
				'muc_filter_mute_repeat': ['Count of messages for action %s', 'Count of messages for action', None, '3'],
				'muc_filter_mute_repeat_action': ['Action for messages overflow %s', 'Action for messages overflow', ['off','kick','ban'], 'off'],
				'muc_filter_newbie': ['Mute newbie %s', 'Mute all messages from newbie', [True,False], False],
				'muc_filter_newbie_repeat': ['Count of messages for newbie %s', 'Count of messages for newbie for action', None, '3'],
				'muc_filter_newbie_repeat_action': ['Action for messages overflow for newbie %s', 'Action for messages overflow for newbie', ['off','kick','ban'], 'off'],
				'muc_filter_newbie_time': ['Mute newbie time %s', 'Time of mute all messages from newbie', None, '60'],
				'muc_filter_adblock': ['Adblock muc filter is %s', 'Adblock filter', ['off','visitor','kick','ban','replace','mute'], 'off'],
				'muc_filter_repeat': ['Repeat muc filter is %s', 'Repeat same messages filter', ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_match': ['Match muc filter is %s', 'Repeat text in message filter', ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_large': ['Large muc filter is %s', 'Large message filter', ['off','visitor','kick','ban','paste','truncate','mute'], 'off'],
				'muc_filter_censor': ['Censor muc filter is %s', 'Censor filter', ['off','visitor','kick','ban','replace','mute'], 'off'],
				'muc_filter_adblock_raw': ['Raw adblock muc filter is %s', 'Raw adblock filter', ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_censor_raw': ['Raw censor muc filter is %s', 'Raw censor filter', ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_raw_percent': ['Persent of short words for raw actions is %s', 'Persent of short words for raw actions', None, '40'],
				'muc_filter_reduce_spaces_msg': ['Reduce spaces in message %s', 'Reduce duplicates of spaces in message', [True,False], False],

				# MUC-Filter presence

				'muc_filter_history': ['Block joins without history %s', 'Block joins without history', [True,False], True],
				'muc_filter_history_ban': ['Ban joins without history %s', 'Additional ban joins without history', [True,False], True],
				'muc_filter_adblock_prs': ['Adblock muc filter for presence is %s', 'Adblock filter for presence', ['off','kick','ban','replace','mute'], 'off'],
				'muc_filter_rejoin': ['Repeat join muc filter is %s', 'Repeat join muc filter', [True,False], False],
				'muc_filter_whitelist': ['Whitelist is %s', 'Whitelist via muc filter', [True,False], False],
				'muc_filter_blacklist': ['Blacklist is %s', 'Blacklist via muc filter', [True,False], False],
				'muc_filter_blacklist_rules_jid': ['Blacklist rules for jid\'s %s', 'Jid\'s rules for blacklist via muc filter.', None, ''],
				'muc_filter_blacklist_rules_nick': ['Blacklist rules for nick\'s %s', 'Nick\'s rules for blacklist via muc filter.', None, ''],
				'muc_filter_newline': ['New line in presence muc filter is %s', 'New line muc filter', ['off','kick','ban','mute','replace'], 'off'],
				'muc_filter_newline_count': ['New line count in presence muc filter is %s', 'Count of new line muc filter', None, '2'],
				'muc_filter_newline_msg': ['New line in message muc filter is %s', 'New line muc filter', ['off','kick','ban','mute','replace'], 'off'],
				'muc_filter_newline_msg_count': ['New line count in message muc filter is %s', 'Count of new line muc filter', None, '2'],
				'muc_filter_repeat_prs': ['Repeat presence muc filter is %s', 'Repeat presence muc filter', ['off','kick','ban','mute'], 'off'],
				'muc_filter_large_nick': ['Large nick muc filter is %s', 'Large nick muc filter', ['off','visitor','kick','ban','truncate','mute'], 'off'],
				'muc_filter_large_status': ['Large status muc filter is %s', 'Large status muc filter', ['off','visitor','kick','ban','truncate','mute'], 'off'],
				'muc_filter_censor_prs': ['Censor muc filter for presence is %s', 'Censor muc filter for presence', ['off','kick','ban','replace','mute'], 'off'],
				'muc_filter_deny_hash': ['Deny by hash %s', 'Lock joins via hash', [True,False], False],
				'muc_filter_deny_hash_list': ['Deny hashes list %s', 'Hashes list for lock joins', None, ''],
				'muc_filter_hash': ['Hash. Check activity %s', 'Actions by hash activity', [True,False], False],
				'muc_filter_hash_ban_by_rejoin': ['Hash. Ban if hash activity %s', 'Actions for ban by hash activity', [True,False], True],
				'muc_filter_hash_ban_by_rejoin_timeout': ['Hash. Timeout for clean hash activity %s', 'Time period for clean hash activity', None, '600'],
				'muc_filter_hash_ban_server_by_rejoin': ['Hash. Ban server by hash activity %s', 'Ban server by hash activity', [True,False], True],
				'muc_filter_hash_ban_server_by_rejoin_exception': ['Hash. Exception for ban servers %s', 'Exception for ban servers', None, ''],
				'muc_filter_hash_ban_server_by_rejoin_notify_jid': ['Hash. Jid\'s for servers ban notify %s', 'Jid\'s for servers ban notify', None, ''],
				'muc_filter_hash_ban_server_by_rejoin_rejoins': ['Hash. Count of rejoins from server for ban %s', 'Count of rejoins from server for ban', None, '5'],
				'muc_filter_hash_ban_server_by_rejoin_timeout': ['Hash. Timeout of rejoins from server for ban %s', 'Timeout of rejoins from server for ban', None, '60'],
				'muc_filter_hash_time': ['Hash. Time for events %s', 'Time period for events', None, '20'],
				'muc_filter_hash_events': ['Hash. Events count %s', 'Events count per time period', None, '10'],
				'muc_filter_hash_action': ['Hash. Action type %s', 'Type of action', ['whitelist','lock by hash'], 'whitelist'],
				'muc_filter_hash_action_time': ['Hash. Time to disable action %s', 'Time to disable action', None, '1800'],
				'muc_filter_hash_action_current': ['Hash. Action for already joined %s', 'Action for already joined', ['off','kick','ban'], 'off'],
				'muc_filter_censor_prs_raw': ['Raw censor muc filter for presence is %s', 'Raw censor muc filter for presence', ['off','kick','ban','mute'], 'off'],
				'muc_filter_adblock_prs_raw': ['Raw adblock muc filter for presence is %s', 'Raw adblock filter for presence', ['off','kick','ban','mute'], 'off'],
				'muc_filter_reduce_spaces_prs': ['Reduce spaces in presence %s', 'Reduce duplicates of spaces in presence', [True,False], False],
				#'muc_filter_caps': ['Limitation by caps %s', 'Limitation to join by caps', [True,False], False],
				'muc_filter_caps_list': ['Type of list %s', 'Type of list for caps', ['off','black','white'], 'off'],
				'muc_filter_caps_white': ['Whitelist %s', 'Whitelist for caps', None, '\n'],
				'muc_filter_caps_black': ['Blacklist %s', 'Blacklist for caps', None, '\n'],
				#'muc_filter_caps_smart': ['Smart lists %s', 'Smart lists for caps', [True,False], False],
				#'muc_filter_caps_white_smart': ['Smart whitelist %s', 'Smart whitelist for caps', None, '\n'],
				#'muc_filter_caps_black_smart': ['Smart blacklist %s', 'Smart blacklist for caps', None, '\n'],
				'muc_filter_validate_action': ['Action for invalid items %s', 'Action for invalid items', ['off','ban','ban server'], 'ban'],
				'muc_filter_validate_nick': ['Validate nick %s', 'Validate nick', [True,False], True],
				'muc_filter_validate_login': ['Validate login %s', 'Validate login', [True,False], True],
				'muc_filter_validate_resource': ['Validate resource %s', 'Validate resource', [True,False], True],
				'muc_filter_validate_caps_node': ['Validate caps node %s', 'Validate caps node', [True,False], True],
				'muc_filter_validate_caps_version': ['Validate caps version %s', 'Validate caps version', [True,False], True],
				'muc_filter_validate_count': ['Count of invalid items %s', 'Count of invalid items for action', None, '4'],
				'muc_filter_validate_ban_server_exception': ['Exception for ban servers %s', 'Exception for ban servers', None, ''],
				'muc_filter_validate_ban_server_notify_jid': ['Jid\'s for servers ban notify %s', 'Jid\'s for servers ban notify', None, ''],
				'muc_filter_fast_join': ['Lock fast joins %s', 'Lock fast joins', [True,False], True],
				'muc_filter_fast_join_count': ['Count of fast joins %s', 'Count of fast joins', None, '3'],
				'muc_filter_fast_join_time': ['Time for count of fast joins %s', 'Time for count of fast joins', None, '5'],

				# Bomb

				'bomb': ['Bomb. Allow take a bomb %s', 'Allow take a bomb in current conference', [True,False], True],
				'bomb_fault': ['Bomb. Allow random unexplosive bombs %s', 'Allow some times take unexplosive bombs', [True,False], True],
				'bomb_fault_persent': ['Bomb. Persent of fault bombs %s', 'Persent of fault bombs', None, '25'],
				'bomb_random': ['Bomb. Allow bot take a bomb to random user %s', 'Allow bot take a bomb to random user', [True,False], False],
				'bomb_random_active': ['Bomb. Allow random bombs only in active room %s', 'Allow random bombs only in active room', [True,False], True],
				'bomb_random_active_timer': ['Bomb. Time for detect room as unactive %s', 'Time for detect room as unactive', None, '1200'],
				'bomb_random_timer': ['Bomb. Time between random bombs %s', 'Time between random bombs', None, '1800'],
				'bomb_random_timer_persent': ['Bomb. Persent of mistakes for time between random bombs %s', 'Persent of mistakes for time between random bombs', None, '25'],
				'bomb_random_timer_skip_persent': ['Bomb. Persent of skiped random bombs %s', 'Persent of mistakes skiped random bombs', None, '25'],
				'bomb_timer': ['Bomb. Timer is %s', 'Time to deactivate a bomb', None, '45'],
				'bomb_wire': ['Bomb. Wire count is %s', 'Wire count for bomb', None, '4'],
				'bomb_action': ['Bomb. Action for bomb explode %s', 'Type of action for bomb explode', ['off','kick'], 'kick'],
				'bomb_action_level': ['Bomb. Don\'t use action when access level lower than or equal %s', 'Ignore bomb action depends from access level', ['4','5','6','7','8','9'], '4'],
				'bomb_reason': ['Bomb. Reason %s', 'Reason for bomb explode', None, 'KA-BO-OM!!!111'],
				'bomb_idle': ['Bomb. Idle for unable get the bomb %s', 'Idle for unable get the bomb', None, '900'],

				# Karma actions

				'karma_action': ['Karma. Actions for karma change is %s', 'Allow change role/affiliation by karma change', [True,False], False],
				'karma_action_reason': ['Karma. Reason for actions by karma change is %s', 'Reason for change role/affiliation by karma change', None, 'by karma change!'],
				'karma_action_1ban': ['Karma. Ban when karma is lower than %s', 'Ban when karma is lower than defined value', None, '-50'],
				'karma_action_2kick': ['Karma. Kick when karma is lower than %s', 'Kick when karma is lower than defined value', None, '-20'],
				'karma_action_3visitor': ['Karma. Revoke voice when karma is lower than %s', 'Revoke voice when karma is lower than defined value', None, '-10'],
				'karma_action_4none': ['Karma. None affiliation when karma is lower than %s', 'Revoke affiliation when karma is lower than defined value', None, '-5'],
				'karma_action_5participant': ['Karma. Participant affiliation when karma is higher than %s', 'Give a participant affiliation when karma is higher than defined value', None, '5'],
				'karma_action_6member': ['Karma. Member affiliation when karma is higher than %s', 'Give a member affiliation when karma is higher than defined value', None, '20'],
				'karma_action_7moderator': ['Karma. Moderator role when karma is higher than %s', 'Give a moderator role when karma is higher than defined value', None, '50'],
				'karma_hard': ['Hard rule for karma is %s', 'Not allow any symbols between nick and karma digit' ,[True,False], False],
				'karma_limit': ['Limits for karma change is %s', 'Limitation of karma\'s change. Depends of access level' ,[True,False], True],
				'karma_limit_size': ['Value of limits for karma change %s', 'Value of limitation of karma\'s change. Depends of access level' ,None, '[3,5]'],

				# Flood
				'flood': ['Flood is %s', 'Autoanswer', ['off','random','smart'], 'off'],
				'autoflood': ['Autoflood is %s', 'Autoflood', [True,False], False],
				'floodcount': ['Number of message for autoflood\'s start: %s', 'Number of message for autoflood\'s start', None, '3'],
				'floodtime': ['Time period for autoflood\'s start: %s', 'Time period for autoflood\'s start', None, '1800'],
				'autophrases': ['Autophrases is %s', 'Autophrases', ['off','without highlight','all'], 'off'],
				'autophrasestime': ['Time period for autophrases is %s', 'Time period for autophrases', None, '7200'],
				'floodrepeat': ['Repeat phrase after match %s', 'Repeat phrase after match same messages', ['off','2','3','4','5','6','7','8','9','10'], '3']

				}

config_group_other = ['Other settings','#room-other',
				['ai','url_title','parse_define','clear_answer','smiles','autoturn','make_stanza_jid_count','content_length','acl_multiaction',
				'paste_xhtml_images','set_default_locale','store_users_url','trusted_servers','visitor_action','visitor_action_time'],None]

config_group_censor = ['Censor settings','#room-censor',
				['censor','censor_warning','censor_action_member','censor_action_non_member',
				'censor_custom','censor_custom_rules'],None]

config_group_mucfilter = ['General Muc-filter settings','#room-mucfilter',
				['muc_filter','muc_filter_mute_chat','muc_filter_mute_groupchat','muc_filter_mute_repeat','muc_filter_mute_repeat_action'],None]

config_group_mucfilter_newbie = ['Muc-filter settings for newbie','#room-mucfilter-newbie',
				['muc_filter_newbie','muc_filter_newbie_time','muc_filter_newbie_repeat','muc_filter_newbie_repeat_action'],None]

config_group_mucfilter_hash = ['Muc-filter settings for hash','#room-mucfilter-hash',
				['muc_filter_hash','muc_filter_hash_time','muc_filter_hash_events','muc_filter_hash_action','muc_filter_hash_action_time',
				'muc_filter_hash_action_current','muc_filter_deny_hash','muc_filter_deny_hash_list','muc_filter_hash_ban_server_by_rejoin',
				'muc_filter_hash_ban_server_by_rejoin_exception','muc_filter_hash_ban_server_by_rejoin_notify_jid',
				'muc_filter_hash_ban_server_by_rejoin_rejoins','muc_filter_hash_ban_server_by_rejoin_timeout','muc_filter_hash_ban_by_rejoin',
				'muc_filter_hash_ban_by_rejoin_timeout'],None]

config_group_mucfilter_content = ['Muc-filter settings by content','#room-mucfilter-content',
				['muc_filter_newline','muc_filter_newline_count','muc_filter_newline_msg_count','muc_filter_newline_msg',
				'muc_filter_large','muc_filter_repeat','muc_filter_match','muc_filter_reduce_spaces_msg','muc_filter_reduce_spaces_prs',
				'muc_filter_rejoin','muc_filter_repeat_prs','muc_filter_large_nick','muc_filter_large_status','muc_filter_history',
				'muc_filter_history_ban'],None]

config_group_mucfilter_raw = ['Muc-filter settings for raw-actions','#room-mucfilter-raw',
				['muc_filter_adblock_raw','muc_filter_adblock_prs_raw',
				'muc_filter_censor_raw','muc_filter_censor_prs_raw','muc_filter_raw_percent'],None]

config_group_mucfilter_censor = ['Muc-filter settings for censor/ad-block','#room-mucfilter-censor',
				['muc_filter_adblock_prs','muc_filter_adblock','muc_filter_censor','muc_filter_censor_prs'],None]

config_group_mucfilter_lists = ['Muc-filter settings for while/black lists','#room-mucfilter-lists',
				['muc_filter_whitelist','muc_filter_blacklist','muc_filter_blacklist_rules_jid','muc_filter_blacklist_rules_nick'],None]

config_group_mucfilter_caps = ['Muc-filter settings for while/black lists by caps','#room-mucfilter-caps-lists',
				['muc_filter_caps_list','muc_filter_caps_white',
				#'muc_filter_caps','muc_filter_caps_smart','muc_filter_caps_white_smart','muc_filter_caps_black_smart',
				'muc_filter_caps_black'],None]

config_group_mucfilter_validate = ['Muc-filter settings for validate items','#room-mucfilter-validate',
				['muc_filter_validate_nick','muc_filter_validate_login','muc_filter_validate_resource',
				'muc_filter_validate_caps_node','muc_filter_validate_caps_version','muc_filter_validate_count',
				'muc_filter_validate_action','muc_filter_validate_ban_server_exception','muc_filter_validate_ban_server_notify_jid'],None]

config_group_mucfilter_fast_action = ['Muc-filter settings for fast action','#room-mucfilter-fast-action',
				['muc_filter_fast_join','muc_filter_fast_join_count','muc_filter_fast_join_time'],None]

config_group_bomb = ['Settings for bomb-joke','#room-bombjoke',
				['bomb','bomb_fault','bomb_fault_persent','bomb_random','bomb_random_timer',
				'bomb_timer','bomb_wire','bomb_action','bomb_action_level','bomb_reason','bomb_random_active',
				'bomb_random_active_timer','bomb_random_timer_persent',
				'bomb_random_timer_skip_persent','bomb_idle'],None]

config_group_karma = ['Actions for karma change','#room-karma-action',
				['karma_action','karma_action_1ban','karma_action_2kick','karma_action_3visitor',
				'karma_action_4none','karma_action_5participant','karma_action_6member','karma_action_7moderator','karma_hard',
				'karma_limit','karma_limit_size'],None]

config_group_flood = ['Flood settings','#room-flood',
				['flood','autoflood','floodcount','floodtime','autophrases','autophrasestime','floodrepeat'],None]

config_groups = [config_group_mucfilter,config_group_mucfilter_newbie,config_group_mucfilter_hash,config_group_mucfilter_content,
				config_group_mucfilter_raw,config_group_mucfilter_censor,config_group_mucfilter_lists,config_group_mucfilter_caps,
				config_group_mucfilter_validate,config_group_mucfilter_fast_action,config_group_other,config_group_bomb,
				config_group_karma,config_group_censor,config_group_flood]

# type:
# b - binary (true\false)
# i - integer
# f - float
# tXX - text[:XX]
# mXX - multiline text[:XX]
# lXX - len(list) == XX
# d - droplist
# XXe - execute latest field by eval

owner_prefs = {'syslogs_enable': ['Logger. Enable system logs','b',True],
				'movement_logs_enable':['Logger. Enable logging ins and outs of the conference','b',True],
				'status_logs_enable':['Logger. Enable status change logging','b',True],
				'aff_role_logs_enable':['Logger. Enable role and affiliation logging','b',True],
				'html_logs_enable':['Logger. Html logs. Otherwize in text','b',True],
				'chatlogs_logs_gmt':['Logger. Use GMT time in MUC logs','b',False],
				'html_logs_end_text':['Logger. Additional text for logs','m512',''],
				'karma_limit':['Karma. Minimal karma for allow krama change for participants','i',5],
				'karma_show_default_limit':['Karma. Default length of list karma top+/-','i',10],
				'karma_show_max_limit':['Karma. Maximal length of list karma top+/-','i',20],
				'watch_size':['Watcher. Frequency of requests in watcher','i',900],
				'user_agent':['Www. User-agent for web queries','m256','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'],
				'size_overflow':['Www. Limit of page in bytes for www command','i',262144],
				'youtube_max_videos':['Youtube. Maximal links number','i',10],
				'youtube_default_videos':['Youtube. Default links number','i',3],
				'youtube_max_page_size':['Youtube. Page size limit','i',131072],
				'youtube_default_lang':['Youtube. Default language','t2','ru'],
				'age_default_limit':['Age. Default number of users for age commands','i',10],
				'age_max_limit':['Age. Maximal number of users for age commands','i',100],
				'anek_private_limit':['Anek. Anekdote size for private send','i',500],
				'troll_default_limit':['Troll. Default message number for troll command','i',10],
				'troll_max_limit':['Troll. Maximal message number for troll command','i',100],
				'troll_sleep_time':['Troll. Delay between messages for troll command','f',0.05],
				'backup_sleep_time':['Backup. Requests delay for backup command','f',0.1],
				'calendar_default_splitter':['Calendar. Default splitter for calendar','t10','_'],
				'clear_delay':['Clear. Delay between massages in clear command','f',1.3],
				'clear_default_count':['Clear. Default message number for clear command','i',20],
				'clear_max_count':['Clear. Maximal message number for clear command','i',100],
				'ping_digits':['Iq. Number after point in ping','i',3],
				'lfm_api':['LastFM. Api for lastfm plugin','t64','no api'],
				'lastfm_max_limit':['LastFM. Number of answers for lastfm plugin','i',10],
				'reboot_time':['Kernel. Restart timeout for error at bot initial (no connection, auth error)','i',180],
				'timeout':['Iq. Timeout for iq queries','i',600],
				'schedule_time':['Kernel. Schedule time','i',10],
				'sayto_timeout':['Sayto. Age of message in sayto before delete it from base with undelivered','i',1209600],
				'sayto_cleanup_time':['Sayto. Timeout for sayto base cleanup','i',86400],
				'scan_time':['Spy. Time for spy scan','i',1800],
				'spy_action_time':['Spy. Time for reaction on spy scan','i',86400],
				'rss_max_feed_limit':['Rss. Maximum rss count','i',10],
				'rss_min_time_limit':['Rss. Minimal time for rss check in minutes','i',10],
				'rss_get_timeout':['Rss. Timeout for rss request from server in seconds','i',15],
				'whereis_time_dec':['Whereis. Frequency for answer check for whereis command','f',0.5],
				'watcher_room_activity':['Watcher. Try rejoin in rooms with low activity','b',True],
				'watcher_self_ping':['Watcher. Allow self ping','b',True],
				'disco_max_limit':['Disco. Maximus andwers count for disco command','i',10],
				'juick_user_post_limit':['Juick. Number of posts','i',10],
				'juick_user_post_size':['Juick. Number of symbols in post','i',50],
				'juick_msg_answers_default':['Juick. Number of answers','i',10],
				'juick_user_tags_limit':['Juick. Number of tags','i',10],
				'iq_time_enable':['Iq. Allow answer to time request','b',True],
				'iq_uptime_enable':['Iq. Allow answer to uptime request','b',True],
				'iq_version_enable':['Iq. Allow answer to version request','b',True],
				'iq_disco_enable':['Iq. Allow answer to service discovery','b',True],
				'iq_ping_enable':['Iq. Allow answer to ping','b',True],
				'iq_show_rooms_disco':['Iq. Show bot rooms in service discovery','b',True],
				'paranoia_mode':['Kernel. Paranoic mode. Disable all execute possibles on bot','b',False],
				'show_loading_by_status':['Kernel. Bot status. Show different status for bot loading','b',True],
				'show_loading_by_status_show':['Kernel. Bot status. Status while loading','d','dnd',['chat','online','away','xa','dnd']],
				'show_loading_by_status_message':['Kernel. Bot status. Message while loading','t256','Loading...'],
				'show_loading_by_status_percent':['Kernel. Bot status. Show percent of loading','b',True],
				'show_loading_by_status_room':['Kernel. Bot status. Show join to room while loading','b',True],
				'kick_ban_notify':['Kernel. Notify when bot is kicked or banned','b',True],
				'kick_ban_notify_jid':['Kernel. Notify jid for bot kick or ban','t1024',''],
				'watch_activity_timeout':['Watcher. Timeout for no actions in room for rejoin','i',1800],
				'muc_filter_large_message_size':['Muc-filter. Message size for filter','i',512],
				'muc_filter_match_count':['Muc-filter. A kind words count','i',3],
				'muc_filter_match_warning_match':['Muc-filter. Number of kind parts in message','i',3],
				'muc_filter_match_warning_space':['Muc-filter. Number of empty parts in message','i',5],
				'muc_filter_match_view':['Muc-filter. Message limit','i',512],
				'muc_filter_match_warning_nn':['Muc-filter. Number of empty new lines','i',3],
				'muc_filter_rejoin_count':['Muc-filter. Number of reconnects for monitoring','i',3],
				'muc_filter_rejoin_timeout':['Muc-filter. Time for reconnect count','i',120],
				'muc_filter_status_count':['Muc-filter. Number of precences per time','i',3],
				'muc_filter_status_timeout':['Muc-filter. Time between presences','i',600],
				'muc_filter_large_status_size':['Muc-filter. Maximux status-message size','i',50],
				'muc_filter_large_nick_size':['Muc-filter. Maximum nick size','i',20],
				'muc_filter_repeat_count':['Muc-filter. Repeat count','i',3],
				'muc_filter_repeat_time': ['Muc-filter. Timeout for repeat message', 'i', 3600],
				'muc_filter_notify': ['Muc-filter. Notify about abnormal activity', 'b', False],
				'muc_filter_notify_jids': ['Muc-filter. Jid\'s for notify', 't1024', ''],
				'muc_filter_notify_peroid': ['Muc-filter. Time peroid for notify', 'i', 10],
				'muc_filter_notify_count': ['Muc-filter. Count of events for notify', 'i', 5],
				'muc_filter_notify_wait': ['Muc-filter. Time between notifies', 'i', 300],
				'html_paste_enable':['Paste. Paste as html. Otherwize as text','b',True],
				'yandex_api_key':['City. Yandex.Map API-key','t128','no api'],
				'bing_api_key':['Bing. Translator API-key','t128','no api'],
				'steam_api_key':['Steam. API-key','t128','no api'],
				'censor_text':['Kernel. Text for hide censore','t32','[censored]'],
				'ddos_limit':['Kernel. Time of ignore for anti-ddos','l10','[1800,1800,1800,1800,1800,600,300,150,60,0]'],
				'ddos_diff':['Kernel. Anti-ddos time delay between messages','l10','[30,30,30,30,20,20,15,10,5,0]'],
				'ddos_iq_requests':['Kernel. Iq anti-ddos. Requests number','i',30],
				'ddos_iq_limit':['Kernel. Iq anti-ddos. Time limits for requests','i',10],
				'amsg_limit_size':['Msgtoadmin. Size limit for msgtoadmin','i',1024],
				'amsg_limit':['Msgtoadmin. Time limit for next message for msgtoadmin','l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,60]'],
				'karma_timeout':['Karma. Time for karma change from access level','l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,5]'],
				'karma_discret':['Karma. Difference between two action in karma','i',5],
				'karma_discret_lim_up':['Karma. Upper value of karma for control action','i',100],
				'karma_discret_lim_dn':['Karma. Lower value of karma for control action','i',-100],
				'disco_exclude':['Disco. Exclude from disco by regexps','m256e',u'([؀-ݭ)\n(ﭐ-ﻼ])\n(syria|arab)','disco_exclude_update()'],
				'exclude_messages':['Kernel. Exclude symbols from bot\'s messages','m256e',u'([؀-ۿ])\n([ݐ-ݿ])\n([ﭐ-﷿])\n([ﹰ-﻿])','message_exclude_update()'],
				'1st_april_joke':['Kernel. 1st April joke','b',True],
				'soft_update_resend_hash':['Kernel. Send new hash into rooms after soft update','b',False],
				'notepad':['Notepad','m4096',''],
				'wot_region':['Region of API Server', 'd', 'RU', ['RU','EU','COM','SEA','KR']],
				'wot_appid':['World of Tanks. Application ID','t64','demo'],
				'wot_delay':['World of Tanks. Time of delay','i',2],
				'wot_retries':['World of Tanks. Count of retries','i',2]
				}

owner_group_mucfilter = ['Muc-filter settings','#owner-mucfilter',
				['muc_filter_large_message_size','muc_filter_match_count','muc_filter_match_warning_match',
				'muc_filter_match_warning_space','muc_filter_match_view','muc_filter_match_warning_nn',
				'muc_filter_rejoin_count','muc_filter_rejoin_timeout','muc_filter_status_count',
				'muc_filter_status_timeout','muc_filter_large_status_size','muc_filter_large_nick_size',
				'muc_filter_repeat_count','muc_filter_repeat_time','muc_filter_notify','muc_filter_notify_jids',
				'muc_filter_notify_peroid','muc_filter_notify_count','muc_filter_notify_wait']]

owner_group_iq = ['Iq requests settings','#owner-iq',
				['iq_time_enable','iq_uptime_enable','iq_version_enable','iq_disco_enable',
				'iq_ping_enable','ping_digits','timeout','iq_show_rooms_disco']]

owner_group_juick = ['Juick settings','#owner-juick',
				['juick_user_post_limit','juick_user_post_size','juick_msg_answers_default','juick_user_tags_limit']]

owner_group_logs = ['Logs settings','#owner-logs',
				['syslogs_enable','status_logs_enable','aff_role_logs_enable','movement_logs_enable','html_logs_enable','html_logs_end_text','chatlogs_logs_gmt']]

owner_group_youtube = ['Youtube settings','#owner-youtube',
				['youtube_max_videos','youtube_default_videos','youtube_max_page_size','youtube_default_lang']]

owner_group_other = ['Other settings','#owner-other',
				['anek_private_limit','backup_sleep_time','calendar_default_splitter',
				'disco_max_limit','disco_exclude','html_paste_enable']]

owner_group_api = ['API settings','#owner-api',
				['yandex_api_key','bing_api_key','steam_api_key','lfm_api','wot_appid']]

owner_group_karma = ['Karma settings','#owner-karma',
				['karma_limit','karma_show_default_limit','karma_show_max_limit','karma_timeout','karma_discret','karma_discret_lim_up','karma_discret_lim_dn']]

owner_group_www = ['WWW settings','#owner-www',
				['size_overflow','user_agent']]

owner_group_troll = ['Antitroll settings','#owner-troll',
				['troll_default_limit','troll_max_limit','troll_sleep_time']]

owner_group_kernel = ['Kernel settings','#owner-kernel',
				['censor_text','ddos_limit','ddos_diff','paranoia_mode','reboot_time','schedule_time',
				'show_loading_by_status','show_loading_by_status_show','show_loading_by_status_message',
				'show_loading_by_status_percent','kick_ban_notify','kick_ban_notify_jid',
				'ddos_iq_requests','ddos_iq_limit','exclude_messages','1st_april_joke','soft_update_resend_hash']]

owner_group_lastfm = ['LastFM settings','#owner-lastfm',
				['lfm_api','lastfm_max_limit']]

owner_group_whereis = ['Whereis settings','#owner-whereis',
				['whereis_time_dec']]

owner_group_watcher = ['Watcher settings','#owner-watcher',
				['watch_size','watcher_room_activity','watch_activity_timeout','watcher_self_ping']]

owner_group_clear = ['Clear settings','#owner-clear',
				['clear_delay','clear_default_count','clear_max_count']]

owner_group_rss = ['RSS settings','#owner-rss',
				['rss_max_feed_limit','rss_min_time_limit','rss_get_timeout']]

owner_group_amsg = ['Message for admin settings','#owner-amsg',
				['amsg_limit_size','amsg_limit']]

owner_group_age = ['Age settings','#owner-age',
				['age_default_limit','age_max_limit']]

owner_group_sayto = ['Sayto settings','#owner-sayto',
				['sayto_timeout','sayto_cleanup_time']]

owner_group_spy = ['Spy settings','#owner-spy',
				['scan_time','spy_action_time']]

owner_group_notepad = ['Notepad','#owner-notepad',
				['notepad']]

owner_group_wot = ['World of Tanks settings','#owner-wot',
				['wot_region','wot_appid', 'wot_delay', 'wot_retries']]

owner_groups = [owner_group_amsg,owner_group_rss,owner_group_clear,
				owner_group_kernel,owner_group_lastfm,owner_group_whereis,
				owner_group_watcher,owner_group_troll,owner_group_www,
				owner_group_karma,owner_group_sayto,owner_group_age,
				owner_group_mucfilter,owner_group_iq,owner_group_juick,
				owner_group_logs,owner_group_youtube,owner_group_other,
				owner_group_api,owner_group_notepad,owner_group_wot]

comms = [
	 (0, 'help', helpme, 2, 'Help system. Helps without commands: about, donation, access'),
	 (9, 'join', bot_join, 2, 'Join conference.\njoin room[@conference.server.ru[/nick]]\n[password]'),
	 (9, 'leave', bot_leave, 2, 'Leave conference.\nleave room[@conference.server.ru[/nick]]'),
	 (9, 'rejoin', bot_rejoin, 2, 'Rejoin conference.\nrejoin room[@conference.server.ru[/nick]]\n[password]'),
	 (9, 'bot_owner', owner, 2, 'Bot owners list.\nbot_owner show\nbot_owner add|del jid'),
	 (9, 'bot_ignore', ignore, 2, 'Black list.\nbot_ignore show\nbot_ignore add|del jid'),
	 (9, 'syslogs', show_syslogs, 2, 'Show bot\'s syslogs.\nsyslogs [number of records] [text]'),
	 (9, 'syslogs_search', show_syslogs_search, 2, 'Search in bot\'s syslogs.\nsyslogs_search <regexp>\n[date regexp]'),
	 (6, 'where', info_where, 1, 'Show conferences.'),
	 (6, 'where+', info_where_plus, 1, 'Show conferences.'),
	 (0, 'inbase', info_base, 1, 'Your identification in global base.'),
	 (9, 'look', real_search, 2, 'Search user in conferences where the bot is.'),
	 (9, 'glook', real_search_owner, 2, 'Search user in conferences where the bot is. Also show jid\'s'),
	 (7, 'rss', rss, 2, 'News:\nrss show - show current.\nrss add url time mode - add news.\nrss del url - remove news.\nrss get url feeds mode - get current news.\nrss new url feeds mode - get unread news only.\nrss clear - clear all news in current conference.\nrss all - show all news in all conferences.\n\nurl - url of rss/atom chanel. can set without http://\ntime - update time. number + time identificator. h - hour, m - minute. allowed only one identificator.\nfeeds - number of messages to receive. 10 max.\nmode - receive mode. full - full news, head - only headers, body - only bodies.\nwith -url to be show url of news.'),
	 (7, 'alias', alias, 2, 'Aliases.\nalias add|add_global new=old\nalias del|del_global|show text'),
	 (0, 'commands', info_comm, 1, 'Show commands list.'),
	 (8, 'comm', comm_on_off, 2, 'Enable/Disable commands.\ncomm - show disable commands\ncomm on command - enable command\ncomm off command1[ command2 command3 ...] - disable one or more command'),
	 (0, 'bot_uptime', uptime, 1, 'Show bot uptime.'),
	 (6, 'info', info, 1, 'Misc information about bot.'),
	 (3, 'new', vcs_info, 1, 'Last VCS update log'),
	 (9, 'limit', conf_limit, 2, 'Set temporary message limit.'),
	 (9, 'plugin', bot_plugin, 2, 'Plugin system.\nplugin show|local\nplugin add|del name'),
	 (9, 'error', show_error, 2, 'Show error(s).\nerror [number|clear]'),
	 (0, 'whoami', info_access, 1, 'Your identification.'),
	 (0, 'whois', info_whois, 2, 'Identification.'),
	 (0, 'lang', info_lang, 2, 'Show language for user.'),
	 (0, 'status', status, 2, 'Show status.'),
	 (3, 'prefix', set_prefix, 2, 'Set command prefix. Use \'none\' for disable prefix'),
	 (9, 'set_locale', set_locale, 2, 'Change bot localization.\nset_locale en|%s' % '|'.join([tmp[:-4] for tmp in os.listdir(loc_folder[:-6]) if tmp[-4:]=='.txt'])),
	 (7, 'config', configure, 2, 'Conference configure.\nconfig [show[ status]|help][ item]'),
	 (4, 'pmlock', muc_filter_lock, 2, 'Deny recieve messages from unaffiliated participants in private'),
	 (9, 'ddos', ddos_info, 2, 'Temporary ignore with ddos detect.\nddos [show|del jid]')]

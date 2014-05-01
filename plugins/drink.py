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

def to_drink(type, jid, nick, text):
	dmas = [L('first','%s/%s'%(jid,nick)),L('second','%s/%s'%(jid,nick)),L('third','%s/%s'%(jid,nick)),L('fourth','%s/%s'%(jid,nick)),
			L('fifth','%s/%s'%(jid,nick)),L('sixth','%s/%s'%(jid,nick)),L('seventh','%s/%s'%(jid,nick)),L('eighth','%s/%s'%(jid,nick)),
			L('nineth','%s/%s'%(jid,nick)),L('tenth','%s/%s'%(jid,nick)),L('eleventh','%s/%s'%(jid,nick)),L('twelveth','%s/%s'%(jid,nick)),
			L('thirteenth','%s/%s'%(jid,nick)),L('fourteenth','%s/%s'%(jid,nick)),L('fivteenth','%s/%s'%(jid,nick)),L('sixteenth','%s/%s'%(jid,nick)),
			L('seventeenth','%s/%s'%(jid,nick)),L('eighteenth','%s/%s'%(jid,nick)),L('nineteenth','%s/%s'%(jid,nick)),('twentieth'),
			L('twenty-first','%s/%s'%(jid,nick)),L('twenty-second','%s/%s'%(jid,nick)),L('twenty-third','%s/%s'%(jid,nick)),
			L('twenty-fourth','%s/%s'%(jid,nick)),L('twenty-fifth','%s/%s'%(jid,nick)),L('twenty-sixth','%s/%s'%(jid,nick)),L('twenty-seventh','%s/%s'%(jid,nick)),
			L('twenty-eighth','%s/%s'%(jid,nick)),L('twenty-nineth','%s/%s'%(jid,nick)),L('thirtieth','%s/%s'%(jid,nick)),L('thirty-first','%s/%s'%(jid,nick))]
	mmas1 = [L('january','%s/%s'%(jid,nick)),L('february','%s/%s'%(jid,nick)),L('march','%s/%s'%(jid,nick)),L('april','%s/%s'%(jid,nick)),
			 L('may','%s/%s'%(jid,nick)),L('june','%s/%s'%(jid,nick)),L('july','%s/%s'%(jid,nick)),L('august','%s/%s'%(jid,nick)),
			 L('september','%s/%s'%(jid,nick)),L('october','%s/%s'%(jid,nick)),L('november','%s/%s'%(jid,nick)),L('december','%s/%s'%(jid,nick))]
	mmas2 = [L('January','%s/%s'%(jid,nick)),L('February','%s/%s'%(jid,nick)),L('March','%s/%s'%(jid,nick)),L('April','%s/%s'%(jid,nick)),
			 L('May','%s/%s'%(jid,nick)),L('June','%s/%s'%(jid,nick)),L('July','%s/%s'%(jid,nick)),L('August','%s/%s'%(jid,nick)),
			 L('September','%s/%s'%(jid,nick)),L('October','%s/%s'%(jid,nick)),L('November','%s/%s'%(jid,nick)),L('December','%s/%s'%(jid,nick))]
	wday = [L('monday','%s/%s'%(jid,nick)),L('tuesday','%s/%s'%(jid,nick)),L('wendesday','%s/%s'%(jid,nick)),L('thirsday','%s/%s'%(jid,nick)),
			L('friday','%s/%s'%(jid,nick)),L('saturday','%s/%s'%(jid,nick)),L('sunday','%s/%s'%(jid,nick))]
	lday = [L('last','%s/%s'%(jid,nick)),L('last','%s/%s'%(jid,nick)),L('Last','%s/%s'%(jid,nick)),L('last','%s/%s'%(jid,nick)),
			L('Last','%s/%s'%(jid,nick)),L('Last','%s/%s'%(jid,nick)),L('lAst','%s/%s'%(jid,nick))]
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		week1 = ''
		week2 = ''
		if not ddate: msg = L('Read file error.','%s/%s'%(jid,nick))
		else:
			if len(text) <= 2:
				ltim = tuple(time.localtime())
				text = '%s %s' % (ltim[2], mmas2[ltim[1]-1])
				week1 = '%s %s %s' % (ltim[2]/7+(ltim[2]%7 > 0), wday[ltim[6]], mmas2[ltim[1]-1])
				if ltim[2]+7 > calendar.monthrange(ltim[0], ltim[1])[1]: week2 = '%s %s %s' % (lday[ltim[6]].lower(), wday[ltim[6]], mmas2[ltim[1]-1])
			or_text = text
			if text.count('.')==1: text = text.split('.')
			elif text.count(' ')==1: text = text.split(' ')
			else: text = [text]
			msg = ''
			ddate = ddate.split('\n')
			ltxt = len(text)
			for tmp in ddate:
				if or_text.lower() in tmp.lower(): msg += '\n'+tmp
				elif week1.lower() in tmp.lower() and week1 != '': msg += '\n'+tmp
				elif week2.lower() in tmp.lower() and week2 != '': msg += '\n'+tmp
				else:
					try:
						ttmp = tmp.split(' ')[0].split('.')
						tday = [ttmp[0]]
						tday.append(dmas[int(ttmp[0])-1])
						tmonth = [ttmp[1]]
						tmonth.append(mmas1[int(ttmp[1])-1])
						tmonth.append(mmas2[int(ttmp[1])-1])
						tmonth.append(str(int(ttmp[1])))
						t = tday.index(text[0])
						t = tmonth.index(text[1])
						msg += '\n'+tmp
					except: pass
			if msg == '': msg = L('Holiday: %s not found.','%s/%s'%(jid,nick)) % or_text
			else: msg = L('I know holidays: %s','%s/%s'%(jid,nick)) % msg
	else: msg = L('Database doesn\'t exist.','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def calend(type, jid, nick, text):
	msg, url, text = '', '', text.strip()
	if not text: url = 'http://www.calend.ru/day/%s-%s/' % tuple(time.localtime())[1:3]
	elif re.match('\d+\.\d+$', text): url = 'http://www.calend.ru/day/%s-%s/' % tuple(text.split('.')[::-1])
	elif len(text) > 1: url = 'http://www.calend.ru/search/?search_str=' + urllib.quote(text.encode('cp1251'))
	if url:
		data = html_encode(load_page(url))
		t = get_tag(data,'title')
		if t == u'Поиск':
			hl = re.findall('<a  href="(/holidays(?:/\d*?)+?)" title=".+?">(.+?)</a>(?:.|\s)+?/>\s+?(\d+ .+?)\s', data)
			if len(hl) == 1:
				d = re.search('class="img_small" /></a></td>\s+?<td>\s+?(.+?\.)\s+?</td>', data, re.S).group(1)
				d = unescape(re.sub('\s+', ' ', d.strip()))
				msg += '%s (%s) - %s\nhttp://www.calend.ru%s' % (hl[0][1], hl[0][2], d, hl[0][0])
			elif hl:
				for a in hl: msg += '\n%s (%s)' % (a[1], a[2])
		else:
			d = get_tag(data,'h1')
			hl = re.findall('<a  href="/holidays(?:/\d*?)+?" title=".+?">(.+?)</a>', data)
			if hl: msg = '%s:\n%s' % (d, '\n'.join(hl))
	else: msg = L('What?','%s/%s'%(jid,nick))
	if not msg: msg = L('Holiday: %s not found.','%s/%s'%(jid,nick)) % text
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'drink', to_drink, 2, 'Find holiday\ndrink [name_holiday/date]'),
		(3, 'calend', calend, 2, 'Find holiday\ncalend [name_holiday/date]')]
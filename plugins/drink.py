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

# translate: first,second,third,fourth,fifth,sixth,seventh,eighth,nineth,tenth,eleventh,twelveth,thirteenth,fourteenth,fivteenth,sixteenth,seventeenth,eighteenth,nineteenth,twentieth,twenty-first,twenty-second,twenty-third,twenty-fourth,twenty-fifth,twenty-sixth,twenty-seventh,twenty-eighth,twenty-nineth,thirtieth,thirty-first,january,february,march,april,may,june,july,august,september,october,november,december,January,February,March,April,May,June,July,August,September,October,November,December,monday,tuesday,wendesday,thirsday,friday,saturday,sunday,last,last,Last,last,Last,Last,lAst

drink_dmas = ['first','second','third','fourth','fifth','sixth','seventh','eighth','nineth','tenth','eleventh','twelveth',
			'thirteenth','fourteenth','fivteenth','sixteenth','seventeenth','eighteenth','nineteenth','twentieth',
			'twenty-first','twenty-second','twenty-third','twenty-fourth','twenty-fifth','twenty-sixth','twenty-seventh',
			'twenty-eighth','twenty-nineth','thirtieth','thirty-first']
drink_mmas1 = ['january','february','march','april','may','june','july','august','september','october','november','december']
drink_mmas2 = ['January','February','March','April','May','June','July','August','September','October','November','December']
drink_wday = ['monday','tuesday','wendesday','thirsday','friday','saturday','sunday']
drink_lday = ['last','last','Last','last','Last','Last','lAst']

def to_drink(type, jid, nick, text):
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		week1 = ''
		week2 = ''
		if not ddate: msg = L('Read file error.','%s/%s'%(jid,nick))
		else:
			if len(text) <= 2:
				ltim = tuple(time.localtime())
				text = '%s %s' % (ltim[2], L(drink_mmas2[ltim[1]-1],'%s/%s'%(jid,nick)))
				week1 = '%s %s %s' % (ltim[2]/7+(ltim[2]%7 > 0), L(drink_wday[ltim[6]],'%s/%s'%(jid,nick)), L(drink_mmas2[ltim[1]-1],'%s/%s'%(jid,nick)))
				if ltim[2]+7 > calendar.monthrange(ltim[0], ltim[1])[1]: week2 = '%s %s %s' % (L(drink_lday[ltim[6]].lower(),'%s/%s'%(jid,nick)), L(drink_wday[ltim[6]],'%s/%s'%(jid,nick)), L(drink_mmas2[ltim[1]-1],'%s/%s'%(jid,nick)))
			or_text = text
			if text.count('.')==1: text = text.split('.')
			elif text.count(' ')==1: text = text.split(' ')
			else: text = [text]
			msg = ''
			ddate = ddate.split('\n')
			for tmp in ddate:
				if or_text.lower() in tmp.lower(): msg += '\n'+tmp
				elif week1.lower() in tmp.lower() and week1 != '': msg += '\n'+tmp
				elif week2.lower() in tmp.lower() and week2 != '': msg += '\n'+tmp
				else:
					try:
						ttmp = tmp.split(' ')[0].split('.')
						tday = [ttmp[0]]
						tday.append(L(drink_dmas[int(ttmp[0])-1],'%s/%s'%(jid,nick)))
						tmonth = [ttmp[1]]
						tmonth.append(L(drink_mmas1[int(ttmp[1])-1],'%s/%s'%(jid,nick)))
						tmonth.append(L(drink_mmas2[int(ttmp[1])-1],'%s/%s'%(jid,nick)))
						tmonth.append(str(int(ttmp[1])))
						t = tday.index(L(text[0],'%s/%s'%(jid,nick)))
						t = tmonth.index(L(text[1],'%s/%s'%(jid,nick)))
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

execute = [(3, 'drink', to_drink, 2, 'Find holiday\ndrink [name_holiday/date]',['raw']),
		(3, 'calend', calend, 2, 'Find holiday\ncalend [name_holiday/date]')]
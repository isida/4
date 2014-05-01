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

currency_conv_list = ['ATS','AUD','BEF','BYR','CAD','CHF','CNY','DEM','DKK','EEK',\
					  'EGP','ESP','EUR','FIM','FRF','GBP','GRD','IEP','ISK','ITL',\
					  'JPY','KGS','KWD','KZT','LTL','NLG','NOK','PTE','SDR','SEK',\
					  'SGD','TRL','TRY','UAH','USD','XDR','YUN','RUB']

def currency_converter(type, jid, nick, text):
	msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	text = text.strip().upper()
	if text == 'LIST': msg = L('Available values:\n%s','%s/%s'%(jid,nick)) % ', '.join(currency_conv_list).replace('RUB','RUR')
	else:
		repl_curr = ((u'RUR','RUB'),(u'€','EUR'),('$','USD'),(u'¥','JPY'),(u'£','GBP'),(',','.'))
		for tmp in repl_curr: text = text.replace(tmp[0],' %s ' % tmp[1])
		c_from,c_to,c_summ = '','',''
		val = [t for t in re.findall('[A-Z]{3,4}', text, re.S) if t in currency_conv_list]
		if len(val) >= 2: c_from,c_to = val[:2]
		val = ''.join(re.findall('[0-9\.]',text))
		if val.replace('.','').isdigit() and val.count('.') <= 1:
			if val.startswith('.'): c_summ = '0%s' % val
			elif val.endswith('.'): c_summ = '%s0' % val
			else: c_summ = val
		if c_from and c_to and c_summ:
			date = tuple(time.localtime())[:3]
			mname = ['%D0%AF%D0%BD%D0%B2%D0%B0%D1%80%D1%8C','%D0%A4%D0%B5%D0%B2%D1%80%D0%B0%D0%BB%D1%8C',
					 '%D0%9C%D0%B0%D1%80%D1%82','%D0%90%D0%BF%D1%80%D0%B5%D0%BB%D1%8C',
					 '%D0%9C%D0%B0%D0%B9','%D0%98%D1%8E%D0%BD%D1%8C',
					 '%D0%98%D1%8E%D0%BB%D1%8C','%D0%90%D0%B2%D0%B3%D1%83%D1%81%D1%82',
					 '%D0%A1%D0%B5%D0%BD%D1%82%D1%8F%D0%B1%D1%80%D1%8C','%D0%9E%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C',
					 '%D0%9D%D0%BE%D1%8F%D0%B1%D1%80%D1%8C','%D0%94%D0%B5%D0%BA%D0%B0%D0%B1%D1%80%D1%8C']
			url = 'http://quote.rbc.ru/cgi-bin/conv/external/converter.shtml?source=cb.0&tid_from=%s&commission=1.0&tid_to=%s&summa=%s&day=%s&mon=%s&year=%s' % (c_from,c_to,c_summ,date[2],mname[date[1]-1],date[0])
			body = html_encode(load_page(url))
			try:
				curr = body.split('<select name="tid_from" class="n">')[1].split('</select>')[0]
				curr_list = dict(re.findall('<option value="(.*?)".*?>(.*?)</option>',curr,re.S|re.I|re.U))
			except: curr_list = {}
			try: body = body.split('<table id="rTable" class="table">',1)[1]
			except: body = ''
			regex = '<tbody>.*?<td>(.*?)</td>.*?<td class="b">(.*?)</td>.*?<td class="b">(.*?)</td>.*?<td>(.*?)</td>.*?<td class="b">(.*?)</td>'
			mt = re.findall(regex, body, re.S)
			if mt != []:
				mt = [t.strip() for t in mt[0]]
				if curr_list.has_key(mt[0]): frv = curr_list[mt[0]]
				else: frv = mt[0]
				if curr_list.has_key(mt[3]): tov = curr_list[mt[3]]
				else: tov = mt[3]
				msg = '%s %s (%s) = %s %s (%s) | 1 %s = %s %s' % (c_summ,c_from,frv,mt[4],c_to,tov,c_from,mt[2],c_to)
				msg = msg.replace('RUB','RUR')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'convert', currency_converter, 2, 'Currency converter\nconvert from to count\nconvert list')]

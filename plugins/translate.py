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

def translate_ru(type, jid, nick, text):
	text = text.strip()
	trlang = {'en':['e',L('English','%s/%s'%(jid,nick))],'ru':['r',L('Russian','%s/%s'%(jid,nick))],'fr':['f',L('French','%s/%s'%(jid,nick))],
			  'es':['s',L('Spanish','%s/%s'%(jid,nick))],'it':['i',L('Italian','%s/%s'%(jid,nick))],'de':['g',L('German','%s/%s'%(jid,nick))],
			  'pt':['p',L('Portuguese','%s/%s'%(jid,nick))]}
			  
	trlang2 = {'e':'en','r':'ru','f':'fr','s':'es','i':'it','g':'de','p':'pt'}
	
	if text.lower() == 'list': msg = L('Available languages for translate:','%s/%s'%(jid,nick)) + ' ' + ', '.join(sorted(trlang.keys()))
	elif text[:5].lower() == 'info ':
		text = text.lower().split(' ')
		msg = ''
		for tmp in text:
			if tmp in trlang: msg += '%s - %s, ' % (tmp,trlang[tmp][1])
		if len(msg): msg = L('Available languages: %s','%s/%s'%(jid,nick)) % msg[:-2]
		else: msg = L('I don\'t know this language','%s/%s'%(jid,nick))
	elif text[:5].lower() == 'lang ' and text.count(' ')==1:
		text = text.lower().split(' ')[1]
		msg = ', '.join(['%s - %s' % (k,trlang[k][1]) for k in trlang.keys() if text in trlang[k][1].lower()])
		if len(msg): msg = L('Available languages: %s','%s/%s'%(jid,nick)) % msg
		else: msg = L('I don\'t know this language','%s/%s'%(jid,nick))
	else:
		if ' ' in text:
			text = text.split(' ',2)
			url = 'http://m.translate.ru/services/MobileService.asmx/TranslateText4Touch?'
			if len(text)>1 and trlang.has_key(text[0].lower()):
				if len(text)>2 and trlang.has_key(text[1].lower()): lfrom,lto,tr_text = text[0].lower(),text[1].lower(),text[2]
				else: lfrom,lto,tr_text = '',text[0].lower(),' '.join(text[1:])
				if lfrom: lft = trlang[lfrom][0]
				else: lft = 'a'
				lft += trlang[lto][0]
				search_results = load_page(url, {'intLang':lto,\
												 'text':tr_text.encode("utf-8"),\
												 'direction':lft,\
												 'template':'General'})
				tr_xml = xmpp.simplexml.XML2Node(search_results)
				isWord = tr_xml.getTagData('isWord') == 'true'
				result = tr_xml.getTagData('result')
				tr_direct = tr_xml.getTagData('ptsDirCode')
				if isWord:
					result = result.replace('&nbsp;<span class="ref_info"></span>,\n',',')
					result = result.replace('<span class="ref_dictionary">\n','<span class="ref_dictionary">')
					result = result.replace('<span class="ref_comment">\n','<span class="ref_comment">')
					result = result.replace('</span>\n<span class="ref_info">','</span><span class="ref_info">')
					result = result.replace('<li><span class="ref_result">\n','<li><span class="ref_result">, ')
					for t in re.findall('(</div>\n.*?<div class="tr_pr">)',result,re.I+re.U+re.S): result = result.replace(t,'</div><div class="tr_pr">')
					result = result.replace('<span class="ref_source">','||<span class="ref_source">')
					for t in re.findall('(<a href=.*?</a>)',result,re.I+re.U+re.S): result = result.replace(t,'')
					for t in re.findall('(<span id=.*?</span>)',result,re.I+re.U+re.S): result = result.replace(t,'')
					result = result.replace('<br><span class="w_des">','<span class="w_des">')
					result = result.replace('<b>\n','<b>')
					msg = urllib.unquote(unhtml(result).encode('utf8')).decode('utf8', 'ignore')
					msg = msg.replace('||','').replace(')\n(',') (').replace('\n, ',', ').replace(' ,',',').replace(',\n',', ')
				else: msg = result
				if not lfrom:
					if '\n' in msg: symb = '\n'
					else: symb = ' '
					msg = L('%s%s[Source: %s]','%s/%s'%(jid,nick)) % (msg,symb,trlang[trlang2[tr_direct[0]]][1].strip())
			else: msg = L('Incorrect language settings for translate. translate list - available languages.','%s/%s'%(jid,nick))
		else: msg = L('Command\'s format: translate [from] to text','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'translate', translate_ru, 2, 'Translator from translate.ru\ntranslate [from_language] to_language text - translate text\ntranslate list - list for available languages for translate\ntranslate info <reduction> - get info about language reduction\ntranslate lang <expression> - get languages by expression')]


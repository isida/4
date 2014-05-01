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

def bing_translate(type, jid, nick, text):
	text = text.strip()
	trlang = {'id':L('Indonesian','%s/%s'%(jid,nick)), 'it':L('Italian','%s/%s'%(jid,nick)), 'ar':L('Arabic','%s/%s'%(jid,nick)),
			'ja':L('Japanese','%s/%s'%(jid,nick)), 'bg':L('Bulgarian','%s/%s'%(jid,nick)), 'ko':L('Korean','%s/%s'%(jid,nick)),
			'ca':L('Catalan','%s/%s'%(jid,nick)), 'lv':L('Latvian','%s/%s'%(jid,nick)), 'zh-chs':L('Chinese Simplified','%s/%s'%(jid,nick)),
			'lt':L('Lithuanian','%s/%s'%(jid,nick)), 'zh-cht':L('Chinese Traditional','%s/%s'%(jid,nick)), 'no':L('Norwegian','%s/%s'%(jid,nick)),
			'cs':L('Czech','%s/%s'%(jid,nick)), 'pl':L('Polish','%s/%s'%(jid,nick)), 'da':L('Danish','%s/%s'%(jid,nick)),
			'pt':L('Portuguese','%s/%s'%(jid,nick)), 'nl':L('Dutch','%s/%s'%(jid,nick)), 'ro':L('Romanian','%s/%s'%(jid,nick)),
			'en':L('English','%s/%s'%(jid,nick)), 'ru':L('Russian','%s/%s'%(jid,nick)), 'et':L('Estonian','%s/%s'%(jid,nick)),
			'sk':L('Slovak','%s/%s'%(jid,nick)), 'fi':L('Finnish','%s/%s'%(jid,nick)), 'sl':L('Slovenian','%s/%s'%(jid,nick)),
			'fr':L('French','%s/%s'%(jid,nick)), 'es':L('Spanish','%s/%s'%(jid,nick)), 'de':L('German','%s/%s'%(jid,nick)),
			'sv':L('Swedish','%s/%s'%(jid,nick)), 'el':L('Greek','%s/%s'%(jid,nick)), 'th':L('Thai','%s/%s'%(jid,nick)),
			'ht':L('Haitian Creole','%s/%s'%(jid,nick)), 'tr':L('Turkish','%s/%s'%(jid,nick)), 'he':L('Hebrew','%s/%s'%(jid,nick)),
			'uk':L('Ukrainian','%s/%s'%(jid,nick)), 'hi':L('Hindi','%s/%s'%(jid,nick)), 'vi':L('Vietnamese','%s/%s'%(jid,nick)),
			'hu':L('Hungarian','%s/%s'%(jid,nick))}
	if text.lower() == 'list': msg = L('Available languages for translate:','%s/%s'%(jid,nick)) + ' ' + ', '.join(sorted(trlang.keys()))
	elif text[:5].lower() == 'info ':
		text = text.lower().split(' ')
		msg = ''
		for tmp in text:
			if tmp in trlang: msg += '%s - %s, ' % (tmp,trlang[tmp])
		if len(msg): msg = L('Available languages: %s','%s/%s'%(jid,nick)) % msg[:-2]
		else: msg = L('I don\'t know this language','%s/%s'%(jid,nick))
	elif text[:5].lower() == 'lang ' and text.count(' ')==1:
		text = text.lower().split(' ')[1]
		msg = ', '.join(['%s - %s' % (k,trlang[k]) for k in trlang.keys() if text in trlang[k].lower()])
		if len(msg): msg = L('Available languages: %s','%s/%s'%(jid,nick)) % msg
		else: msg = L('I don\'t know this language','%s/%s'%(jid,nick))
	else:
		if ' ' in text:
			text = text.split(' ',2)
			url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
			bing_api = GT('bing_api_key')
			if bing_api == 'no api': msg = L('Not found Api-key for Bing translator','%s/%s'%(jid,nick))
			elif len(text)>1 and trlang.has_key(text[0].lower()):
				if len(text)>2 and trlang.has_key(text[1].lower()): lfrom,lto,tr_text = text[0].lower(),text[1].lower(),text[2]
				else: lfrom,lto,tr_text = '',text[0].lower(),' '.join(text[1:])
				translate_results = html_encode(load_page(url, {'oncomplete':'responseData',\
																'appId':bing_api,\
																'text':tr_text.encode("utf-8"),\
																'from':lfrom,\
																'to':lto}))
				try: msg = re.findall('responseData\(\"(.*?)\"\)\;$',unicode(translate_results),re.S|re.I|re.U)[0]
				except: msg = L('I can\'t translate it!','%s/%s'%(jid,nick))
			else: msg = L('Incorrect language settings for translate. bt list - available languages.','%s/%s'%(jid,nick))
		else: msg = L('Command\'s format: bt [from] to text','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'bt', bing_translate, 2, 'Bing translator.\nbt [from_language] to_language text - translate text\nbt list - list for available languages for translate\nbt info <reduction> - get info about language reduction\nbt lang <expression> - get languages by expression')]


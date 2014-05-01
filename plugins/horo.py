#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) ferym <ferym@jabbim.org.ru>                                #
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

# translate: aries,taurus,gemini,cancer,leo,virgo,libra,scorpio,sagittarius,capricorn,aquarius,pisces
horodb=['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']

def handler_horoscope(type, jid, nick, text):
	param = text.strip().lower()
	msg = L('What?','%s/%s'%(jid,nick))
	if param:
		if param == 'list': msg = ', '.join(['%s (%s)' % (L(t).capitalize(),t.capitalize()) for t in horodb])
		if param == 'date':
			horo_dates = ['21.03-19.04','20.04-20.05','21.05-20.06','21.06-22.07','23.07-22.08','23.08-22.09','23.09-22.10','23.10-21.11','22.11-21.12','22.12-19.01','20.01-18.02','19.02-20.03']
			msg = L('List of dates:\n%s','%s/%s'%(jid,nick)) % '\n'.join([u'%s … %s' % (horo_dates[i],L(t).capitalize()) for i,t in enumerate(horodb)])
			if type=='groupchat':
				send_msg('chat', jid, nick, msg)
				msg = L('Send for you in private','%s/%s'%(jid,nick))
		if param in [L(t) for t in horodb] or param in horodb:
			if param not in horodb: param = dict([[L(t),t] for t in horodb])[param]
			body = html_encode(load_page('http://horo.mail.ru/prediction/%s/today' % param))
			try: msg = unhtml_hard(re.findall('<div id="tm_today">(.+?)<div class="mb2">',body,re.S|re.I|re.U)[0].strip())
			except: msg = L('Unknown error!','%s/%s'%(jid,nick))
			if type=='groupchat':
				send_msg('chat', jid, nick, msg)
				msg = L('Send for you in private','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(3, 'horo', handler_horoscope, 2, 'Horoscope.\nhoro list - show all zodiacs.\nhoro date - show dates for zodiacs. | Author: ferym')]

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

JUICK_JID = 'juick@juick.com'

# Список последних сообщений:
JUICK_MESSAGES = 'http://api.juick.com/messages'

JUICK_MESSAGES_REQUEST = '%s?' % JUICK_MESSAGES
# Поиск по сообщениям: search=<запрос>
# Фильтрация по тегу: tag=<тег>
# Фильтрация по типу контента: media=all | media=photo | media=video
# Последние сообщения пользователя: user_id=<uid> | user_id=<uid>&tag=<тег>
# Для списков сообщений выводится одна «страница». Для вывода дополнительных «страниц»: параметры before_mid, page
# before_mid=<id последнего загруженного сообщения>&page=<page>

# Просмотр сообщения с комментариями
JUICK_THREAD = 'http://api.juick.com/thread?' # mid=<message ID>

# Получение UserID по нику:
JUICK_USERS = 'http://api.juick.com/users?' # uname=ugnich

# Популярные теги:
JUICK_TAGS = 'http://api.juick.com/tags'

# Все теги пользователя:
JUICK_TAGS_USER = '%s?' % JUICK_TAGS # user_id=<uid>

JUICK_URL = 'http://juick.com/%s'

def juick(type, jid, nick, text):
	text = text.strip()
	topt = text.split(' ',1)
	topt[0] = topt[0].lower()
	try: prm = topt[1].strip()
	except: prm = ''
	if topt[0] == 'msg' and prm: juick_msg(type, jid, nick, prm)
	elif topt[0] == 'tags': juick_tags(type, jid, nick, prm)
	elif topt[0] == 'search': juick_search(type, jid, nick, prm)
	elif topt[0] == 'user': juick_user(type, jid, nick, prm)
	else:
		try: tmpt = re.findall('(^[^@]#?[0-9]+)',text)[0]
		except: tmpt = ''
		if tmpt: juick_msg(type, jid, nick, text)
		elif text and text[0] == '@': juick_user(type, jid, nick, text)
		else: send_msg(type, jid, nick, L('Smoke help about command!','%s/%s'%(jid,nick)))

def juick_user(type, jid, nick, text):
	if text and text[0] == '@': text = text[1:]
	try: result = json.loads(html_encode(load_page(JUICK_MESSAGES_REQUEST, {'user_id':str(json.loads(html_encode(load_page(JUICK_USERS, {'uname': text})).replace('\t',' '*8))[0]['uid'])})).replace('\t',' '*8))
	except:
		send_msg(type, jid, nick, L('User @%s not found!','%s/%s'%(jid,nick)) % text)
		return
	tp = []
	for t in result[:GT('juick_user_post_limit')]:
		tm = '#%s' % t['mid']
		if t.has_key('tags'): tm = '%s *%s' % (tm, ' *'.join(t['tags']))
		tm = '%s | %s' % (tm,replacer(t['body'][:GT('juick_user_post_size')].replace('\n',' \\ ')+['',u'…'][len(t['body']) > GT('juick_user_post_size')]))
		if t.has_key('replies'): tm = '%s %s' % (tm, L('Replies: %s','%s/%s'%(jid,nick)) % t['replies'])
		tp.append(tm)
	msg = L('Found: %s','%s/%s'%(jid,nick)) % '%s\n%s' % (text,'\n'.join(tp))
	send_msg(type, jid, nick, msg)

def juick_search(type, jid, nick, text):
	result = json.loads(html_encode(load_page(JUICK_MESSAGES_REQUEST, {'search': text})).replace('\t',' '*8))
	tp = []
	for t in result[:GT('juick_user_post_limit')]:
		tm = '#%s @%s: %s' % (t['mid'],replacer(t['user']['uname']),replacer(t['body'][:GT('juick_user_post_size')].replace('\n',' \\ ')+['',u'…'][len(t['body']) > GT('juick_user_post_size')]))
		if t.has_key('replies'): tm = '%s | %s' % (tm, L('Replies: %s','%s/%s'%(jid,nick)) % t['replies'])
		if t.has_key('tags'): tm = '%s | *%s' % (tm, ' *'.join(t['tags']))
		tp.append(tm)
	msg = L('Found: %s','%s/%s'%(jid,nick)) % '\n%s' % '\n'.join(tp)
	send_msg(type, jid, nick, msg)

def juick_tags(type, jid, nick, text):
	if text and text[0] == '@': text = text[1:]
	try:
		if text: hdr,url,params = L('Popular tags of @%s:','%s/%s'%(jid,nick)) % text,JUICK_TAGS_USER,{'user_id':str(json.loads(html_encode(load_page(JUICK_USERS, {'uname': text})).replace('\t',' '*8))[0]['uid'])}
		else: hdr,url,params = L('Popular tags:','%s/%s'%(jid,nick)),JUICK_TAGS,{}
		result = json.loads(html_encode(load_page(url,params)).replace('\t',' '*8))
		tags = [((t['messages'],replacer(t['tag']))) for t in result]
		tags.sort(reverse=True)
		msg = '%s %s' % (hdr,', '.join(['%s [%s]' % (t[1],t[0]) for t in tags[:GT('juick_user_tags_limit')]]))
	except:
		if text: msg = L('User @%s not found!','%s/%s'%(jid,nick)) % text
		else: msg = L('Unknown error!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def juick_msg(type, jid, nick, text):
	j_mid,j_rid = re.findall('#?([0-9]+)\/?([0-9]+)?',text)[0]
	if j_rid:
		try: j_rid = int(j_rid)
		except: j_rid = 0
	else: j_rid = 0
	try: j_replies = int(text.split()[1])
	except: j_replies = GT('juick_msg_answers_default')
	try: result = json.loads(html_encode(load_page(JUICK_THREAD, {'mid': j_mid})).replace('\t',' '*8))
	except:
		send_msg(type, jid, nick, L('Message #%s is not found!','%s/%s'%(jid,nick)) % j_mid)
		return
	if j_rid:
		found = False
		for t in result:
			if t.has_key('rid') and t['rid'] == j_rid:
				result,found = t,True
				break
		if not found:
			send_msg(type, jid, nick, L('Message #%s is not found!','%s/%s'%(jid,nick)) % '%s/%s' % (j_mid,j_rid))
			return
	else: result=result[0]
	uname = replacer(result['user']['uname'])
	try: tags = '*%s' % ' *'.join([replacer(t) for t in result['tags']])
	except: tags = ''
	body = replacer(result['body'])
	timestamp = result['timestamp']
	mid = str(result['mid'])
	try: replies = L('Replies: %s','%s/%s'%(jid,nick)) % result['replies']
	except: replies = 0
	if result.has_key('video'):
		media = result['video']
		media = L('Attach: %s','%s/%s'%(jid,nick)) % media[media.keys()[0]]
	elif result.has_key('photo'): media = L('Attach: %s','%s/%s'%(jid,nick)) % result['photo']['medium']
	else: media = ''
	try: replyto = result['replyto']
	except: replyto = ''
	try: mid2 = '%s#%s' % (mid,result['rid'])
	except: mid2 = mid
	if replyto:
		if replies: msg = '@%s: %s\n%s\n#%s -> #%s/%s, %s, %s, %s' % (uname,tags,body,mid2.replace('#','/'),mid,replyto,timestamp,replies,JUICK_URL % mid2)
		else: msg       = '@%s: %s\n%s\n#%s -> #%s/%s, %s, %s'     % (uname,tags,body,mid2.replace('#','/'),mid,replyto,timestamp,JUICK_URL % mid2)
	else:
		if replies: msg = '@%s: %s\n%s\n#%s, %s, %s, %s' % (uname,tags,body,mid2.replace('#','/'),timestamp,replies,JUICK_URL % mid2)
		else: msg       = '@%s: %s\n%s\n#%s, %s, %s'     % (uname,tags,body,mid2.replace('#','/'),timestamp,JUICK_URL % mid2)
	if media: msg = '%s\n%s' % (msg,media)
	send_msg(type, jid, nick, msg)

def juick_post(type, jid, nick, text):
	send_msg('chat', JUICK_JID, '', text)
	time.sleep(1.2)
	send_msg(type, jid, nick, L('Message posted to Juick.','%s/%s'%(jid,nick)))

global execute

execute = [(3, 'juick', juick, 2, 'Miniblogs http://juick.com\njuick [msg][#]post - show post\njuick tags [user] - show popular tags\njuick search [text] - search text\njuick [user] @username - show messages of user'),
		   (9, 'juick_post', juick_post, 2, 'Send message to blog at juick.com')]

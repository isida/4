#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#    Copyright (C) Vit@liy <vitaliy@root.ua>                                  #
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

ANSW_PREV = {}
FLOOD_STATS = {}
LAST_PHRASE = {}

autophrases_time = {}
list_of_answers, list_of_empty, list_of_phrases_with_highlight, list_of_phrases_no_highlight, dict_of_mind = {}, {}, {}, {}, {}

llist = ['en'] + [tmp[:-4] for tmp in os.listdir(loc_folder[:-6]) if tmp[-4:]=='.txt']
for t in llist:
	if os.path.isfile(loc_folder % t): cur_lang = t
	else: cur_lang = 'en'
	chat_folder = data_folder % 'chat/%s/' % cur_lang
	MIND_FILE = chat_folder + 'mind.txt'
	EMPTY_FILE = chat_folder + 'empty.txt'
	ANSWER_FILE = chat_folder + 'answer.txt'
	PHRASES_FILE = chat_folder + 'phrases.txt'

	list_of_answers[cur_lang] = readfile(ANSWER_FILE).decode('utf-8').split('\n')
	list_of_empty[cur_lang] = readfile(EMPTY_FILE).decode('utf-8').split('\n')
	list_of_phrases_with_highlight[cur_lang] = []
	list_of_phrases_no_highlight[cur_lang] = []
	for phrase in readfile(PHRASES_FILE).split('\n'):
		if 'NICK' in phrase: list_of_phrases_with_highlight[cur_lang].append(phrase.decode('utf-8'))
		else: list_of_phrases_no_highlight[cur_lang].append(phrase.decode('utf-8'))

	dict_of_mind[cur_lang] = {}
	for p in readfile(MIND_FILE).decode('utf-8').split('\n'):
		if '||' in p:
			tmp1, tmp2 = p.strip().split('||')
			dict_of_mind[cur_lang][tmp1] = tmp2.split('|')

def addAnswerToBase(tx):
	if not len(tx) or tx.count(' ') == len(tx): return
	lent = len(cur_execute_fetchall('select ind from answer'))+1
	cur_execute('insert into answer values (%s,%s)', (lent,tx))
	if base_type not in ['sqlite3','mysql']:
		conn.commit()

def getRandomAnswer(tx,room):
	if not tx.strip(): return None
	lent = len(cur_execute_fetchall('select ind from answer'))
	mrand = random.randint(1,lent)
	answ = to_censore(cur_execute_fetchone('select body from answer where ind=%s', (mrand,))[0],room)
	return answ

def getSmartAnswer(type, room, nick, text):
	loc = get_L_('%s/%s' % (room,nick))
	if '?' in text: answ = random.choice(list_of_answers[loc]).strip()
	else: answ = random.choice(list_of_empty[loc]).strip()
	score,sc, var = 1.0,0,[answ]
	text = ' %s ' % text.upper()
	for answer in dict_of_mind[loc]:
		sc = rating(answer, text, room)
		if sc > score: score,var = sc,dict_of_mind[loc][answer]
		elif sc == score: var += dict_of_mind[loc][answer]

	return random.choice(var)

def rating(s, text, room):
	r,s = 0.0,s.split('|')
	for k in s:
		if k in text: r += 1
		if k in ANSW_PREV.get(room, ''): r += 0.5
	return r

def getAnswer(type, room, nick, text):
	text = text.strip()
	if get_config(getRoom(room),'flood') in ['random',True]: answ = getRandomAnswer(text,room)
	else:
		answ = getSmartAnswer(type, room, nick, text)
		ANSW_PREV[room] = text.upper()
	if type == 'groupchat' and text == to_censore(text,room): addAnswerToBase(text)
	return answ

def flood_action(room,jid,nick,type,text):
	if get_config(room,'autoflood'):
		jjid = getRoom(jid)
		tm = time.time()
		prefix = get_local_prefix(room)
		first_word = text.split(' ', 1)[0]
		cur_alias = cur_execute_fetchall('select match from alias where room=%s',(room,))
		if cur_alias: cur_alias = [t[0] for t in cur_alias]
		else: cur_alias = []
		if nick in [get_xnick(room), ''] or cur_execute_fetchone('select pattern from bot_ignore where %s ilike pattern',(jjid,)) or ddos_ignore.has_key(jjid): return
		if first_word in [prefix + i[1] for i in comms] + cur_alias or first_word[:-1] in [d[1] for d in megabase if d[0]==room]:
			if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][0] != jjid: FLOOD_STATS[room] = ['', 0, 0]
			return
		if not FLOOD_STATS.has_key(room) or FLOOD_STATS[room][0] != jjid: FLOOD_STATS[room] = [jjid, tm, 1]
		else: FLOOD_STATS[room][2] += 1
		if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][2] >= get_config_int(room,'floodcount') and tm - FLOOD_STATS[room][1] > get_config_int(room,'floodtime'):
			pprint('Send msg human: %s/%s [%s] <<< %s' % (room,nick,type,text),'dark_gray')
			try:
				msg = getAnswer(type, room, nick, text)
				if text: send_msg_human(type, room, nick, msg, 'msg_human_auto')
				else: return False
			except: return False
			return True
	if get_config(room,'floodrepeat') != 'off' and get_level(room,nick)[0] > 0:
		text = text.strip()
		if LAST_PHRASE.has_key(room) and LAST_PHRASE[room][0] != jid and LAST_PHRASE[room][2] == text:
			if LAST_PHRASE[room][1] >= get_config_int(room,'floodrepeat') - 1:
				try: LAST_PHRASE.pop(room)
				except: pass
				pprint('Send msg human repeat: %s/%s [%s] <<< %s' % (room,nick,type,text),'dark_gray')
				try: send_msg_human(type, room, '', text, 'msg_human_repeat')
				except: return False
				return True
			else: LAST_PHRASE[room] = [jid,LAST_PHRASE[room][1] + 1,text]
		else: LAST_PHRASE[room] = [jid,1,text]
	return False

def phrases_timer():
	for room in list(set([i[0] for i in megabase])):
		if get_config(room,'autophrases') != 'off':
			a_time = int(get_config(room,'autophrasestime'))
			if not room in autophrases_time:
				autophrases_time[room] = time.time() + random.normalvariate(a_time, a_time/12.0)/2
			if time.time() > autophrases_time[room]:
				autophrases_time[room] = time.time() + random.normalvariate(a_time, a_time/12.0)
				if get_config(room,'autophrases') == 'all':
					rand_nicks = [d[1] for d in megabase if d[0]==room if not cur_execute_fetchone('select pattern from bot_ignore where %s ilike pattern',(getRoom(d[4]),)) and d[1] not in [get_xnick(room), '']]
					if rand_nicks:
						nick = random.choice(rand_nicks)
						loc = get_L_('%s/%s' % (room,nick))
						msg = random.choice(list_of_phrases_with_highlight[loc] + list_of_phrases_no_highlight[loc])
						msg = msg.replace('NICK', nick)
				if get_config(room,'autophrases') == 'without highlight' or not rand_nicks: msg = random.choice(list_of_phrases_no_highlight[CURRENT_LOCALE])
				pprint('Send autophrase: %s >>> %s' % (room, msg), 'dark_gray')
				send_msg('groupchat', room, '', msg)

global execute, message_act_control, timer

message_act_control = [flood_action]
timer = [phrases_timer]
execute = []

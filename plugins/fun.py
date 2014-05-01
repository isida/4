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

LAST_RANDOM_POKE = {}
LAST_POKE_PHRASE = {}

def poem(type, jid, nick):
	dict = [[u'я помню',u'не помню',u'забыть бы',u'купите',u'очкуешь',u'какое',u'угробил',u'открою',u'ты чуешь?'],
			[u'чудное',u'странное',u'некое',u'вкусное',u'пьяное',u'свинское',u'чоткое',u'сраное',u'нужное',u'конское'],
			[u'мгновенье,',u'затменье,',u'хотенье,',u'варенье,',u'творенье,',u'везенье,',u'рожденье,',u'смущенье,',u'печенье,',u'ученье,'],
			[u'\n'],
			[u'передомной',u'под косячком',u'на кладбище',u'в моих мечтах',u'под скальпилем',u'в моих штанах',u'из-за угла',u'в моих ушах',u'в ночном горшке',u'из головы',],
			[u'явилась ты,',u'добилась ты,',u'торчат кресты,',u'стихов листы,',u'забилась ты,',u'мои трусы,',u'поют дрозды,',u'из темноты,',u'помылась ты,',u'дают пизды,'],
			[u'\n'],
			[u'как'],
			[u'мимолётное',u'детородное',u'психотропное',u'кайфоломное',u'очевидное',u'у воробушков',u'эдакое вот',u'нам не чуждое',u'благородное',u'ябывдульское'],
			[u'виденье,',u'сиденье,',u'паренье,',u'сужденье,',u'вращенье,',u'сношенье,',u'смятенье,',u'теченье,',u'паденье,',u'сплетенье,'],
			[u'\n'],
			[u'как'],
			[u'гений',u'сторож',u'символ',u'спарта',u'правда',u'ангел',u'водка',u'пиво',u'ахтунг',u'жопа'],
			[u'чистой',u'вечной',u'тухлой',u'просит',u'грязной',u'липкой',u'на хрен',u'в пене',u'женской',u'жаждет'],
			[u'красоты',u'мерзлоты',u'суеты',u'наркоты',u'срамоты',u'школоты',u'типа ты',u'простоты',u'хуеты',u'наготы']]
	send_msg(type, jid, nick, '\n %s' % ' '.join([random.choice(t) for t in dict]))

def oracle(type, jid, nick, text):
	if not text.strip() or text.strip()[-1] != '?': msg = L('What?','%s/%s'%(jid,nick))
	else: msg = random.choice([L('Yes','%s/%s'%(jid,nick)),
			L('Yes - definitely','%s/%s'%(jid,nick)),
			L('You may rely on it','%s/%s'%(jid,nick)),
			L('Without a doubt','%s/%s'%(jid,nick)),
			L('Signs point to yes','%s/%s'%(jid,nick)),
			L('Outlook good','%s/%s'%(jid,nick)),
			L('Most likely','%s/%s'%(jid,nick)),
			L('It is decidedly so','%s/%s'%(jid,nick)),
			L('It is certain','%s/%s'%(jid,nick)),
			L('As I see it, yes','%s/%s'%(jid,nick)),
			L('Reply hazy, try again','%s/%s'%(jid,nick)),
			L('Ask again later','%s/%s'%(jid,nick)),
			L('Better not tell you now','%s/%s'%(jid,nick)),
			L('Cannot predict now','%s/%s'%(jid,nick)),
			L('Concentrate and ask again','%s/%s'%(jid,nick)),
			L('Don\'t count on it','%s/%s'%(jid,nick)),
			L('My reply is no','%s/%s'%(jid,nick)),
			L('Outlook not so good','%s/%s'%(jid,nick)),
			L('My sources say no','%s/%s'%(jid,nick))])
	send_msg(type, jid, nick, msg)

def coin(type, jid, nick, text):
	msg = random.choice([L('Head','%s/%s'%(jid,nick)), L('Tail','%s/%s'%(jid,nick))])
	send_msg(type, jid, nick, msg)

def to_poke(type, jid, nick, text):
	if len(text): text = text.strip()
	if type == 'chat' and get_level(jid,nick)[0] < 7:
		send_msg(type, jid, nick, L('For members this command not available in private!','%s/%s'%(jid,nick)))
		return
	predef_poke = [L('gave NICK ... just gave ... :-\"','%s/%s'%(jid,nick)),
			L('poked a stick NICK in the eye ...','%s/%s'%(jid,nick)),
			L('suggested NICK shrimp :-[','%s/%s'%(jid,nick)),
			L('fed NICK laxative with powdered glass!','%s/%s'%(jid,nick)),
			L('whispered in his ear softly NICK LOL!','%s/%s'%(jid,nick)),
			L('trying kick the ass NICK','%s/%s'%(jid,nick)),
			L('threw the crowbar aside NICK','%s/%s'%(jid,nick)),
			L('gave NICK strawberry poison','%s/%s'%(jid,nick)),
			L('jumped around with a tambourine NICK','%s/%s'%(jid,nick)),
			L('sticking NICK with the words "buy ice cream, you creep!"','%s/%s'%(jid,nick))]
	owner = get_level(jid,nick)[0] == 9
	dpoke = getFile(poke_file,predef_poke)
	t_cmd = text.lower()
	if t_cmd == 'show' and owner:
		if type == 'groupchat':
			send_msg(type, jid, nick, L('Sent in private message','%s/%s'%(jid,nick)))
			type = 'chat'
		msg = '%s\n%s' % (L('Phrases:','%s/%s'%(jid,nick)),'\n'.join(['%s. %s' % (c+1,t) for c,t in enumerate(dpoke)]))
	elif t_cmd.startswith('del ') and owner:
		text = text[4:]
		try: pos = int(text)-1
		except: pos = len(dpoke)+1
		if pos < 0 or pos > len(dpoke): msg = L('The record doesn\'t exist!','%s/%s'%(jid,nick))
		else:
			remove_body = dpoke[pos]
			dpoke.remove(remove_body)
			writefile(poke_file, str(dpoke))
			msg = L('Removed: %s','%s/%s'%(jid,nick)) % remove_body
	elif t_cmd.startswith('add ') and owner:
		text = text[4:]
		if 'NICK' in text:
			dpoke.append(text)
			writefile(poke_file, str(dpoke))
			msg = L('Added','%s/%s'%(jid,nick))
		else: msg = L('I can\'t add it! No keyword "NICK"!','%s/%s'%(jid,nick))
	elif get_level(jid,text)[1] == selfjid: msg = L('I ban a ip for such jokes!','%s/%s'%(jid,nick))
	else:
		if not text:
			nick_list = [d[1] for d in megabase if d[0]==jid and d[4] != Settings['jid'] and d[1] != nick]
			if nick_list:
				curr_nick = random.choice(nick_list)
				try: last_nick = LAST_RANDOM_POKE[jid]
				except: last_nick = ''
				if len(nick_list) > 1:
					while curr_nick == last_nick: curr_nick = random.choice(nick_list)
				LAST_RANDOM_POKE[jid] = curr_nick
				text, is_found = curr_nick, True
			else: is_found = False
		else:
			is_found = False
			for tmp in megabase:
				if tmp[0] == jid and tmp[1] == text:
					is_found = True
					break
		if is_found:
			try: hl_pokes = list_of_phrases_with_highlight[get_L_('%s/%s'%(jid,nick))]
			except: hl_pokes = []
			dp = ['/me %s' % t for t in dpoke]
			for t in hl_pokes:
				if t and t not in dp: dp.append(t)
			try: last_poke = LAST_POKE_PHRASE[jid]
			except: last_poke = ''
			msg = random.choice(dp)
			while last_poke == msg: msg = random.choice(dp)
			LAST_POKE_PHRASE[jid] = msg
			msg,nick,type = msg.replace('NICK',text),'','groupchat'
		elif text: msg = L('I could be wrong, but %s not is here...','%s/%s'%(jid,nick)) % text
		else: msg = L('Masochist? 8-D','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def life(type, jid, nick, text):
	text = reduce_spaces_all(text)
	try:
		tmp = text.split(' ')
		d,m,y = tmp[0].strip().split('.')
		y = int(y)
		if y<20: y += 2000
		elif y<100: y += 1900
		y = str(y)
		if len(tmp)>1: hour, minute, sec = tmp[1].strip().split(':')
		else: hour, minute, sec = '00','00','00'
		BDate = time.mktime(time.strptime(' '.join([y, m, d, hour, minute, sec]), '%Y %m %d %H %M %S'))
		CDate = time.time()
		Age = CDate-BDate
		yrs = int(round(Age/31557600))
		dys = int(round(Age/86400))
		hrs = int(round(Age/3600))
		mins = int(round(Age/60))
		secs = int(round(Age))
		spal = int(round(Age*3285/31557600))
		spal24 = int(round(Age*136.9/31557600))
		morgnyl = int(round(Age*4160000/31557600))
		serdcelit = int(round(Age*2372500/31557600))
		serdceraz = int(round(Age*36500000/31557600))
		vodal = int(round(Age*750/31557600))
		voda = int(round(Age*21/31557600))
		volosicm = int(round(Age*18/31557600))
		volosi = int(round(Age*25550/31557600))
		volosivse = int(round(Age*14/31557600))
		nogtiryk = int(round(Age*5.2/31557600))
		nogtinog = int(round(Age*1.4/31557600))
		vozdyx = int(round(Age*3784320/31557600))
		vozdyxkg = int(round(Age*4881/31557600))
		pot = int(round(Age*252/31557600))
		mochalit = int(round(Age*489/31557600))
		sluni = int(round(Age*337/31557600))
		nervi = int(round(Age*136/31557600))
		smex = int(round(Age*5475/31557600))
		km = int(round(Age*1857/31557600))
		msg = L('You live %s years or %s days or %s hours or %s minutes or %s seconds.\nYou slept %s hours, or %s days.\nYou blink about %s times.\nYour heart pumped %s liters of blood and made %s strikes.\nYou drank %s liters of water and drank it %s hours.\nYou have increased by %s centimeters in my head of hair, dropped %s pieces, all of the hair %s kilometers.\nYou grew up in the hands %s centimeters and in the feet %s centimeters nails.\nYou breathed %s liters of air a total weight of %s kilograms.\nYou have stood out %s liters of sweat, and %s liters of urine, and %s liters of saliva.\nYou lost %s billion nerve cells.\nYou laughed %s times.\nYou\'ve gone %s kilometers','%s/%s'%(jid,nick)) % (yrs, dys, hrs, mins, secs, spal, spal24, morgnyl, serdcelit, serdceraz, vodal, voda, volosicm, volosi, volosivse, nogtiryk, nogtinog, vozdyx, vozdyxkg, pot, mochalit, sluni, nervi, smex, km)
		if type == 'groupchat': send_msg(type, jid, nick, L('Send for you in private','%s/%s'%(jid,nick)))
		send_msg('chat', jid, nick, msg)
	except: send_msg(type, jid, nick, L('Smoke help about command!','%s/%s'%(jid,nick)))

def zalgo(type, jid, nick, text):
	zalgo_threshold = 10
	zalgo_chars = [unichr(i) for i in range(0x0300, 0x036F + 1)]
	zalgo_chars.extend([u'\u0488', u'\u0489'])
	zalgoized = []
	for letter in text:
		zalgoized.append(letter)
		zalgo_num = random.randint(0, zalgo_threshold) + 1
		for _ in range(zalgo_num):
			zalgoized.append(random.choice(zalgo_chars))
	msg = random.choice(zalgo_chars).join(zalgoized)
	send_msg(type,jid,nick,msg)

def godville(type, jid, nick, text):
	text = text.strip()
	if ' ' in text:
		mode, name = text.split(' ', 1)
	else:
		mode, name = 'last', text
	if not mode in ['stat', 'extstat', 'last', 'inv', 'quest']:
		mode, name = 'last', text
	data = load_page('http://godville.net/gods/api/%s.json' % name.encode('utf-8'))
	try:
		data = json.loads(data)
		if mode == 'last':
			try:
				msg = '%s: %s' % (data['name'], data['diary_last'])
			except:
				msg = L('Turn on extended API on game\'s settings','%s/%s'%(jid,nick))
		elif mode in ['stat', 'extstat']:
			msg = L('Name: %s\n','%s/%s'%(jid,nick)) % data['name']
			msg += L('Gold: %s\n','%s/%s'%(jid,nick)) % data['gold_approx']
			msg += L('Level: %s\n','%s/%s'%(jid,nick)) % data['level']
			msg += L('Alignment: %s\n','%s/%s'%(jid,nick)) % data['alignment']
			msg += L('Motto: %s','%s/%s'%(jid,nick)) % data['motto']
			if data['clan']:
				msg += L('\nClan: %s (%s)','%s/%s'%(jid,nick)) % (data['clan'], data['clan_position'])
			if mode == 'extstat' and 'godpower' in data:
				msg += L('\nHealth: %s/%s\n','%s/%s'%(jid,nick)) % (data['health'], data['max_health'])
				msg += L('Bricks: %s\n','%s/%s'%(jid,nick)) % data['bricks_cnt']
				msg += L('Godpower: %s%%','%s/%s'%(jid,nick)) % data['godpower']
		elif mode == 'inv':
			if data['inventory']:
				msg = L('Inventory: %s','%s/%s'%(jid,nick)) % ', '.join(data['inventory'].keys())
			else:
				msg = L('Inventory: %s','%s/%s'%(jid,nick)) % L('Not found!','%s/%s'%(jid,nick))
		elif mode == 'quest':
			msg = '%s: %s' % (data['name'], data['quest'])
	except:
		msg = L('User not found','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(3, 'poem', poem, 1, 'Just funny poem'),
		(3, 'oracle', oracle, 2, 'Prophecy oracle. Example: oracle your_answer?'),
		(3, 'coin', coin, 2, 'Heads or tails'),
		(3, 'poke', to_poke, 2, '"Poke" command\npoke nick - say a random phrase for nick\nControls command, available only for bot owner:\npoke show - show list of phrases\npoke add phrase - add phrase\npoke del phrase_number - remove phrase.'),
		(3, 'life', life, 2, 'Info about your life. Example: life dd.mm.yy [hour:min:sec]'),
		(3, 'zalgo', zalgo, 2, 'Zalgo translate'),
		(3, 'godville', godville, 2, 'Information about hero from Godville.net.\ngodville [last|stat|extstat|inv|quest] username')]

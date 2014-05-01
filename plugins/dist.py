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

dist_max_search_limit = 100
dist_default_search_count = 10

def points2distance(start, end):
	"""
		Calculate distance (in kilometers) between two points given as (latt, long) pairs
		based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
	"""
	start_latt = math.radians(start[0])
	start_long = math.radians(start[1])
	end_latt = math.radians(end[0])
	end_long = math.radians(end[1])
	d_long = end_long - start_long
	a = (math.cos(end_latt) * math.sin(d_long))**2 + (math.cos(start_latt)*math.sin(end_latt)-math.sin(start_latt)*math.cos(end_latt)*math.cos(d_long))**2
	b = math.sin(start_latt)*math.sin(end_latt) + math.cos(start_latt)*math.cos(end_latt)*math.cos(d_long)
	dist = math.atan2(math.sqrt(a), b) * 6372.795
	dist = int(dist + 0.5)
	return dist

def city_capitalize(s):
	s = s.capitalize()
	for k in re.findall('[ -].', s): s = s.replace(k,k.upper())
	for tmp in [u'-На-', u' На ', u'-Де-', u' Де ']: s = s.replace(tmp, tmp.lower())
	return s

def city(type, jid, nick, text):
	parameters = text.strip().split(' ', 1)
	if parameters[0] == 'add' and get_level(jid,nick)[0] == 9:
		try:
			tmp = parameters[1].split('\n', 1)
			place = tmp[0].strip().lower().replace(' - ', '-')
			if len(tmp) == 2:
				coords = re.sub('[^-\.\d]+', ' ', tmp[1]).strip().split()
				if abs(float(coords[0])) < 90 and abs(float(coords[1])) < 180:
					if not cur_execute_fetchone('select * from dist_user where point ilike %s',(place,)):
						cur_execute('insert into dist_user values (%s,%s,%s)',(place,coords[1],coords[0]))
						if base_type not in ['sqlite3','mysql']:
							conn.commit()
						msg = L('Added!','%s/%s'%(jid,nick))
					else: msg = L('This point is in database!','%s/%s'%(jid,nick))
			elif len(GT('yandex_api_key')) > 60:
				text = place.encode('utf-8')
				url = 'http://geocode-maps.yandex.ru/1.x/?geocode=%s&key=%s&format=json&results=1' % (urllib.quote_plus(text), GT('yandex_api_key'))
				j = json.loads(load_page(url))
				place_ext = j['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
				coords = j['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
				if not cur_execute_fetchone('select * from dist_user where point ilike %s',(place,)):
					cur_execute('insert into dist_user values (%s,%s,%s)',(place,coords[1],coords[0]))
					if base_type not in ['sqlite3','mysql']:
						conn.commit()
					msg = L('Added: ','%s/%s'%(jid,nick)) + place_ext + L(' as ','%s/%s'%(jid,nick)) + '"%s"' % place
				else: msg = L('This point is in database!','%s/%s'%(jid,nick))
			else: msg = L('Not found Yandex.Map API. Get API-key on http://api.yandex.ru/maps/form.xml','%s/%s'%(jid,nick))
		except: msg = L('What?','%s/%s'%(jid,nick))
	elif parameters[0] == 'del' and get_level(jid,nick)[0] == 9:
		if cur_execute_fetchone('select * from dist_user where point ilike %s',(parameters[1].lower(),)):
			cur_execute('delete from dist_user where point=%s',(parameters[1].lower(),))
			if base_type not in ['sqlite3','mysql']:
				conn.commit()
			msg = L('Deleted!','%s/%s'%(jid,nick))
		else: msg = L('This point isn\'t in database!','%s/%s'%(jid,nick))
	elif parameters[0] == 'map':
		t = cur_execute_fetchone('select * from dist_user where point ilike %s',(parameters[1].lower(),))
		if not t: t = cur_execute_fetchone('select * from dist where point ilike %s',(parameters[1].lower(),))
		if t:
			tmp = 'http://maps.google.com/maps?ll=%s,%s&spn=0.01,0.01&t=h&q=%s,%s' % (t[1], t[2], t[1], t[2])
			try: msg = city_capitalize(parameters[1]) + L(' on the map: ','%s/%s'%(jid,nick)) + load_page(SHORT_TINYURL % enidna(tmp).decode('utf-8'))
			except: msg = city_capitalize(parameters[1]) + L(' on the map: ','%s/%s'%(jid,nick)) + tmp
		else: msg = L('What?','%s/%s'%(jid,nick))
	elif parameters[0] == 'search':
		if len(GT('yandex_api_key')) > 60:
			text = parameters[1].encode('utf-8')
			text_tmp = text.split(' ', 1)
			if re.match('\d+$', text_tmp[0]):
				results = text_tmp[0]
				text = text_tmp[1]
				skip = '0'
			elif re.match('\d+[-: |]\d+$', text_tmp[0]):
				tmp = re.sub('[-: |]', ' ', text_tmp[0]).split()
				results = int(tmp[1]) - int(tmp[0]) + 1
				skip = int(tmp[0]) - 1
				text = text_tmp[1]
			else: results, skip = '5', '0'
			url = 'http://geocode-maps.yandex.ru/1.x/?geocode=%s&key=%s&format=json&results=%s&skip=%s' % (urllib.quote_plus(text), GT('yandex_api_key'), results, skip)
			j = json.loads(load_page(url))
			msg = ''
			for object in j['response']['GeoObjectCollection']['featureMember']:
				msg += object['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
				msg += ' - (%s)\n' % ', '.join(object['GeoObject']['Point']['pos'].split()[::-1])
			if msg: msg = '\n' + msg
			else: msg = L('Not found!','%s/%s'%(jid,nick))
		else: msg = L('Not found Yandex.Map API. Get API-key on http://api.yandex.ru/maps/form.xml','%s/%s'%(jid,nick))
	else:
		t = cur_execute_fetchone('select * from dist_user where point ilike %s',(text.strip().lower(),))
		if not t:
			t = cur_execute_fetchone('select * from dist where point ilike %s',(text.strip().lower(),))
			if t: msg = L(u'%s - latitude: %s, longtitude: %s') % (city_capitalize(t[0]), t[1], t[2])
			else: msg = L('Not found!','%s/%s'%(jid,nick))
		else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

def dist(type, jid, nick, text):
	text,splitter,splitted,points = text.strip(),[' - ','|','\n',' '],False,''
	if ' ' in text and text.split(' ',1)[0].lower() == 'search':
		try:
			dist_count = int(text.split(' ',2)[2])
			dist_count = 1 if dist_count < 1 else dist_max_search_limit if dist_count > dist_max_search_limit else dist_count
		except: dist_count = dist_default_search_count
		tmp = cur_execute_fetchall('select point from dist_user where point ilike %s order by point limit %s',('%%%s%%' % text.split(' ',2)[1].lower(),dist_count))
		if not tmp: tmp = cur_execute_fetchall('select point from dist where point ilike %s order by point limit %s',('%%%s%%' % text.split(' ',2)[1].lower(),dist_count))
		if tmp: msg = L('Found: %s','%s/%s'%(jid,nick)) % ', '.join(map(city_capitalize, [t[0] for t in tmp]))
		else: msg = L('City %s not found','%s/%s'%(jid,nick)) % city_capitalize(text.split(' ',2)[1])
	else:
		for tmp in splitter:
			if tmp in text:
				points,splitted = text.split(tmp),True
				break
		if splitted and len(points)==2:
			t1 = cur_execute_fetchone('select * from dist_user where point ilike %s',(points[0].lower(),))
			t2 = cur_execute_fetchone('select * from dist_user where point ilike %s',(points[1].lower(),))
			if not t1 or not t2:
				if not t1: t1 = cur_execute_fetchone('select * from dist where point ilike %s',(points[0].lower(),))
				if not t2: t2 = cur_execute_fetchone('select * from dist where point ilike %s',(points[1].lower(),))
			if t1 and t2: msg = L('%s km','%s/%s'%(jid,nick)) % points2distance((float(t1[1]), float(t1[2])), (float(t2[1]), float(t2[2])))
			elif t1: msg = L('City %s not found','%s/%s'%(jid,nick)) % city_capitalize(points[1])
			elif t2: msg = L('City %s not found','%s/%s'%(jid,nick)) % city_capitalize(points[0])
			else: msg = L('Cities not found','%s/%s'%(jid,nick))
		else: msg = L('Error in parameters. Read the help about command.','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(3, 'dist', dist, 2, 'Distance between cities.\ndist search city [count of cities]\ndist city1 - city2'),
			(3, 'city', city, 2, 'Cities and other place-name of the world. Examples:\ncity add place-name\n[latitude, longtitude] - add city to database\ncity del place-name - delete city from database\ncity search [count of results|range of results] place-name - search city\ncity map place-name - city on the map\ncity place-name - coordinates of city')]

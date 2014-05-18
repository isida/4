#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    GEOIP to PostgreSQL                                                      #
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
# REQUIRED: wget, unzip                                                       #
# --------------------------------------------------------------------------- #

import csv,os

URL = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip'
DUMP = 'geoip.dump'

_SQL1 = '''DROP TABLE geoip_blocks;
CREATE TABLE geoip_blocks (
	startIpNum bigint,
	endIpNum bigint,
	locId integer
);
INSERT INTO geoip_blocks VALUES'''

_SQL2 = '''(0,0,0);
CREATE INDEX geoip_blocks_1 ON geoip_blocks (startIpNum,endIpNum,locId);
CREATE INDEX geoip_blocks_2 ON geoip_blocks (locId,startIpNum,endIpNum);
DELETE FROM geoip_blocks WHERE locId=0;'''

_SQL3 = '''DROP TABLE geoip_location;
CREATE TABLE geoip_location (
	locId integer,
	country text,
	region text,
	city text,
	postalCode text,
	latitude real,
	longitude real,
	metroCode text,
	areaCode text
);
INSERT INTO geoip_location VALUES'''

_SQL4 = '''(0,'','','','',0,0,'','');
CREATE INDEX geoip_location_1 ON geoip_location (locId);
DELETE FROM geoip_location WHERE locId=0;'''

print 'Download GEOIP file'

ZIPFILE = URL.split('/')[-1]

try: os.remove(ZIPFILE)
except: pass
os.system('wget %s' % URL)
os.system('unzip %s' % ZIPFILE)
try: os.remove(ZIPFILE)
except: pass

FOLDER = [t for t in os.listdir('.') if t.startswith(ZIPFILE.split('-',1)[0]) and os.path.isdir(t)][0]
BLOCKS_CSV = '%s/GeoLiteCity-Blocks.csv' % FOLDER
LOCATION_CSV = '%s/GeoLiteCity-Location.csv' % FOLDER

print 'Remove old dump file: %s' % DUMP

try: os.remove(DUMP)
except: pass

DMP = open(DUMP, 'a')
# ------------- Blocks -------------
DMP.write(_SQL1)
print 'Parse: %s' % BLOCKS_CSV

csvfile = open(BLOCKS_CSV, 'rb')
csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
CNT = 0
for row in csvreader:
	if len(row) > 1 and row[0].isdigit():
		ROW = '(%s),\n' % ','.join(row)
		DMP.write(ROW)
		CNT += 1
	if not CNT % 10000:
		os.system('printf "."')
		DMP.write('(0,0,0);\nINSERT INTO geoip_blocks VALUES')

print '\nTotal blocks: %s' % CNT
		
DMP.write(_SQL2)
# ------------- Location -------------
DMP.write(_SQL3)

print 'Parse: %s' % LOCATION_CSV

csvfile = open(LOCATION_CSV, 'rb')
csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
CNT = 0
for row in csvreader:
	if len(row) > 1 and row[0].isdigit():
		ROW = '(%s),\n' % ','.join(["'%s'" % t.replace("'","`") for t in row])
		try: ROW = ROW.decode('latin-1').encode('utf8')
		except:
			print 'Error!', ROW
			ROW = ''.join([['?',l][l<='~'] for l in ROW])
		DMP.write(ROW)
		CNT += 1
	if not CNT % 10000:
		os.system('printf "."')
		DMP.write('(0,\'\',\'\',\'\',\'\',0,0,\'\',\'\');\nINSERT INTO geoip_location VALUES')

print '\nTotal locations: %s' % CNT

DMP.write(_SQL4)
DMP.close()

print 'Import dump file to PostgreSQL'
os.system('psql -U isidabot isidabot -f %s' % DUMP)

print 'Done!'
# The end is near!

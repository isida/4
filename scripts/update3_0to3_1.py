import os, sys

global clean, rename, cur, conn

os.chdir('..')
settings_folder = 'settings/%s'
conference_config_path = settings_folder % 'conference.config'
owner_config_path = settings_folder % 'owner.config'
configname = settings_folder % 'config.py'
topbase_path = settings_folder % 'topbase.db'
aliases_path = settings_folder % 'aliases'
blacklist_path = settings_folder % 'blacklist.db'
conoff_path = settings_folder % 'commonoff'
conf_path = settings_folder % 'conf'
feed_path = settings_folder % 'feed'
hidenrooms_path = settings_folder % 'hidenroom.db'
botignore_path = settings_folder % 'ignore'
botowner_path = settings_folder % 'owner'
locale_path = settings_folder % 'locale'
logroom_path = settings_folder % 'logroom.db'
spy_path = settings_folder % 'spy.db'
tban_path = settings_folder % 'temporary.ban'
saytoowner_path = settings_folder % 'saytoowner.db'
ignoreban_path = settings_folder % 'ignoreban.db'

ar = {'--help':'This page',
	  '--all':'Import all files',
	  '--owner-config':'Import owners config',
	  '--conference-config':'Import conference config',
	  '--top':'Import statictic for `top` command',
	  '--alias':'Import aliases',
	  '--blacklist':'Import blacklist of rooms',
	  '--comm':'Import list of disabled commands',
	  '--rooms':'Import list of bot\'s rooms',
	  '--rss':'Import RSS/ATOM feeds',
	  '--hiden-rooms':'Import list of hiden rooms',
	  '--bot-ignore':'Import patterns for bot ignore',
	  '--locale':'Import current locale name',
	  '--logs':'Import rooms with enabled logs',
	  '--bot-owner':'Import list of bot owners',
	  '--spy':'Import spy for room activity',
	  '--tban':'Import list of temporary bans',
	  '--say-to-owner':'Import base for `msgtoadmin` command',
	  '--ignore-ban':'Import list of rooms with ignore global ban',
	  '--clean':'Remove source file(s) after import',
	  '--rename':'Rename source file(s) after import'
	  }


def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def errorHandler(text):
	print text
	sys.exit()

def mv(file):
	newfile = file.split('/')
	newfile = '/'.join(newfile[:-1]+['_%s' % newfile[-1]])
	os.system('mv %s %s' % (file,newfile))

def remove(file):
	try: os.remove(file)
	except: pass

def import_file(filename,basename,eval_for,eval_string):
	try:
		print 'Import: %s' % filename
		c = eval(readfile(filename))
		cnt = 0
		for t in eval(eval_for):
			r = eval(eval_string)
			req = 'insert into %s values(%s);' % (basename,','.join(['%'+a for a in 's'*len(r)]))
			cnt += 1
			cur.execute(req,r)
		print '\t%s record(s)' % cnt
		conn.commit()
		if rename: mv(filename)
		elif clean: remove(filename)
	except Exception, SM: print 'Error [%s] while proceed file %s' % (str(SM),filename)

print 'Updater for Isida Jabber Bot from 3.0 to 3.1'
print '(c) Disabler Production Lab.'

base_charset, base_type = 'utf8', 'pgsql'

if os.path.isfile(configname): execfile(configname)
else: errorHandler('%s is missed.' % configname)

try: _,_,_,_,_ = base_name,base_user,base_host,base_pass,base_port
except: errorHandler('Missed settings for SQL DB!')

arg = sys.argv[1:]

if arg:
	clean = '--clean' in arg
	rename = '--rename' in arg
	all = '--all' in arg
	if '--help' in arg:
		ark = ar.keys()
		ark.sort()
		print 'Usage:\n%s' % '\n'.join(['%-32s%s' % (t,ar[t]) for t in ark])
	else:
		for t in arg:
			if t not in ar.keys():
				print 'Unknown option: %s\nUse `--help` option' % t
				os._exit(0)
		if base_type == 'pgsql':
			import psycopg2
			conn = psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
		elif base_type == 'mysql':
			import MySQLdb
			conn = MySQLdb.connect(db=base_name, user=base_user, host=base_host, passwd=base_pass, port=int(base_port), charset=base_charset)
		else: errorHandler('Unknown database backend!')

		print 'Base type: %s' % base_type
		cur = conn.cursor()

		# --------- Conference config  --------- #
		if '--conference-config' in arg or all:
			try:
				print 'Import: %s' % conference_config_path
				c = eval(readfile(conference_config_path))
				to_base,cnt = 'config_conf',0
				for t in c.keys():
					for tmp in c[t].keys():
						r = (t,tmp,unicode(c[t][tmp]))
						req = 'insert into %s values(%s);' % (to_base,','.join(['%'+a for a in 's'*len(r)]))
						cnt += 1
						cur.execute(req,r)
				print '\t%s record(s)' % cnt
				conn.commit()
				if rename: mv(conference_config_path)
				elif clean: remove(conference_config_path)
			except Exception, SM: print 'Error [%s] while proceed file %s' % (str(SM),conference_config_path)

		# --------- Owner config  --------- #
		if '--owner-config' in arg or all: import_file(owner_config_path,'config_owner','c.keys()','(t,unicode(c[t]))')

		# --------- Top command  --------- #
		if '--top' in arg or all: import_file(topbase_path,'top','c','t')

		# --------- Aliases  --------- #
		if '--alias' in arg or all: import_file(aliases_path,'alias','c','t')

		# --------- Blacklist of rooms  --------- #
		if '--blacklist' in arg or all: import_file(blacklist_path,'blacklist','c','(t,)')

		# --------- Comm ON/OFF  --------- #
		if '--comm' in arg or all: import_file(conoff_path,'commonoff','c','t')
			
		# --------- Conferences list  --------- #
		if '--rooms' in arg or all: import_file(conf_path,'conference','c',"list(t.split('\\n',1)+[''])[:2]")

		# --------- Feeds  --------- #
		if '--rss' in arg or all: import_file(feed_path,'feed','c','t')

		# --------- Hiden rooms  --------- #
		if '--hiden-rooms' in arg or all: import_file(hidenrooms_path,'hiden_rooms','c','(t,)')
			
		# --------- Bot Ignore  --------- #
		if '--bot-ignore' in arg or all: import_file(botignore_path,'bot_ignore','c',"[('%%%s%%' % t,),(t,)]['@' in t]")
			
		# --------- Bot Locale  --------- #
		if '--locale' in arg or all: import_file(locale_path,'config_owner','range(0,1)',"('bot_locale',c)")

		# --------- Logs in rooms  --------- #
		if '--logs' in arg or all: import_file(logroom_path,'log_rooms','c','(t,)')

		# --------- Bot owners  --------- #
		if '--bot-owner' in arg or all: import_file(botowner_path,'bot_owner','c','(t,)')

		# --------- Spy for rooms activity  --------- #
		if '--spy' in arg or all: import_file(spy_path,'spy','c','t')

		# --------- Temporary ban  --------- #
		if '--tban' in arg or all: import_file(tban_path,'tmp_ban','c','t')

		# --------- Say to owner  --------- #
		if '--say-to-owner' in arg or all: import_file(saytoowner_path,'saytoowner','c.keys()','(t,c[t])')

		# --------- Ignore ban --------- #
		if '--ignore-ban' in arg or all: import_file(ignoreban_path,'ignore_ban','c','(t,)')

		print 'Finished!'
		cur.close()
		conn.commit()
		conn.close()

else: print 'use `--help` option'

# The end is near!

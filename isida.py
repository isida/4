#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida Jabber Bot                                                         #
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

import os, sys, time, re, traceback, threading

sys.path = ['./lib'] + sys.path

data_folder = 'data/%s'
slog_folder	= data_folder % 'log/%s'
tmp_folder	= 'tmp/%s'

updatelog_file	= slog_folder % 'update.log'
ver_file		= tmp_folder % 'version'
old_ver_file	= tmp_folder % 'ver'
pid_file		= tmp_folder % 'isida.pid'
starttime_file	= tmp_folder % 'starttime'

id_append = ''
svn_ver_format	= '%s-svn%s'
git_ver_format	= '%s.%s-git%s'
time_ver_format	= '%s-none%s'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def printlog(text):
	print text
	lt = tuple(time.localtime())
	fname = slog_folder % 'crash_%04d%02d%02d.txt' % lt[0:3]
	fbody = '%s|%s\n' % ('%02d%02d%02d' % lt[3:6],text)
	fl = open(fname, 'a')
	fl.write(fbody.encode('utf-8'))
	fl.close()

def crashtext(t):
	t = '*** %s ***' % t
	s = '*'*len(t)
	return '\n%s\n%s\n%s\n' % (s,t,s)

def crash(text):
	printlog(crashtext(text))
	sys.exit()

def update(USED_REPO):
	if USED_REPO == 'svn':
		if os.name == 'nt':
			os.system('svnversion > %s' % old_ver_file)
			os.system('svn up')
			os.system('svnversion > %s' % ver_file)
		else:
			os.system('echo `svnversion` > %s' % old_ver_file)
			os.system('svn up')
			os.system('echo `svnversion` > %s' % ver_file)
		try: ver = int(re.findall('[0-9]+',readfile(ver_file))[0]) - int(re.findall('[0-9]+',readfile(old_ver_file))[0])
		except: ver = -1
		if ver > 0: os.system('svn log --limit %s > %s' % (ver,updatelog_file))
		elif ver < 0: os.system('echo Failed to detect version! > %s' % updatelog_file)
		else: os.system('echo No Updates! > %s' % updatelog_file)
		writefile(ver_file, unicode(svn_ver_format % (str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ',''),id_append)).encode('utf-8'))
	elif USED_REPO == 'git':
		os.system('git pull -u origin master')
		os.system('git describe --always > %s' % ver_file)
		revno = str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		os.system('git log --pretty=format:'' > %s' % ver_file)
		writefile(ver_file, unicode(git_ver_format % (os.path.getsize(ver_file)+1,revno,id_append)).encode('utf-8'))
		os.system('git log -1 > %s' % updatelog_file)
		writefile(updatelog_file, unicode(readfile(updatelog_file)).replace('\n\n','\n').replace('\r','').replace('\t',''))
	else: os.system('echo Update not available! Read wiki at http://isida-bot.com to use SVN/GIT! > %s' % updatelog_file)

if __name__ == "__main__":
	if os.name == 'nt': printlog('Warning! Correct work only on *NIX system!')

	try: writefile(starttime_file,str(int(time.time())))
	except:
		printlog(crashtext('Isida is crashed! Incorrent launch!'))
		raise

	if os.path.isfile(pid_file) and os.name != 'nt':
		try: last_pid = int(readfile(pid_file))
		except: crash('Unable get information from %s' % pid_file)
		try:
			os.getsid(last_pid)
			crash('Multilaunch detected! Kill pid %s before launch bot again!' % last_pid)
		except Exception, SM:
			if not str(SM).lower().count('no such process'): crash('Unknown exception!\n%s' % SM)

	writefile(pid_file,str(os.getpid()))

	dirs = os.listdir('.')+os.listdir('../')

	if '.svn' in dirs:
		USED_REPO = 'svn'
		if os.name == 'nt': os.system('svnversion > %s' % ver_file)
		else: os.system('echo `svnversion` > %s' % ver_file)
		os.system('echo Just Started! > %s' % updatelog_file)
		bvers = str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		writefile(ver_file, unicode(svn_ver_format % (bvers,id_append)).encode('utf-8'))
	elif '.git' in dirs:
		USED_REPO = 'git'
		os.system('git describe --always > %s' % ver_file)
		revno = str(readfile(ver_file)).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
		os.system('git log --pretty=format:'' > %s' % ver_file)
		writefile(ver_file, unicode(git_ver_format % (os.path.getsize(ver_file)+1,revno,id_append)).encode('utf-8'))
	else:
		USED_REPO = 'unknown'
		writefile(ver_file, unicode(time_ver_format % (hex(int(os.path.getctime('../')))[2:],id_append)).encode('utf-8'))

	while 1:
		try: execfile('kernel.py')
		except KeyboardInterrupt: break
		except SystemExit, mode:
			for t in threading.enumerate():
				try:
					if str(t).startswith('<KThread'): t.kill()
					elif str(t).startswith('<_Timer'): t.cancel()
				except: pass
			mode = str(mode)
			if mode == 'update': update(USED_REPO)
			elif mode == 'exit': break
			elif mode == 'restart': pass
			else:
				printlog('unknown exit type!')
				break
		except Exception, SM:
			try: SM = str(SM)
			except: SM = unicode(SM)
			printlog(crashtext('Isida is crashed! It\'s imposible, but You do it!'))
			printlog('%s\n' % SM)
			traceback.print_exc()
			break
	os._exit(0)

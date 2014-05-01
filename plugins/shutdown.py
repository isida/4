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

def bot_shutdown(type, jid, nick, text, reason, xtype):
	global game_over,bot_exit_type
	StatusMessage = L('%s by command from %s','%s/%s'%(jid,nick)) % (reason, nick)
	if text != '': StatusMessage += ', ' + L('reason: %s','%s/%s'%(jid,nick)) % text
	send_presence_all(StatusMessage)
	bot_exit_type, game_over = xtype, True

def bot_exit(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Shutdown','%s/%s'%(jid,nick)), 'exit')

def bot_restart(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Restart','%s/%s'%(jid,nick)), 'restart')

def bot_update(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Update','%s/%s'%(jid,nick)), 'update')

def bot_soft_update(type, jid, nick, text):
	global plugins_reload
	caps_and_send(xmpp.Presence(show='dnd', status=L('Soft update activated!','%s/%s'%(jid,nick)), priority=Settings['priority']))
	plugins_reload = True
	while not game_over and plugins_reload: time.sleep(1)
	if GT('soft_update_resend_hash'):
		pprint('*** Send new hash in to rooms','bright_green')
		cnf = cur_execute_fetchall('select * from conference;')
		for tocon in cnf:
			if tocon[1]: pprint('->- %s | pass: %s' % tocon,'green')
			else: pprint('->- %s' % tocon[0],'green')
			zz = join(tocon)
	if Settings['status'] == 'online': caps_and_send(xmpp.Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(xmpp.Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))
	send_msg(type, jid, nick, L('Soft update finished! Plugins loaded: %s. Commands: %s','%s/%s'%(jid,nick)) % (len(plugins)+1,len(comms)))

global execute

execute = [(9, 'quit', bot_exit, 2, 'Shutting down the bot. You can set reason.'),
	 (9, 'restart', bot_restart, 2, 'Restart the bot. You can set reason.'),
	 (9, 'update', bot_update, 2, 'Update from VCS. You can set reason.'),
	 (9, 'soft_update', bot_soft_update, 2, 'Soft update from VCS.')]

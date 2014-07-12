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

# ----------------------------------------------------------------------
# фукнция вызывается при подаче команду боту
def empty_command(type, jid, nick, text): return
# type - тип chat или groupchat
# jid - конференция или jid из которой пришла команда
# nick - ник пославшего команду
# text - параметры команды

# ----------------------------------------------------------------------
# функция вызывается раз в секунду.
def empty_timer(): return
# параметров нет.

# ----------------------------------------------------------------------
# функция вызывается при входящем презенсе
def empty_presence(room,jid,nick,type,arr): return
# room ... конференция из которой пришел презенс или jid
# jid .... jid пославшего презенс
# nick ... nick пославшего презенс
# type ... тип презенса

# arr .... массив дополнительных пареметров:
# (text, role, affiliation, exit_type, exit_message, show, priority, not_found)

# text - статусное сообщение
# role - роль
# affiliation - аффиляция
# exit_type - тип выхода "вышел" | "выгнали" | "забанили"
# exit_message - статусное сообщение при выходе или ризон при кике/бане
# show - статус online|chat|away|xa|dnd
# priority - приоритет
# not_found - тип презенса:
#		0 - вход
#		1 - смена роли\аффиляции
#		2 - смена статуса

# ----------------------------------------------------------------------
# функция вызывается при входящих сообщениях
# при пассивной обработке сообщений без ответа в конференцию
def empty_message(room,jid,nick,type,text): return
# room ... конференция из которой пришло сообщение
# jid .... jid пославшего сообщение
# nick ... ник пославшего сообщение
# type ... тип сообщения
# text ... текст сообщения

# ----------------------------------------------------------------------
# функция вызывается при входящих сообщениях,
# при активной обработке сообщений с ответом в конференцию
# в зависмости от возвращаемого результата (False|True) срабатывает или не срабатывает флуд
def empty_act_message(room,jid,nick,type,text): return True
# room ... конференция из которой пришло сообщение
# jid .... jid пославшего сообщение
# nick ... ник пославшего сообщение
# type ... тип сообщения
# text ... текст сообщения

# ----------------------------------------------------------------------

global execute, timer, presence_control, message_control, message_act_control

# если данные фичи не нужны - удалить ниже и из global
timer = [empty_timer] # список функций, которые вызываются раз в секунду
presence_control = [empty_presence] # реакция на презенс
message_control = [empty_message] # пассивная реакция на сообщение
message_act_control = [empty_act_message] # активная реакция на сообщение

# описание команд
execute = [(0, 'empty', empty_command, 1, 'command decription')]
# 1. уровень доступа:
#		0 - без ограничений
#		1 - не ниже visitor|none
#		2 - не ниже visitor|member
#		3 - не ниже participant|none
#		4 - не ниже participant|member
#		5 - не ниже moderator|none
#		6 - не ниже moderator|member
#		7 - не ниже moderator|admin
#		8 - не ниже moderator|owner
#		9 - владелeц бота
# 2. название команды на которую бот будет реагировать
# 3. название функции, которая вызывается командой
# 4. тип передачи параметров:
#		0 - передавать справку и все параметры после неё в виде массива
#		1 - не передавать параметров
#		2 - передавать остаток текста после команды
# 5. описание команды, которое покажет бот по help <название_команды>
# при этом в файл локали надо поместить текст вида 'command decription<tab>описание команды'

# полезные функции:
# send_msg(type,jid,nick,msg) - отправка сообщения
# readfile(filename) - чтение файла
# writefile(filename,data) - запись файла
# getFile(filename,default) - чтение файла. если файла нет - создание с содержимым default
# get_tag(body,tag) - взять tag из body
# join(conference) - войти в конференцию. возвращает None или ошибку
# leave(conference,sm) - покинуть конференцию со статусным сообщением sm
# getName(jid) - взять NAME@server.tld/resource
# getServer(jid) - взять name@SERVER.TLD/resource
# getResourse(jid) - взять name@server.tld/RESOURCE
# getRoom(jid) - взять NAME@SERVER.TLD/resource
# shell_execute(cmd) - выполнить shell команду
# get_affiliation(room,nick) - возвращает аффиляцию
# get_level(room,nick) - возвращает (уровень_доступа, jid)
# html_encode(body) - определение кодировки и декодирование body в unicode

# -*- coding: utf-8 -*-

#-------------------------------------------------------#
#				 Isida-bot Config file
#						v4.0ru
#-------------------------------------------------------#


#-------------------------------------------------------#
#--------------- Настройки подключения -----------------#
Settings = {
'nickname': 		u'<пишем сюда ник бота>',					# Ник бота в конференциях
'jid':				u'isida-jabber-bot@server.tld/isida-bot',	# Jid бота с ресурсом
'password':			u'********',								# Пароль
'status':			u'online',									# Статус бота chat|online|away|xa|dnd
'priority':			0,											# Приоритет
'message':			u'Йа аццкое железко!'}						# Статус-сообщение


#-------------------------------------------------------#
#---------------- Стартовые настройки ------------------#
SuperAdmin		=	u'username@server.tld'					# JID владельца бота
defaultConf		=	u'room@conference.server.tld'			# Стартовая конференция
prefix			=	u'_'									# Префикс команд по умолчанию
msg_limit		=	2048									# Лимит размера сообщений


#-------------------------------------------------------#
#---------------- Настройка прокси/хостов --------------#
#proxy = {'host':'localhost','port':3128,'user':'me','password':'secret'}	# Прокси
#proxy = {'host':'127.0.0.1','port':3128,'user':'','password':''}
#proxy = {'host':'localhost','port':3128}
#server = 'allports.jabber.ru:443'								# Подключение минуя ресольвер
#secure = True													# Включение ssl (порт 5223)
#http_proxy = {'host':'localhost','port':3128,'user':'me','password':'secret'}	# Http-прокси
#http_proxy = {'host':'127.0.0.1','port':3128,'user':None,'password':None}


#-------------------------------------------------------#
#-------------- Отладка, системные логи ----------------#
#ignore_owner = True										# не исполнять для владельца бота отключенные команды
#halt_on_exception = True									# останавливать работу бота при исключениях
#debug_xmpppy = True										# режим отладки xmpppy
#debug_console = True										# режим показа действий бота в консоле
#database_debug = True										# режим отладки PostgreSQL
CommandsLog = True											# логгирование команд бота
#thread_type = None											# тип тредов thread/threading. по умолчанию - threading
#ENABLE_TLS = False											# принудительное отключение TLS при сбоях на больших станзах на старых версиях OpenSSL
#ENABLE_SASL = False										# отключение SASL



#-------------------------------------------------------#
#----------------- Настройка баз данных ----------------#
#---------------------- PostgreSQL ---------------------#
base_type = 'pgsql'			# тип базы: pgsql
base_name = 'isidabot'		# название базы для PostgreSQL
base_user = 'isidabot'		# пользователь базы для PostgreSQL
base_host = 'localhost'		# хост базы для PostgreSQL
base_pass = '******'		# пароль базы для PostgreSQL
base_port = '5432'			# порт для подключения. стандартный - 5432

#----------------------- SQLite3 -----------------------#
#base_type = 'sqlite3'		# тип базы: sqlite3

#------------------------ MySQL ------------------------#
#base_type = 'mysql'		# тип базы: mysql
#base_name = 'isidabot'		# название базы для MySQL
#base_user = 'isidabot'		# пользователь базы для MySQL
#base_host = 'localhost'	# хост базы для MySQL
#base_pass = '******'		# пароль базы для MySQL
#base_port = 3306			# порт для подключения. стандартный - 3306


#-------------------------------------------------------#
#------------------ Файлы, пути к файлам ---------------#
tmp_folder = 'tmp/%s'							# папка временных данных
data_folder = 'data/%s'							# папка данных
set_folder 	= 'settings/%s'						# папка настроек
sqlite_base = data_folder % 'sqlite3.db'		# файл с базой sqlite3
slog_folder = data_folder % 'log/%s'			# папка системных логов
back_folder = data_folder % 'backup/%s'			# папка хранения резервных копий
loc_folder 	= data_folder % 'locales/%s.txt'	# папка локализаций
log_folder 	= data_folder % 'conflogs/%s'		# папка логов конференций
LOG_FILENAME = slog_folder % 'error.txt'		# логи ошибок
ver_file = tmp_folder % 'version'				# версия бота
cens = data_folder % 'censor.txt'				# цензор
custom_cens = data_folder % 'custom_censor.txt'	# цензор пользователя
public_log = log_folder % 'chatlogs/%s'			# папка публичных логов конференций
system_log = log_folder % 'syslogs/%s'			# папка системных логов конференций
logs_css_path = '../../../.css/isida.css'		# путь к css файлу для логов
tld_list = data_folder % 'tldlist.txt'			# список tld кодов
poke_file = data_folder % 'poke.txt'			# список ответов для команды poke
answers_file = tmp_folder % 'answers.txt'		# имя файла по умолчанию для импорта/экспорта ответов
date_file = data_folder % 'date.txt'			# список праздников
pastepath = data_folder % 'paste/'				# путь для больших сообщений
pasteurl  = 'http://fill_it_before_use/paste/'	# url для сообщений. необходимо вписать *СВОЙ* сайт!
paste_css_path = '.css/isida.css'				# путь к css
default_msg_limit = msg_limit					# размер сообщений по умолчанию
smile_folder = '.smiles'						# папка со смайлами в чатлогах
smile_descriptor = 'icondef.xml'				# дескриптор смайлов
back_file = back_folder % '%s.back'				# шаблон копий файлов
starttime_file = tmp_folder % 'starttime'

#-------------------------------------------------------#
# Регекспы для блокиратора рекламы, регистронезависимые #
adblock_regexp = [u'([-0-9a-zа-я_+]+@c[-0-9a-z-.]+)',
				  u'https?://(.*?icq.*?/[-a-z0-9?+./=?&]*?)']

#-------------------------------------------------------#
#------------- Дополнительные настройки ----------------#
#default_censor_set = 2				# номер набора правил для цензора. 1 - слово целиком, 2 - кроме первой буквы

#-------------------------------------------------------#

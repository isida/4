#!/usr/bin/python

about_txt = '''
# --------------------------------------------------------------------------- #
#                                                                             #
#    GUI for Locale Generator                                                 #
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
'''

import sys
import os
import locale_generator
from PyQt4 import QtGui, QtCore, Qt

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.setWindowIcon(Qt.QIcon("icons/isida.png"))
		if self.regenerate():
			self.resize(400, 150)
			self.setWindowTitle('GUI for Locale Generator')

			self.window = Qt.QWidget()

			self.layout_main = Qt.QGridLayout()
			self.layout_main.setContentsMargins(3, 3, 3, 3)
			self.layout_main.setSpacing(3)
			self.window.setLayout(self.layout_main)

			self.textLabelEN = QtGui.QLabel('<center><b>EN<\b><\center>')
			self.textEditEN = Qt.QTextEdit()
			self.textEditEN.setReadOnly(1)
			self.textEditEN.setPlainText(self.loc_dict.values()[0][self.nontrans[0]].split('\t')[0].replace('\\n', '\n').replace('\\t', '\t'))
			self.layout_main.addWidget(self.textLabelEN, 0, 0)
			self.layout_main.addWidget(self.textEditEN, 0, 1)
			
			self.textLabel = {}
			self.textEdit = {}
			
			for n, k in enumerate(self.loc_dict.keys()):
				self.textLabel[k] = QtGui.QLabel('<center><b>%s<\b><\center>' % k.upper())
				self.textEdit[k] = Qt.QTextEdit()
				self.textEdit[k].setPlainText(self.loc_dict[k][self.nontrans[0]].split('\t')[1].replace('\\n', '\n').replace('\\t', '\t'))
				self.layout_main.addWidget(self.textLabel[k], n + 1, 0)
				self.layout_main.addWidget(self.textEdit[k], n + 1, 1)

			self.setCentralWidget(self.window)

			exit_act = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
			exit_act.setShortcut('Ctrl+Q')
			exit_act.setStatusTip('Exit application')
			self.connect(exit_act, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

			info_act = QtGui.QAction(QtGui.QIcon('icons/dialog-information.png'), 'Info', self)
			info_act.setShortcut('Ctrl+I')
			info_act.setStatusTip('Informations about locales')
			self.connect(info_act, QtCore.SIGNAL('triggered()'), self.show_locales_info)

			prev_act = QtGui.QAction(QtGui.QIcon('icons/go-previous.png'), 'Previous', self)
			prev_act.setShortcut('Ctrl+P')
			prev_act.setStatusTip('Previous non-translate')
			self.connect(prev_act, QtCore.SIGNAL('triggered()'), self.prev_notrans)

			save_act = QtGui.QAction(QtGui.QIcon('icons/document-save.png'), 'Save', self)
			save_act.setShortcut('Ctrl+S')
			save_act.setStatusTip('Save locales')
			self.connect(save_act, QtCore.SIGNAL('triggered()'), self.save_locales)

			save_l = {}
			for k in self.loc_dict.keys():
				save_l[k] = QtGui.QAction(QtGui.QIcon('icons/document-save.png'), 'Save %s' % k.upper(), self)
				save_l[k].setStatusTip('Save locale: %s' % k.upper())
				self.connect(save_l[k], QtCore.SIGNAL('triggered()'), lambda: self.save_locales(k))

			next_act = QtGui.QAction(QtGui.QIcon('icons/go-next.png'), 'Next', self)
			next_act.setShortcut('Ctrl+N')
			next_act.setStatusTip('Next non-translate')
			self.connect(next_act, QtCore.SIGNAL('triggered()'), self.next_notrans)

			about_act = QtGui.QAction(QtGui.QIcon('icons/help-browser.png'), 'About...', self)
			about_act.setStatusTip('About...')
			self.connect(about_act, QtCore.SIGNAL('triggered()'), self.about_info)

			self.connect(self, Qt.SIGNAL('triggered()'), self.closeEvent)

			self.statusBar()

			menubar = self.menuBar()

			menu_f = menubar.addMenu('&Menu')
			menu_f.addAction(save_act)
			for k in self.loc_dict.keys():
				menu_f.addAction(save_l[k])
			menu_f.addAction(info_act)
			menu_f.addAction(exit_act)

			menu_e = menubar.addMenu('&Edit')
			menu_e.addAction(prev_act)
			menu_e.addAction(next_act)

			menu_i = menubar.addMenu('&Info')
			menu_i.addAction(about_act)

			toolbar_f = self.addToolBar('File')
			toolbar_f.addAction(exit_act)
			toolbar_f.addAction(save_act)
			toolbar_f.addAction(info_act)

			toolbar_e = self.addToolBar('Edit')
			toolbar_e.addAction(prev_act)
			toolbar_e.addAction(next_act)
		else:
			self.save_locales(None,None)
			self.setWindowTitle('Info')
			self.window = Qt.QWidget()
			self.layout_main = Qt.QVBoxLayout()
			self.layout_main.setContentsMargins(3, 3, 3, 3)
			self.layout_main.setSpacing(3)
			self.window.setLayout(self.layout_main)
			
			lbl = QtGui.QLabel('<center>Regenerated without mistakes!<\center>')
			self.layout_main.addWidget(lbl)
			quit_act = QtGui.QPushButton('Quit')
			self.layout_main.addWidget(quit_act)
			self.connect(quit_act, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
			self.setCentralWidget(self.window)

	def regenerate(self):
		path_to_locale = locale_generator.path_to_locale
		lf = os.listdir(path_to_locale)
		self.loc_dict = {}
		self.label_inf = ''
		for tmp in lf:
			if tmp[-4:] == '.txt':
				msg, result, lz = locale_generator.regenerate(path_to_locale,tmp)
				self.label_inf += '%s\n' % msg.replace('write', 'Found')
				self.loc_dict[tmp[:-4]] = result.split('\n')
		self.label_inf += 'Total found definitions: %s\n' % lz

		self.nontrans = []

		#self.show_locales_info()

		for k in self.loc_dict.keys():
			self.nontrans += [i[0] for i in enumerate(self.loc_dict[k]) if locale_generator.locale_mark in i[1] and i[1][0] != '#']

		self.nontrans = list(set(self.nontrans))
		self.nontrans.sort()
		self.curs = 0
		self.count = len(self.nontrans)
		self.save = True

		if not self.count:
			return False
		else:
			return True

	def closeEvent(self, event):
		if self.count:
			tmp_en = self.textEditEN.toPlainText().replace('\n', '\\n').replace('\t', '\\t')
			for k in self.loc_dict.keys():
				if self.loc_dict[k][self.nontrans[self.curs]] != '%s\t%s' % (tmp_en, self.textEdit[k].toPlainText().replace('\n', '\\n').replace('\t', '\\t')):
					self.save = False
			if not self.save:
				reply = QtGui.QMessageBox.question(self, 'Quit', "Are you sure to quit without saving?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
				if reply == QtGui.QMessageBox.No:
					event.ignore()
					return
		event.accept()

	def show_locales_info(self):
		self.show_info(self.label_inf)

	def show_info(self, txt):
		QtGui.QMessageBox.information(self, 'Info', txt, QtGui.QMessageBox.Ok)

	def next_notrans(self):
		tmp_en = self.textEditEN.toPlainText().replace('\n', '\\n').replace('\t', '\\t')
		for k in self.loc_dict.keys():
			tmp_k = '%s\t%s' % (tmp_en, self.textEdit[k].toPlainText().replace('\n', '\\n').replace('\t', '\\t'))
			if self.loc_dict[k][self.nontrans[self.curs]] != tmp_k:
				self.save = False
				self.loc_dict[k][self.nontrans[self.curs]] = tmp_k
		self.curs = (self.curs + 1) % self.count
		self.textEditEN.setText(self.loc_dict.values()[0][self.nontrans[self.curs]].split('\t')[0].replace('\\n', '\n').replace('\\t', '\t'))
		for k in self.loc_dict.keys():
			self.textEdit[k].setText(self.loc_dict[k][self.nontrans[self.curs]].split('\t')[1].replace('\\n', '\n').replace('\\t', '\t'))

	def prev_notrans(self):
		tmp_en = self.textEditEN.toPlainText().replace('\n', '\\n').replace('\t', '\\t')
		for k in self.loc_dict.keys():
			tmp_k = '%s\t%s' % (tmp_en, self.textEdit[k].toPlainText().replace('\n', '\\n').replace('\t', '\\t'))
			if self.loc_dict[k][self.nontrans[self.curs]] != tmp_k:
				self.save = False
				self.loc_dict[k][self.nontrans[self.curs]] = tmp_k
		self.curs = (self.curs - 1) % self.count
		self.textEditEN.setText(self.loc_dict.values()[0][self.nontrans[self.curs]].split('\t')[0].replace('\\n', '\n').replace('\\t', '\t'))
		for k in self.loc_dict.keys():
			self.textEdit[k].setText(self.loc_dict[k][self.nontrans[self.curs]].split('\t')[1].replace('\\n', '\n').replace('\\t', '\t'))

	def save_locales(self, locale_for_saving=None, main_interface=True):
		if main_interface: tmp_en = self.textEditEN.toPlainText().replace('\n', '\\n').replace('\t', '\\t')
		if not locale_for_saving:
			ls = self.loc_dict.keys()
		else:
			ls = [locale_for_saving]
		for k in ls:
			if main_interface: self.loc_dict[k][self.nontrans[self.curs]] = '%s\t%s' % (tmp_en, self.textEdit[k].toPlainText().replace('\n', '\\n').replace('\t', '\\t'))
			result = '\n'.join(self.loc_dict[k])
			if not result.endswith('\n\n'): result = '%s\n' % result
			locale_generator.writefile('%s.txt' % k,result.encode('utf-8'))
			tmp_body = []
			for t in result.split('\n\n',1)[1].split('\n'):
				if locale_generator.locale_mark not in t: tmp_body.append(t)
			tmp2_body,cnt = [],0
			for t in range(0,len(tmp_body)-2):
				if tmp_body[cnt].startswith(locale_generator.file_mark) and tmp_body[cnt+2].startswith(locale_generator.file_mark): cnt += 2
				tmp2_body.append(tmp_body[cnt])
				cnt += 1
			original_file = '%s\n\n%s' % (locale_generator.readfile('%s/%s.txt' % (locale_generator.path_to_locale,k)).decode('UTF').replace('\r','').split('\n\n',1)[0],'\n'.join(tmp2_body))
			if not original_file.endswith('\n\n'): original_file = '%s\n' % original_file
			locale_generator.writefile('%s/%s.txt' % (locale_generator.path_to_locale,k),original_file.encode('utf-8'))
		if main_interface:
			if not self.regenerate():
				self.show_info('Regenerated without mistakes!')
				self.close()
			else:
				for n, k in enumerate(self.loc_dict.keys()):
					self.textEditEN.setPlainText(self.loc_dict.values()[0][self.nontrans[0]].split('\t')[0].replace('\\n', '\n').replace('\\t', '\t'))
					self.textEdit[k].setPlainText(self.loc_dict[k][self.nontrans[0]].split('\t')[1].replace('\\n', '\n').replace('\\t', '\t'))
				self.show_info('Done!')

	def about_info(self):
		self.show_info(about_txt.replace('#', '').replace('-', ''))

if __name__ == "__main__" :
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
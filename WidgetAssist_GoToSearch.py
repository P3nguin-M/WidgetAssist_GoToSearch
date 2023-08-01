

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
import os, time, subprocess, sys, traceback
from widget_gui import Ui_WidgetAssist
from user_alert import Ui_AlertWindow

import widget_module as mod

icon_file=os.path.join('Dependencies', 'wInstaller.ico')

thread=mod.threading()
log = mod.logging()
init = mod.init_process()
file = mod.filework()

class ThreadClass1(QtCore.QThread):
	disable_sig = QtCore.pyqtSignal()
	enable_sig = QtCore.pyqtSignal()

	def __init__(self, parent = None):
		super(ThreadClass1, self).__init__(parent)
		
	def run(self):
		self._stopped = False
		connection_class = mod.connections()
		status = mod.status_class()
		thread = mod.threading()
		
		global already_processed 

		already_processed = []
		
		while self._stopped == False:
			all_connected = connection_class.find_samsung_modem()

			if len(all_connected) == 0:
				## check to see if device is in queue list
				if len(connection_class.check_queued()) == 0:
					## no devices in current process and clear GUI
					status.set_status('', '')
					already_processed=[]
				else:
					pass

			elif len(all_connected) > 1:
				status.set_status('ERROR', f'Too many devices found connected: {len(all_connected)}')

			elif len(all_connected) == 1:
				if all_connected[0] in already_processed:
					pass
				else:
					self.disable_sig.emit()
					## add to list to not re-run more than once
					already_processed.append(all_connected[0])
					## wait for possible devices that disconnect on first connect
					## causing issues forcing technician to restart process (replug)
					time.sleep(1.5)
					init.step_one(all_connected[0])

			time.sleep(1)
			self.enable_sig.emit()


	def stop(self):
		self._stopped = True


class ThreadClass2(QtCore.QThread):

	update_info_sig = QtCore.pyqtSignal(str, str)
	def __init__(self, parent = None):
		super(ThreadClass2, self).__init__(parent)
		
	def run(self):
		self._stopped = False

		status=mod.status_class()		
		past_status = ''
		self.update_info_sig.emit('', '')

		while self._stopped == False:
			try:

				## [portnum, status]
				curr_status = status.read_status()
					
				if curr_status[1] != past_status:
					self.update_info_sig.emit(curr_status[1], curr_status[0])
					past_status=curr_status[1]

				time.sleep(.25)
			except Exception as e:
				log.log_errors(f'ThreadClass2: {e}{traceback.format_exc()}')
				time.sleep(1)


	def stop(self):
		self._stopped = True



class MainWindow(QMainWindow, Ui_WidgetAssist):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		
		self.main_win = QMainWindow()
		self.ui_widgetapp = Ui_WidgetAssist()
		self.ui_widgetapp.setupUi(self.main_win)
		self.main_win.setWindowTitle('WidgetAssist: [GoToSearch] (v2.2)')

		self.alert_win = QMainWindow()
		self.alert_ui = Ui_AlertWindow()
		self.alert_win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.alert_ui.setupUi(self.alert_win)

		self.dev_processing = ThreadClass1(self)
		self.dev_processing.disable_sig.connect(self.disable_buttons)
		self.dev_processing.enable_sig.connect(self.enable_buttons)
		self.dev_processing.start()

		self.dev_gui_update = ThreadClass2(self)
		self.dev_gui_update.update_info_sig.connect(self.update_device_info)
		self.dev_gui_update.start()
		
		self.ui_widgetapp.reboot.triggered.connect(lambda: thread.create_thread(f'processing().reboot_device()'))
		self.ui_widgetapp.shutdown.triggered.connect(lambda: thread.create_thread(f'processing().poweroff_device()'))
		self.ui_widgetapp.retry_proc.triggered.connect(lambda: thread.create_thread(f'processing().reset_device()'))
		
		self.alert_ui.browse_apk.clicked.connect(self.load_apk)


	def update_device_info(self, msg_info, port_num):
		try:
			if msg_info == '' and port_num == '':
				self.ui_widgetapp.PORT_WIN.setText('')
				self.ui_widgetapp.TEXT_WIN.setText('')
			else:
				port_text = f'Detected {port_num}'
				self.ui_widgetapp.PORT_WIN.setText(port_text)
				self.ui_widgetapp.TEXT_WIN.append("".join(msg_info))
				self.ui_widgetapp.TEXT_WIN.verticalScrollBar().setValue(self.ui_widgetapp.TEXT_WIN.verticalScrollBar().maximum())
		except Exception as error:
			log.log_errors(f'GUI_Update: ')

	def enable_buttons(self):
		try:
			self.ui_widgetapp.reboot.setDisabled(False)
			self.ui_widgetapp.shutdown.setDisabled(False)
			self.ui_widgetapp.retry_proc.setDisabled(False)

		except Exception as e:
			log.log_errors(f'enable_btns: {e}')


	def disable_buttons(self):
		try:
			self.ui_widgetapp.reboot.setDisabled(True)
			self.ui_widgetapp.shutdown.setDisabled(True)
			self.ui_widgetapp.retry_proc.setDisabled(True)

		except Exception as e:
			log.log_errors(f'disable_btns: {e}')

	def load_apk(self):
		imported_apk_file = QFileDialog.getOpenFileName(self, 'Select .apk file given for processing', 'c:\\',"APK File (*.apk)")
		try:
			if imported_apk_file:
				imported_apk_file_path=imported_apk_file[0]
				if file.import_apk_file(imported_apk_file_path) == 1:
					log.log_normal(f'Imported install.apk for first time use')
					main_win.show()
					self.hide_alert()

				else:
					log.log_errors(f'Error while loading install.apk\n{traceback.format_exc()}')
		except Exception as e:
			log.log_errors(f'Import_APK: {e}\n{traceback.format_exc()}')


	def show_alert(self):
		self.alert_win.show()

	def hide_alert(self):
		self.alert_win.hide()

	def hide(self):
		self.main_win.hide()


	def show(self):
		self.main_win.show()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon(icon_file))
	try:
		## make sure if demo apk is 
		## only installed to alert user
		## on every runtime instance
		if file.check_apk_md5() == 0:
			main_win = MainWindow()
			main_win.show()
			main_win.activateWindow()
			sys.exit(app.exec_())
		else:
			main_win = MainWindow()
			main_win.show()
			main_win.activateWindow()
			## show alert window too
			main_win.show_alert()
			sys.exit(app.exec_())

	except Exception as e:
		log.log_errors(f'Main: {e}\n{traceback.format_exc()}')

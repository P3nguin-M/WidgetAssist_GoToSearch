## WidgetAssist Guide & Troubleshooting ##

This tool has been designed to help automate marketing processes
onto newer Samsung devices running Android 9.0-13.0. With the ability
to enable functionality of Samsung devices as well as modify their stock state 
without showing signs of tampering.



Install Prerequites:
* Samsung-USB-Driver supplied (stable current version 1.7.46.0)
* adb driver supplied
* Remove or halt any conflicting apps that process androids using any tools (Read below on Troubleshooting)
* Installation of WidgetAssist_Installer.exe



Instructions:

1) Start by running WidgetAssist as Administrator. 

2) Connect a device that is full bootup and on setup. Optionally for older devices Android 10 and below, enter Test menu (*#0*#) beforehand. 

3) Wait for Widget Assist process completion message: "Process Complete. Please power off." You may power off manually or by using Menu -> Shutdown



Troubleshooting (Issue / Solution):

I: I plugin device and nothing happens!
S: Use a utility or device manager to view device is showing up and 
Samsung modem is showing with a COM. Usually this is due to a bad USB or 
could also be the drivers are not properly installed.

I: ADB Auth Dialog is a no show!
S: Please make sure any utilities that work with android devices have been
removed or stopped before using this app. Some apps will conflict and cause adb
issues. If the device has no test menu this process will not work, this is usually
seen in very low end Samsung devices missing normal DeviceTest menu.

I: Program has suddenly crashed during / before or after process completion.
S: There may be times that the application will come to a halt due to faulty USB connection, misc bugs.
If this is an issue backup: C:\Program Files(x86)\WidgetAssist\Dependencies\logs\error_log.txt
and reach out to a team member for more help or reporting bugs. This file can be attached in the report for helping the engineers. 

I: Program has went through entire process but Widget did not install!
S: There are a few instances where the widget may not properly install. This is being actively 
developed and updated upon errors. Please report any failures with logs to a team member for 
active error reporting including Model \ OS of problem device(s).

I: App Status: 'Test menu is not opened.. Please retry'
S: That device is not supported to automate opening of the test menu if that message is received. Please manually enter the test menu and replug when you see this message. 

I: App has been stuck on same message and nothing is happening?!
S: There's a few different circumstances that can cause these types of issues. If
this continues happening persistently on the same model please report with logs to team member.
Usually bad usb connections and or interfering applications can cause this. Please close all, make sure the connection is stable and restart process.

I: Widget did not align properly!?
S: This is still being currently perfected. Please report log to team member for research 
and development.
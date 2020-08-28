A very simple Linux GUI tool to monitor or change a ProtonVPN connection.

Requirements:

1. Linux (any, tested on openSUSE Tumbleweed)
2. Python (tested on v3.7)
3. ProtonVPN cli tool (https://protonvpn.com/support/linux-vpn-tool/)
4. tkinter - If you get :File "pvpnmon.py", line 1, in <module>
			    import tkinter as tk
				ModuleNotFoundError: No module named 'tkinter'
		run: sudo apt install python3-tk (or similar for your distro)

Download, and setup ProtonVPN-cli, as per above link. 

Download 	1.	pvpnmon.py
					2.	check.sh
					3.	kill.sh
					4.	iprestore.sh
					5.	ipsave.sh
	and make sure they are in the same folder. 
	**Optionally**, download logo.gif and place in same folder, for a background logo.

Run pvpnmon from terminal with 'python3 pvpnmon.py &'  -  **in the directory where you downloaded pvpnmon.py to**.

**Alternatively**, run 'python3 pvpnmon.py -top &' to keep the monitor window above other windows.

Terminal may ask for your SU password, as internally it runs 'sudo protonvpn status', and other commands.  It may take a few seconds for the GUI to launch, as it will query the ProtonVPN servers..

CTRL-C after running, to release terminal window.

Leave terminal window open, to keep the GUI running. Closing terminal will close the GUI. **see changelog.txt for notes on closing GUI with kill-switch activated**

Pvpnmon is in Beta status.

**This GUI is a 3rd party program, and in no way supported or endorsed by ProtonVPN.
Any issues, bugs, or complaints should be directed to this GitHub repository, not to ProtonVPN.**


import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import sys

global homedir
homedir = os.environ['HOME'] 
update = 0
global status
status = ""
global counter
counter = 0

def counter_label(label):

  def getstatus():
    global status
    global isPing
    global ping
    global isKillActive
	
    if isKillActive:
        return
    status = os.popen('sudo protonvpn status').read()
    if isPing.get():
        ping = os.popen('ping -c 1 -w 2 google.com').read()
    if 'time='in ping:
        x = ping.find('time=')
        x2 = ping.find(' ms')
        #TODO : below is legacy from v1, clean it
        ms = ping[x+5:x2]
        l = len(status)
        trimstat = status[0:l-1]
        status = trimstat + '\nGoogle Ping : '+ms+'ms'
    return


  def update(isReal):
    global update
    global status
    global isPing
    global txtWorking
    global isKillActive

    L1 = txtWorking[0 : 1] 
    L2 = txtWorking[1 :] 
    txtWorking = L2+L1
    upTxt = '('+ txtWorking + ')\n'

    if isReal:	
        getstatus()
    if not isMini.get():
        lblPstatus = 'Proton VPN Monitor\n'
    else:
        lblPstatus = ''
    lblPstatus = lblPstatus + upTxt + status
    lblPstatus = lblPstatus.replace(' ', '')
    lblPstatus = lblPstatus.replace(':', ': ')

    quickcheck= os.popen('sudo sh check.sh '+homedir).read()

    #TODO : Legacy from v1 - check this
    if len(lblPstatus) < 60:
        lblPstatus = 'Updating!'
        getstatus()

    if 'Disconnected' in lblPstatus and quickcheck=='yes\n':
        lblPstatus='Updating!'
        getstatus()
		
    if 'Connected' in lblPstatus and quickcheck=='no\n':
        lblPstatus='Updating!'
        getstatus()

    if quickcheck=='no\n':
        if isKill.get():
            status = os.popen('sudo sh kill.sh').read()
            isKillActive = True
        label.config(fg="red")
        w=filemenu.index("Connect-Last",  )
        filemenu.entryconfig(w, state = "normal")
        lblPstatus = lblPstatus.replace('%', '')
    else:
        label.config(fg="blue")
        w=filemenu.index("Connect-Last",  )
        filemenu.entryconfig(w, state = "disabled")

    if isKillActive:
        label.config(fg="red")
        lblPstatus = '**  KILL  **\n** SWITCH **\n** ACTIVE!**'

    # TODO: work out what v2 does here
    # if 'Internet : Offline' in lblPstatus:
    #     label.config(fg='orange')
    #     lblPstatus = lblPstatus.replace('Internet : Offline',  '*INTERNET* : *OFFLINE*')

    # TODO: check this!!
    if 'Load' in lblPstatus:
        x2 = lblPstatus.find('%')
        if not x2==-1:
            load = int(lblPstatus[int(x2-3): int(x2)])
            if load > 85:
                label.config(fg="orange")
                lblPstatus = lblPstatus.replace('Load',  '*LOAD*')
            
		

    if isMini.get() and not isKillActive:
        statuslines = lblPstatus.splitlines(True)
        origPstatus = lblPstatus
        if quickcheck=='yes\n':
            lblPstatus = statuslines[0] + statuslines[1] + statuslines[4] + statuslines[9] + statuslines[10]
        else:
            lblPstatus = statuslines[0] + statuslines[1] + statuslines[2] + statuslines[3]
        if isPing.get() and 'Ping' in origPstatus:
            if quickcheck=='yes\n':
                lblPstatus = lblPstatus + statuslines[13]
            else:
                lblPstatus = lblPstatus + statuslines[4]
                
    if not isPing.get() and not isMini.get():
        x = lblPstatus.find('Google')
        lblPstatus = lblPstatus[0:x]
    label.config(text=str(lblPstatus))

  def count():

    global counter
    global pollspeed
    counter = counter +1
    if pollspeed.get() == 1000:
        wait = 61
    else:
        wait = 64*4
		
    if counter == 1:
        update(True)

    if counter==wait:
        update(True)
        counter = 1
    else:
        update(False)
    label.after(pollspeed.get(), count)
  count()

def fastconnect():
	global isKillActive
	global isMini
	global counter
                
	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn c -f').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False
		isMini.set(False)
		counter = 0


def p2pconnect():
	global isKillActive
	global isMini
	global counter

	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn c --p2p').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False
		isMini.set(False)
		counter = 0
		
def torconnect():
	global isKillActive
	global isMini
	global counter
	
	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn c --tor').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False
		isMini.set(False)
		counter = 0
		
def scconnect():
	global isKillActive
	global isMini
	global counter
	
	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn c --sc').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False
		isMini.set(False)
		counter = 0
		
def lastconnect():
	global isKillActive
	global isMini
	global counter
	
	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn r').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False
		isMini.set(False)
		counter = 0
		
def rndconnect():
	global isKillActive
	global isMini
	global counter	

	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn c -r').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False      
		isMini.set(False)
		counter = 0
		
def reconnect():
	global isKillActive
	global isMini
	global counter
	
	if isKillActive:
		status = os.popen('sudo sh iprestore.sh ' + homedir).read()
	disconnect()
	status=os.popen('sudo protonvpn r').read()
	print(status)
	if 'Connected!' in status:
		isKillActive = False      
		isMini.set(False)
		counter = 0
		
def disconnect():
      status=os.popen('sudo protonvpn d').read()
      print(status)
      
def about():
	messagebox.showinfo("About", 'Proton VPN\nMonitor Tool\n\nVersion 2.0beta\n\nm0nk3h')

def help():
	text = 'When using the VPN menu, only servers that are available on your subscription plan will connect.\n\nAn error will be displayed in the Terminal if you select a server type that is not available on your plan.\n\n'
	text = text +'If the status line stops moving for more than a few seconds (a few seconds delay is a server query), check terminal output for any errors.  Pvpnmon is Beta status.\n\n'
	text = text + 'If server details are not shown (IP, Exit Country, Server Load, etc), this could be due to the server being busy. \n\n'
	text = text + 'Google Ping shows the time it takes to receive a ping reply from google.com, to indicate the latency of your connection. It updates once per minute.  You can disable this in the Opt menu.\n\n'
	text = text + 'Disconnection detection is less than 1 second by default.  If you select Fast Poll from Opt menu, this will improve to less than 1/4 second, at the expense of higher CPU use & disk reads.\n\n'
	text = text + '**Experimental** Kill-Switch, when activated in the Opt menu will halt *all* network traffic on your machine on a disconnection detection (see above). Reconnect by using the VPN menu. Killswitch in the status window refers to the ProtonVPN commandline option, NOT the status of the PvpnMon internal killswitch.'
	messagebox.showinfo('Help / FAQ', text)

def ctryconnect():
	root.withdraw() 
	sub = tk.Tk()
	sub.title('Country Select')
	subheader=tk.Label(sub, fg="black")
	subheader.pack()
	tkvar = StringVar(sub)
	choices = ['AU - Australia', 'AT - Austria',  'BE - Belgium',  'BR - Brazil',  'BG - Bulgaria',
	'CA - Canada',  'CR - Costa Rica',  'CZ - Czech Republic',  'DK - Denmark',  'EE - Estonia', 
	'FI - Finland',  'FR - France',  'DE - Germany',  'HK - Hong Kong',  'IS - Iceland', 
	'IN - India',  'IE - Ireland',  'IL - Isreal',  'IT - Italy',  'JP - Japan',  'KR - Korea (Republic of)', 
	'LU - Luxembourg',  'NL - Netherlands',  'NZ - New Zealand',  'NO - Norway',  'PL - Poland',  'PT - Portugal',
	'RO - Romania',  'RU - Russian Federation',  'SG - Singapore',  'ZA - South Africa',  'ES - Spain',  
	'SE - Sweden',  'CH - Switzerland',  'TW - Taiwan',  'UK - Ukraine',  'UK - United Kingdom',  'US - United States']
	popupMenu = OptionMenu(sub, tkvar, *choices)
	popupMenu.pack()
	tkvar.set('NL - Netherlands') 
	tkvar2 = StringVar(sub)
	choices2 = {'UDP', 'TCP'}
	popupMenu2 = OptionMenu(sub, tkvar2,  *choices2)
	popupMenu2.pack()
	tkvar2.set('UDP')
	
	subspacer=tk.Label(fg='black')
	subspacer.config(text=' ')
	subspacer.pack()
	
	def ctryconnectexit():
		ccode=tkvar.get()[0:2] + ' -p ' + tkvar2.get()
		global isKillActive
		if isKillActive:
			status = os.popen('sudo sh iprestore.sh ' + homedir).read()
		disconnect()
		print(ccode)
		status=os.popen('sudo protonvpn connect --cc ' + ccode).read()
		print(status)
		if 'Connected!' in status:
			isKillActive = False
		isMini.set(False)
		
		root.update()
		root.deiconify()
		
	def exit():
		root.update()
		root.deiconify()
		sub.destroy()
		
	buttonok = tk.Button(sub, text='Connect', width=12, command=ctryconnectexit)
	buttonok.pack()
	buttonexit = tk.Button(sub, text='Exit', width=8, command=exit)
	buttonexit.pack()

	sub.mainloop()
    
root = tk.Tk()
global isMini
global isPing
global ping
global pollspeed
global isKill
global isKillActive
global txtWorking
pollspeed = tk.IntVar()
pollspeed.set(1000)
ping = '  '
isMini = tk.BooleanVar()
isMini.set(False)
isPing = tk.BooleanVar()
isPing.set(True)
isKill = tk.BooleanVar()
isKill.set(False)
isKillActive = False
txtWorking = '---+---+---+---+---+'

root.title("ProtonVPN Monitor")    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Connect-Fastest", command=fastconnect)
filemenu.add_command(label="Conn.-Fast. p2p", command=p2pconnect)
filemenu.add_command(label="Conn.-Fast. Tor", command=torconnect)
filemenu.add_command(label="Conn.-Fast. SCore", command=scconnect)
filemenu.add_command(label="Conn.-Fast. Ctry", command=ctryconnect)
filemenu.add_separator()
filemenu.add_command(label="Connect-Last", command=lastconnect)
filemenu.add_command(label="Connect-Random", command=rndconnect)
filemenu.add_separator()
filemenu.add_command(label="Reconnect", command=reconnect)
filemenu.add_command(label="Disconnect", command=disconnect)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="VPN", menu=filemenu)
w=filemenu.index("Connect-Last",  )
filemenu.entryconfig(w, state = "disabled")
optmenu = Menu(menubar, tearoff=0)
optmenu.add_checkbutton(label='Mini GUI',  onvalue=True,  offvalue=False,  variable =isMini)
optmenu.add_checkbutton(label='Ping',  onvalue=True,  offvalue=False,  variable =isPing)
optmenu.add_checkbutton(label='Fast Poll',  onvalue=250,  offvalue=1000,  variable =pollspeed)
optmenu.add_checkbutton(label='Kill Switch',  onvalue=True,  offvalue=False,  variable =isKill)
menubar.add_cascade(label='Opt.',  menu=optmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help / FAQ", command=help)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

if os.access("logo.gif", os.F_OK):
	logo = tk.PhotoImage(file="logo.gif")
	label = tk.Label(root, fg="blue", compound = tk.CENTER,  image=logo)
else:
	label = tk.Label(root, fg="blue")
label.pack()
counter_label(label)
#print(os.popen('sudo sh ipsave.sh ' + homedir).read())
#print(os.popen('sudo pvpn --update').read())

if len(sys.argv)==2:
	if str(sys.argv[1])=='-top':
		root.call('wm', 'attributes', '.', '-topmost', '1')
#root.call('wm',  'iconify',  '.')
#gets rid of window decorations, but makes it unmoveable!
#root.call('wm',  'overrideredirect', '.',  'True')
root.mainloop()

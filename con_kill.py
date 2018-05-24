import psutil
import os
import time
import tkMessageBox
import geoip2.database
from tkinter import *
import socket



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

reader = geoip2.database.Reader('GeoLite2.mmdb')
labels = []
buttons=[]
root = Tk()

root.minsize(width=650,height=500)
root.maxsize(width=650,height=500)
root.resizable(width=False, height=False)
root.title("Connections")

canvas = Canvas(root)
scrolly = Scrollbar(root, orient='vertical', command=canvas.yview)
canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)


def close_pid(pid):
	try:
		p = psutil.Process(pid)
		#result = tkMessageBox.askquestion("Close", "Closed Process with PID : "+str(pid), icon='warning')
		tkMessageBox.showinfo( "Hello Python", "Closed Process with PID : "+str(pid))
		#if result == 'yes':
		p.terminate() 
		#	return
		#else:
		#	pass			
	except psutil.NoSuchProcess,e :
		tkMessageBox.showinfo( "Error", "No such Proc")

def get_con():	
	print "EDO"
	global labels
	global buttons
	canvas.delete("all")
	x =0	
	connections = psutil.net_connections(kind = "all")
	for connect in connections :	
		#print connect.raddr
		#sock.bind("lockalhost",connect.raddr.port)
		if (len(connect.raddr)==0 or connect.pid == None) :
			pass
		else:			
			print connect.raddr.ip, " ", connect.pid
			process = psutil.Process(connect.pid) 
			pid_num = connect.pid
			

			try :
				address = reader.country(str(connect.raddr.ip)).country #< <<<< <<< <<< ERROR WHILE PROCCESSING IPv6
				f = address.name
				address = f
				label = Label(root, text='IP : '+str(connect.raddr.ip) +' Adress :  '+ str(address) +' PID : ' + str(connect.pid)+ ' Proc_Name : ' + str(process.name()))
				b = Button(root, text ="Close", command = lambda pid_num=pid_num: close_pid(pid_num))
			except Exception, e :
				print (e)
				label = Label(root, text='IP : '+str(connect.raddr.ip)+' Adress :  Error' + ' PID : ' + str(connect.pid)+ ' Proc_Name : ' + str(process.name()) )
				b = Button(root, text ="Close", command = lambda pid_num=pid_num: close_pid(pid_num))
			canvas.create_window(0, x*50, anchor='nw', window=label, height=50)
			canvas.create_window(550, x*50, anchor='nw', window=b, height=50)
			#labels.append(label)
			#buttons.append(b)
			x+=1
		count = 0
		#for lbl in labels:
		#	lbl.pack()
		#	buttons[count].pack()
		#	count +=1
	canvas.pack(fill='both', expand=True, side='left')
	scrolly.pack(fill='y', side='right')
	root.after(2000,get_con)	
get_con()
root.mainloop()
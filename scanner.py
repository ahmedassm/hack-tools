#!/usr/bin/python

'''
this script is made by ahmed assem
'''



from socket import *
import threading
import sys
import os
from scapy.all import getmacbyip


red = "\033[1;31m"
yellow = "\033[1;33m"
cyan = "\033[1;36m"
grey = "\033[0;37m"

python3 = False
python_v = sys.version_info[0]

if python_v == 3:
	python3 = True
ip_list = []

if os.geteuid() != 0:
	print(yellow + "[!] you need super user.")
	exit()


class myThread (threading.Thread):
   def __init__(self,ip):
      threading.Thread.__init__(self) ; self.ip = ip
   def run(self):
      check(self.ip,False)


def check(ip,aon):
	global ip_list
	try:
		sock = socket(AF_INET , SOCK_STREAM)
		#sock.settimeout(1)
		sock.connect((ip,1111))
	except Exception as e:
		if str(e).strip().split(" ")[3] == "refused":
			if aon:
				return True
			else:
				try:
					host = gethostbyaddr(ip)[0]
					mac = str(getmacbyip(ip)).upper()
					if mac != "FF:FF:FF:FF:FF:FF":
						#ip_list.append(host + "=>" + ip + "=> " + mac)
						print(grey + " [" + ip + " " + host + "] ")
				except:
					None

		else:
			#print(str(e).strip())
			return False


def scan():
	print(yellow + "[!] All Thread's Has Been Started")
	for num in range(1,256):
		ip = "192.168.1."+str(num)
		thread1 = myThread(ip)
		thread1.start()



if __name__ == "__main__":
	scan()
	

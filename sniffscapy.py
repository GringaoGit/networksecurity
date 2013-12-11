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
    print "Usage: sniffscapy.py VICTIM PORT"
    sys.exit(1)
 
     
my_mac = get_mac_address()
if not my_mac:
    print "No mac found, Bye"
    sys.exit(1)
 
ip1 = sys.argv[1]
#ip2 = sys.argv[2]
num = sys.argv[2]

my_filter = 'host ' + ip1 + ' and port ' + num
print my_filter

with open("sniffed", "a") as f:
	f.write("\n\n### New Sniffing ### " + my_filter + " ###\n\n")

while 1 :
	found = sniff(filter=my_filter, count=1)
    print found
	print "### cool ### happy ###"
	with open("sniffed", "a") as f:
		f.write("{} \n\n".format(found))
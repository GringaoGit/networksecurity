#!/usr/bin/python
import sys
from dns.resolver import query
from dns.exception import DNSException

def revip(ip):
	n = ip.split('.')
	n.reverse()
	return '.'.join(n)
sstr = '%s.sbl.spamhaus.org.'
def sblip(ip):
	qstr = sstr % revip(ip)
	try:
		qa = query(qstr, 'TXT')
	except DNSException:
		return
	for rr in qa:
		for s in rr.strings:
			print s
def process(args):
	for ip in args:
		sblip(ip)
if __name__ == '__main__':
	process(sys.argv[1:])

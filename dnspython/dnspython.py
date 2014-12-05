#! /usr/bin/python

"""
Licence : BeerWare
"""

import dns.resolver
import dns.query
import dns.zone
import dns.reversename

host = 'myges.fr'

# record A
answers_IPv4 = dns.resolver.query(host, 'A')
for rdata in answers_IPv4:
    print 'IPv4 :',rdata.address
    ipaddress = rdata.address

# record AAAA
try:
    answers = dns.resolver.query(host, 'AAAA')
    for rdata in answers:
        print rdata
except dns.resolver.NoAnswer:
    print "*** No AAAA record for", host, "***"
except dns.resolver.NXDOMAIN:
    print "*** The domain", host, "does not exist ***"

#Record PTR
try:
    no = dns.reversename.from_address(ipaddress)
    answers = dns.resolver.query(no, 'PTR')
    for rdata in answers:
        print rdata.target
except dns.resolver.NoAnswer:
    print "*** No PTR record for", ipadress, "***"
except dns.resolver.NXDOMAIN:
    print "*** The domain", host, "does not exist ***"

#Record MX
try:
    answers = dns.resolver.query(host, 'MX')
    for rdata in answers:
        print 'MX : ', rdata.exchange, 'has preference', rdata.preference
except dns.resolver.NoAnswer:
    print "*** No MX record for", host, "***"
except dns.resolver.NXDOMAIN:
    print "*** The domain", host, "does not exist ***"

#Record TXT
try:
    for txtrecord in dns.resolver.query(host, 'TXT'):
        print txtrecord.to_text()
except dns.resolver.NoAnswer:
    print "*** No TXT record for", host, "***"
except dns.resolver.NXDOMAIN:
    print "*** The domain", host, "does not exist ***"

# Any records
name_server = '8.8.8.8' #Google's DNS server
ADDITIONAL_RDCLASS = 65535
request = dns.message.make_query(host, dns.rdatatype.ANY)
request.flags |= dns.flags.AD
request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                       dns.rdatatype.OPT, create=True, force_unique=True)       
response = dns.query.udp(request, name_server)
print response
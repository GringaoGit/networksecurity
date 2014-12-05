#!/usr/bin/env python

"""
## Licence : BeerWare !
## Usage : python uriscanqualys.py
"""

import subprocess
import getpass
import sys

# Peut etre rempli automatiquement.
username = raw_input('Enter your username: ')
password = getpass.getpass('Enter your password: ')
title = raw_input('Enter the title of the scan: ')
asset_groups = raw_input('Enter the asset_groups that you want to scan (ex: testgroupasset): ')

query = 'https://%s:%s@qualysapi.qualys.eu/msp/scan.php?asset_groups=%s&scan_title=%s' % (username, password, asset_groups, title)
args = [
    'curl',
    '-H', 'X-Requested-With: ' + title,
    query,
]

xml_output = subprocess.check_output(args).decode('utf-8')
time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
name_file = title+time+'.xml'

f = open(name_file, 'w' )
f.write(xml_output)
f.close()

print 'Scan OK, vous pouvez consulter le fichier '+name_file+'pour voir les resultats.'

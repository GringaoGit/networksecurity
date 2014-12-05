#! /usr/bin/python

"""
Licence : BeerWare
"""
import qualysapi
import requests
import xml.etree.ElementTree as ET
import time
import sys

login = sys.argv[1]
passwd = sys.argv[2]
# scanname = sys.argv[3]

def login(s):
    payload = {
               'action':'login',
               'username':sys.argv[1],
               'password':sys.argv[2]
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/session/', data=payload)
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//TEXT'):
        print elem.text #Prints the "Logged in" message. Not really needed, but reassuring.

def logout(s):
   payload = {
               'action':'logout'
               }
   r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/session/', data=payload)
   xmlreturn = ET.fromstring(r.text)
   for elem in xmlreturn.findall('.//TEXT'):
       print elem.text   #Prints the "Logged out" message. Not really needed, but reassuring.

def launchScan(s, targetIP):
    payload = {
               'action':'launch',
               'ip':targetIP,
               'iscanner_name':'full',
               'option_id':'90202182',
               'scan_title':targetIP,
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/scan/', data=payload)
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//ITEM'):
        if (elem[0].text == 'REFERENCE'): ScanRef = elem[1].text
    return ScanRef

def checkScan(s, ScanRef):
    payload = {
               'action':'list',
               'scan_ref':ScanRef,
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/scan/', data=payload)
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//STATUS'):
        status = elem[0].text
        print elem[0].text   #Prints the status message. Not really needed, but reassuring.
    return status

def launchReport(s, ScanRef, reportType, targetIP):
    payload = {
               'action':'launch',
               'report_type':'Scan',
               'template_id':'736275',
               'output_format':reportType,
               'report_refs':ScanRef,
               'report_title':targetIP,
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/report/', data=payload)
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//ITEM'):
        if (elem[0].text == 'ID'): reportID = elem[1].text
    return reportID

def checkReport(s, reportID):
    payload = {
               'action':'list',
               'id':reportID,
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/report/', data=payload)
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//STATUS'):
        status = elem[0].text
        print elem[0].text  #Prints the status message. Not really needed, but reassuring.
    return status

def downloadReport(s, reportID, targetIP):
    payload = {
               'action':'fetch',
               'id':reportID,
               }
    r = s.post('https://qualysapi.qualys.eu/api/2.0/fo/report/', data=payload)
    with open("./Scan_Report_"+targetIP+".pdf", "wb") as report:
        report.write(r.content)

def main():
    s = requests.Session()
    s.headers.update({'X-Requested-With':'Facklers PyQual python primer'})
    login(s)
    ipList = ['212.198.219.28']
    for targetIP in ipList:
        ScanRef = launchScan(s, targetIP)
        time.sleep(600)
        while checkScan(s, ScanRef) != "Finished":
            time.sleep(600)
        reportType = 'pdf'
        reportID = launchReport(s, ScanRef, reportType, targetIP)
        time.sleep(120)
        while checkReport(s, reportID) != "Finished":
            time.sleep(120)
        downloadReport(s, reportID, targetIP)
    logout(s)
    s.close()

if __name__ == "__main__": main()
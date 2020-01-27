#!/usr/bin/env python

'''
See README.md
'''

import json
import requests
import sys

baseUrl = 'https://passwordvault/PasswordVault/WebServices/'
logonUrl= 'auth/Cyberark/CyberArkAuthenticationService.svc/Logon'
safeUrl = 'PIMServices.svc/Safes'
accountUrl = 'PIMServices.svc/Account'

credsFileName = 'creds.json'
userPermsFileName = 'user-perms.json'
userPermsFileNameNM = 'user-perms-nm.json'
vaultAdminsPermsFileName = 'vault-admin-perms.json'
accountFileName = 'adm-account-template.json'

caBundlePath = False

def croak():
    print('Aborting due to error')
    exit(1)

#

if len(sys.argv) == 1:
    print('Missing argument: username')
    userName = input('Enter username:')

else:
    userName = sys.argv[1]
    print('processing user: %s' % userName)

createAdmObj = input('create  managed ? y/n ')
createNMObj = input('create not managed ? y/n ')
objName = 'Telia-Personal-' + userName + '_adm'
objNameNM = 'Telia-Personal-' + userName + '_NM'
credsFile = open(credsFileName, 'r')
credsJson = json.load(credsFile)
credsFile.close()


requests.packages.urllib3.disable_warnings()


caUrl = baseUrl + logonUrl
resp = requests.post(caUrl, json = credsJson, verify = caBundlePath)
print('auth response code: %s' % resp.status_code)
if resp.status_code != 200: croak()
caToken = json.loads(resp.text)['CyberArkLogonResult']

if createAdmObj.lower() == 'y':

    caUrl = baseUrl + safeUrl
    caPayload = {
    "safe": {
        "objName": objName,
        "ManagingCPM": "PasswordManager1"
    }
    }
    caHeaders = {
        "Authorization": caToken
    }

    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('create safe response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()


    caUrl = baseUrl + safeUrl + '/' + objName + '/Members'
    userPermsFile = open(userPermsFileName, 'r')
    caPayload = json.load(userPermsFile, encoding = 'ascii')
    userPermsFile.close()
    caPayload['member']['MemberName'] = userName
    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('add user membership response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()


    caUrl = baseUrl + safeUrl + '/' + objName + '/Members'
    vaultAdminsPermsFile = open(vaultAdminsPermsFileName, 'r')
    caPayload = json.load(vaultAdminsPermsFile, encoding = 'ascii')
    vaultAdminsPermsFile.close()
    caPayload['member']['MemberName'] = 'Vault Admins'
    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('add admins membership response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()

if createNMObj.lower() == 'y':
    caUrl = baseUrl + safeUrl
    caPayload = {
    "safe": {
        "objName": objNameNM
    }
    }
    caHeaders = {
        "Authorization": caToken
    }
    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('create safe response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()

    caUrl = baseUrl + safeUrl + '/' + objNameNM + '/Members'
    userPermsFile = open(userPermsFileNameNM, 'r')
    caPayload = json.load(userPermsFile, encoding = 'ascii')
    userPermsFile.close()
    caPayload['member']['MemberName'] = userName
    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('add user membership response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()

    caUrl = baseUrl + safeUrl + '/' + objNameNM + '/Members'
    vaultAdminsPermsFile = open(vaultAdminsPermsFileName, 'r')
    caPayload = json.load(vaultAdminsPermsFile, encoding = 'ascii')
    vaultAdminsPermsFile.close()
    caPayload['member']['MemberName'] = 'Vault Admins'
    resp = requests.post(caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('add admins membership response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()


if createAdmObj.lower() == 'y':
    print('\tpreparing account template')
    try:
        accountFile = open(accountFileName, 'r')
        accountJson = json.load(accountFile, encoding = 'ascii')
        accountFile.close()
    except:
        print('Cannot read account template file (%s)' % accountFileName)
        croak()
    accountJson['account']['safe'] = objName
    accountJson['account']['username'] = userName + '_adm'
    print('\tadding account to safe')
    caUrl = baseUrl + accountUrl
    resp = requests.post(caUrl, json = accountJson, headers = caHeaders, verify = caBundlePath)
    if resp.status_code != 201:
        print(resp.headers)
        print(resp.text)
        croak()
'''
'''
if createAdmObj.lower() == 'y':
    caUrl = baseUrl + safeUrl + '/' + objName + '/Members/' + credsJson['username']
    resp = requests.delete(caUrl, headers = caHeaders, verify = caBundlePath)
    print('remove creator membership response code: %s' % resp.status_code)
    if resp.status_code != 200:
        print(resp.text)
        croak()


if createNMObj.lower() == 'y':
    caUrl = baseUrl + safeUrl + '/' + objNameNM + '/Members/' + credsJson['username']
    resp = requests.delete(caUrl, headers = caHeaders, verify = caBundlePath)
    print('remove creator membership response code: %s' % resp.status_code)
    if resp.status_code != 200:
        print(resp.text)
        croak()

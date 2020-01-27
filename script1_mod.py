#!/usr/bin/env python

'''
See README.md
'''

'''
Description of this script:

    With this script you can connect to some API and login only as an
    authorized user. After authorization you can upload from file new payloads,
    accounts and remove membership response codes.

For better security:

    I recomend to use Signatures with Timestamps. Works like the regular Signer
    but also records the time of the signing and can be used to expire signatures.

'''

import json
import requests
import sys

baseUrl = 'https://passwordvault/PasswordVault/WebServices/'
logonUrl= 'auth/Cyberark/CyberArkAuthenticationService.svc/Logon'
safeUrl = 'PIMServices.svc/Safes'
accountUrl = '+'

credsFileName = 'creds.json'
userPermsFileName = 'user-perms.json'
userPermsFileNameNM = 'user-perms-nm.json'
vaultAdminsPermsFileName = 'vault-admin-perms.json'
accountFileName = 'adm-account-template.json'

caBundlePath = False

def croak():
    print('Aborting due to error')
    exit(1)

def create_caUrl(name):
    return baseUrl + safeUrl + '/' + name + '/Members'

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

    resp = requests.post(
        caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('create safe response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()

    caUrl = create_caUrl(objName)

    caPayload = load_payload(userPermsFileName)
    text = 'add user membership response code: %s'
    post_response(text, caUrl, caPayload, userName)

    caPayload = load_payload(vaultAdminsPermsFileName)
    text = 'add admins membership response code: %s'
    post_response(text, caUrl, caPayload, 'Vault Admins')

    print('\tpreparing account template')
    accountJson = load_payload(accountFileName)
    accountJson['account']['safe'] = objName
    accountJson['account']['username'] = userName + '_adm'
    print('\tadding account to safe')
    caUrl = baseUrl + accountUrl
    resp = requests.post(
        caUrl, json = accountJson, headers = caHeaders, verify = caBundlePath)
    if resp.status_code != 201:
        print(resp.headers)
        print(resp.text)
        croak()

    remove_response_code(objName)

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
    resp = requests.post(
        caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print('create safe response code: %s' % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()


    caUrl = create_caUrl(objNameNM)
    caPayload = load_payload(userPermsFileNameNM)
    text = 'add user membership response code: %s'
    post_response(text, caUrl, caPayload, userName)

    caPayload = load_payload(vaultAdminsPermsFile)
    text = 'add admins membership response code: %s'
    post_response(text, caUrl, caPayload, 'Vault Admins')

    remove_response_code(objNameNM)


def post_response(text, caUrl, caPayload, user_name):
    caPayload['member']['MemberName'] = user_name
    resp = requests.post(
        caUrl, json = caPayload, headers = caHeaders, verify = caBundlePath)
    print(text % resp.status_code)
    if resp.status_code != 201:
        print(resp.text)
        croak()

def remove_response_code(obj_name):
    caUrl = baseUrl + safeUrl + '/' + obj_name + '/Members/' + credsJson['username']
    resp = requests.delete(caUrl, headers = caHeaders, verify = caBundlePath)
    print('remove creator membership response code: %s' % resp.status_code)
    if resp.status_code != 200:
        print(resp.text)
        croak()

def load_payload(file_name):
    try:
        userPermsFile = open(file_name, 'r')
        caPayload = json.load(userPermsFile, encoding = 'ascii')
        userPermsFile.close()
    except:
        print('Cannot read payment file (%s)' % accountFileName)
        croak()
    return caPayload

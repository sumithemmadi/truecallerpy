#!/usr/bin/python

# ==================================================================================
# MIT License

# Copyright (c) 2022 Emmadi Sumith Kumar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#====================================================================================

import os
import sys
import json
import codecs
import random
import argparse
import requests
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from phonenumbers.phonenumberutil import number_type
from .truecallerLogin import truecallerpy_login , truecallerpy_login_with_file ,getNumber
from .version import truecallerpy_info

parser = argparse.ArgumentParser(
    description="truecallerpy: search phone number details.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--search",  metavar='NUMBER',
                    help="search phone number")
parser.add_argument("-v", "--version", action="store_true",
                    help="print the version of the package")
parser.add_argument("-n", "--name", action="store_true", help="print's name")
parser.add_argument("-e", "--email", action="store_true", help="print's email")
parser.add_argument("-i", "--installationId",
                    action="store_true", help="print's installationId output")
parser.add_argument("--json", action="store_true",
                    help="print's json output only")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print's raw info")
parser.add_argument("--login", action="store_true", help="login to truecaller")
parser.add_argument("-f", "--file", help="use json file to login")
args = parser.parse_args()
config = vars(args)

def getNumber(x):
    if x[0] == "0":
        return x[1:].replace(" ", "")
    else:
        return x.replace(" ", "")


def getAuthKey():
    if "HOME" in os.environ:
        config_dir = os.environ['HOME'] + "/.config"
    else:
        config_dir = os.environ['HOMEPATH'] + "\.config"

    directory = "truecallerpy"
    file = "authkey.json"
    path = os.path.join(config_dir, directory, file)

    try:
        with open(path, encoding='utf-8-sig') as authKeyFile:
            authkey = json.load(authKeyFile)
        return authkey
    except FileNotFoundError:
        return "error"


def search_phonenumber(phoneNumber, regionCode, installationId):
    phNumber = phonenumbers.parse(phoneNumber, regionCode)
    nationalPhoneNumber = phonenumbers.format_number(phNumber , phonenumbers.PhoneNumberFormat.NATIONAL)

    params = {
        'q': getNumber(nationalPhoneNumber),
        'countryCode': "{}".format(phonenumbers.region_code_for_number(phNumber)),
        'type': '4',
        'locAddr': '',
        'placement': 'SEARCHRESULTS,HISTORY,DETAILS',
        'encoding': 'json'
    }
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'accept-encoding': 'gzip',
        'user-agent': 'Truecaller/11.75.5 (Android;10)',
        'clientsecret': 'lvc22mp3l1sfv6ujg83rd17btt',
        'authorization': 'Bearer ' + installationId}
    try:
        req = requests.get(
            'https://search5-noneu.truecaller.com/v2/search', headers=headers, params=params)
        #print(req.status_code, req.text)
        if req.status_code == 429:
            x = {
                "errorCode": 429,
                "errorMessage": "too many requests.",
                "data": None
            }
            return x
        elif req.json().get('status'):
            x = {
                "errorMessage": "Your previous login was expired.",
                "data": None
            }
            return x
        else:
            return req.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def truecallerpy_search_phonenumber(config):
    authenticationJson = getAuthKey()
    if authenticationJson == "error":
        print('\x1b[33mPlease login to your account\x1b[0m')
    else:
        installationId = authenticationJson["installationId"]
        # print(authenticationJson["phones"][0]["countryCode"])

        number = phonenumbers.parse(config['search'], "{}".format(
            authenticationJson["phones"][0]["countryCode"]))
        if phonenumbers.is_valid_number(number) == False:
            raise SystemExit('\x1b[31mEnter valid phone number\x1b[0m')

        phoneNumberNational = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.NATIONAL)
        jsonInfo = search_phonenumber(getNumber(
            phoneNumberNational), phonenumbers.region_code_for_number(number), installationId)

        # print(jsonInfo["data"])
        if jsonInfo["data"] == None and jsonInfo["errorCode"] == 429 and config['json'] == False:
            raise SystemExit(
                '\x1b[33mToo many requests. \nPlease try again tomorrow, maybe!\x1b[0m')
        elif jsonInfo["data"] == None and config["json"] == False and config["raw"] == False and config["email"] == False:
            raise SystemExit(
                '\x1b[33mYour previous login was expired. \nPlease login to your account\x1b[0m')
        elif jsonInfo["data"] == None and config["json"] == True and config["raw"] == False and config["email"] == False:
            print(json.dumps(jsonInfo, indent=3))
        elif config["raw"] == True and config["name"] == False and config["email"] == False:
            print(jsonInfo)
        elif jsonInfo["data"] != None and config["json"] == False and config["raw"] == True and config["name"] == True and config["email"] == False:
            try:
                if "name" in jsonInfo["data"][0]:
                    name = jsonInfo["data"][0]["name"]
                else:
                    name = "Unknown number"

                print(name)
            except OSError as error:
                raise SystemExit(error)

        elif jsonInfo["data"] != None and config["json"] == False and config["raw"] == False and config["name"] == True and config["email"] == False:
            try:
                if "name" in jsonInfo["data"][0]:
                    name = jsonInfo["data"][0]["name"]
                else:
                    name = "Unknown number"

                print("\x1b[33mName\x1b[0m : \x1b[32m {} \x1b[0m".format(name))
            except OSError as error:
                raise SystemExit(error)

        elif jsonInfo["data"] != None and config["json"] == False and config["raw"] == True and config["name"] == False and config["email"] == True:
            try:
                if len(jsonInfo["data"][0]["internetAddresses"])>0 and "id" in jsonInfo["data"][0]["internetAddresses"][0]:
                    email = jsonInfo["data"][0]["internetAddresses"][0]["id"]
                else:
                    email = "Email not found"

                print(email)
            except OSError as error:
                raise SystemExit(error)

        elif jsonInfo["data"] != None and config["json"] == False and config["raw"] == False and config["name"] == False and config["email"] == True:
            try:
                if len(jsonInfo["data"][0]["internetAddresses"])>0 and "id" in jsonInfo["data"][0]["internetAddresses"][0]:
                    email = jsonInfo["data"][0]["internetAddresses"][0]["id"]
                else:
                    email = "Email not found"

                print("\x1b[33memail\x1b[0m : \x1b[32m {} \x1b[0m".format(email))
            except OSError as error:
                raise SystemExit(error)


        else:       
            print(json.dumps(jsonInfo, indent=3))


        


def truecallerpy_get_installationId(config):
    authenticationJson = getAuthKey()
    if authenticationJson == "error":
        print('\x1b[33mPlease login to your account\x1b[0m')
    else:
        installationId = authenticationJson["installationId"]
        if config["raw"] == False:
            print('\x1b[33mYour installationId\x1b[0m : \x1b[32m {}\x1b[0m'.format(
                installationId))
        else:
            print(installationId)
            
def ExecuteTrurcallerPy():
    os.system("")
    if config["version"] == True and config['login'] == False and config['file'] == None and config['name'] == False and config['raw'] == False and config['search'] == None and config['installationId'] == False:
        print(truecallerpy_info())
    elif config['login'] == True and config['file'] == None and config['name'] == False and config['raw'] == False and config['search'] == None and config['installationId'] == False:
        truecallerpy_login(config)
    elif config['login'] == True and config['name'] == False and config['raw'] == False and config['search'] == None and config['installationId'] == False:
        truecallerpy_login_with_file(config)
    elif config['login'] == False and config['file'] == None and config['search'] != None and config['installationId'] == False:
        truecallerpy_search_phonenumber(config)
    elif config['login'] == False and config['file'] == None and config['search'] == None and config['installationId'] == True:
        truecallerpy_get_installationId(config)
    else:
        parser.print_help()

if __name__ == '__main__':
     ExecuteTrurcallerPy()

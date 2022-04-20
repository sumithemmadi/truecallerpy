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
import argparse
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from phonenumbers.phonenumberutil import number_type
import requests
import random
import codecs
from .phonesList import truecallerpy_get_random_phone


def getNumber(x):
    if x[0] == "0":
        return x[1:].replace(" ", "")
    else:
        return x.replace(" ", "")

def truecallerpy_login(config):
    if "HOME" in os.environ:
        config_dir = os.environ['HOME'] + "/.config"
    else:
        config_dir = os.environ['HOMEPATH'] + "\.config"
    # print(config_dir)
    directory = "truecallerpy"
    file = "authkey.json"
    dir_path = os.path.join(config_dir, directory )
    path = os.path.join(config_dir, directory, file)
    try:
        os.makedirs(dir_path, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        raise SystemExit(error)

    print('\x1b[33mLogin\n\n Enter mobile number in International Format\n Example : +919912345678.\x1b[0m')
    number = input('Enter Mobile Number : ')
    if number[0] != "+":
        raise SystemExit('\x1b[31mEnter valid phone number in International Format\x1b[0m')
    phoneNumber = phonenumbers.parse(number, None)

    # check if a number is valid
    if phonenumbers.is_valid_number(phoneNumber) == False:
         raise SystemExit('\x1b[31mEnter valid phone number in International Format\x1b[0m')
    phoneNumberNational = phonenumbers.format_number(
        phoneNumber, phonenumbers.PhoneNumberFormat.NATIONAL)
    print('\x1b[32mSending otp to {} \x1b[0m'.format(getNumber(number)))
    phoneSpecs = truecallerpy_get_random_phone()

    data = {
        "countryCode": phonenumbers.region_code_for_number(phoneNumber),
        "dialingCode": phonenumbers.country_code_for_region(phonenumbers.region_code_for_number(phoneNumber)),
        "installationDetails": {
            "app": {
                "buildVersion": 5,
                "majorVersion": 11,
                "minorVersion": 7,
                "store": "GOOGLE_PLAY"
            },
            "device": {
                "deviceId": ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrst') for i in range(16)),
                "language": "en",
                "manufacturer": "{}".format(phoneSpecs["manufacturer"]),
                "model": "{}".format(phoneSpecs["model"]),
                "osName": "Android",
                "osVersion": "10",
                "mobileServices": ["GMS"]
            },
            "language": "en"
        },
        "phoneNumber": getNumber(phoneNumberNational),
        "region": "region-2",
        "sequenceNo": 2
    }

    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'accept-encoding': 'gzip',
        'user-agent': 'Truecaller/11.75.5 (Android;10)',
        'clientsecret': 'lvc22mp3l1sfv6ujg83rd17btt'
    }

    postRequest = requests.post(
        'https://account-asia-south1.truecaller.com/v2/sendOnboardingOtp', headers=headers, json=data)

    if postRequest.json()['status'] == 1 or postRequest.json()['status'] == 9 or postRequest.json()['message'] == "Sent":
        print('\x1b[32mOtp sent successfully\x1b[0m')

        # otp verification part
        otp = input('Enter Received OTP: ')
        postData = {
            "countryCode": phonenumbers.region_code_for_number(phoneNumber),
            "dialingCode": phonenumbers.country_code_for_region(phonenumbers.region_code_for_number(phoneNumber)),
            "phoneNumber": getNumber(phoneNumberNational),
            "requestId": postRequest.json()['requestId'],
            "token": otp
        }

        otpPostRequest = requests.post(
            'https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp', headers=headers, json=postData)

        if otpPostRequest.json()['status'] == 2:
            print('\x1b[33mYour installationId\x1b[0m : \x1b[32m {}\x1b[0m'.format(
                otpPostRequest.json()['installationId']))
            # print(otpPostRequest.json())
            authKeyFile = open(path , "w")
            json.dump(otpPostRequest.json(), authKeyFile, indent=3)
            authKeyFile.close()
            print('\x1b[32mLogged in successfully.\x1b[0m')
        elif otpPostRequest.json()['status'] == 11:
            # print(otpPostRequest.json())
            print('\x1b[31m! Invalid OTP\x1b[0m')
        else:
            print(otpPostRequest.json()['message'])

    elif (postRequest.json()['status'] == 6):
        print('\x1b[31mYou have exceeded the limit of verification attempts.\nPlease try again after some time.\x1b[0m')
    else:
        print('\x1b[31m {} \x1b[0m'.format(postRequest.json()['message']))

def truecallerpy_login_with_file(config):
    if "HOME" in os.environ:
        config_dir = os.environ['HOME'] + "/.config"
    else:
        config_dir = os.environ['HOMEPATH'] + "\.config"

    directory = "truecallerpy"
    file = "authkey.json"
    dir_path = os.path.join(config_dir, directory )
    path = os.path.join(config_dir, directory,file)
    try:
        os.makedirs(dir_path, exist_ok=True)
        # print("Directory '%s' created successfully" % directory)
    except OSError as error:
         raise SystemExit("Login failed! \nDirectory '%s' can not be created" % directory)

    try:
        # loginJsonFile = open(config['file'])
        with open(config['file']) as loginJsonFile:
            jsonFileData = json.load(loginJsonFile)
            
        installationIdJSON = {
            "status": 2,
            "message": "Verified",
            "installationId": "{}".format(jsonFileData["account"]["installations"][0]["installation"]["id"]),
            "ttl": 123456,
            "userId": "{}".format(jsonFileData["account"]["userId"]),
            "suspended": False,
            "phones": [
                {
                    "phoneNumber": "{}".format(jsonFileData["profile"]["personalData"]["phoneNumbers"][0]["number"]),
                    "countryCode": "{}".format(jsonFileData["profile"]["personalData"]["phoneNumbers"][0]["countryCode"]),
                    "priority": 1
                }
            ]
        }

        print('\x1b[33mYour installationId\x1b[0m : \x1b[32m {}\x1b[0m'.format(jsonFileData["account"]["installations"][0]["installation"]["id"]))
        authKeyFile = open(path, "w")
        json.dump(installationIdJSON, authKeyFile, indent=3)
        authKeyFile.close()
        print('\x1b[32mLogged in successfully.\x1b[0m')

    except IOError:
        raise SystemExit("Login failed!\n" + config['file'] + " the file is not accessible or fail to create " + path)
    finally:
        loginJsonFile.close()



# if __name__ == '__main__':
#     truecallerpy_login(config)
#     truecallerpy_login_with_file(config)

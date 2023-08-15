#!/usr/bin/env python

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
# ====================================================================================

import os
import sys
import json
import argparse
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat
import questionary
import colorama
from colorama import Fore, Style
from .login import login
from .verify_otp import verify_otp
from .search import search_phonenumber, bulk_search
import asyncio


# Initialize colorama
colorama.init()

homePath = os.path.expanduser("~")
truecallerpyAuthDirPath = os.path.join(homePath, ".config", "truecallerpy")
requestFilePath = os.path.join(truecallerpyAuthDirPath, "request.json")
authKeyFilePath = os.path.join(truecallerpyAuthDirPath, "authkey.json")

if not os.path.exists(truecallerpyAuthDirPath):
    try:
        os.makedirs(truecallerpyAuthDirPath, exist_ok=True)
    except OSError as error:
        print(error)
        exit(1)

# Function to validate phone number


def validate_phone_number(input):
    try:
        pn = phonenumbers.parse(input, None)
        if not phonenumbers.is_valid_number(pn):
            return "Invalid Phone Number"
        return True
    except phonenumbers.NumberParseException:
        return "Enter a valid phone number in International Format"

# Function to validate OTP


def validate_otp(input):
    if len(input) != 6 or not input.isdigit():
        return "Enter a valid 6-digit OTP."
    return True


def check_for_file():
    if not os.path.isfile(authKeyFilePath):
        return False

    try:
        with open(authKeyFilePath) as file:
            json.load(file)
        return True
    except (ValueError, IOError):
        return False

# Function to perform the login process


def loginFuntion():
    print(
        f"{Fore.YELLOW}{Style.BRIGHT}Login\n\n Enter mobile number in International Format\n Example : {Fore.MAGENTA}+919912345678{Fore.YELLOW}.\n"
    )

    questions = [
        {
            "type": "text",
            "name": "phonenumber",
            "message": "Enter your phone number:",
            "validate": lambda input: validate_phone_number(input),
        }
    ]
    inputNumber = questionary.prompt(questions)

    try:
        pn = phonenumbers.parse(inputNumber["phonenumber"], None)
    except phonenumbers.NumberParseException:
        print("Enter a valid phone number in International Format")
        exit(1)

    response = None
    new_req = True

    if os.path.exists(requestFilePath):
        with open(requestFilePath, "r") as file:
            fileData = json.load(file)
            if (
                "parsedPhoneNumber" in fileData
                and f"+{fileData['parsedPhoneNumber']}" == inputNumber["phonenumber"]
            ):
                print(
                    f"{Fore.MAGENTA}\nPrevious request was found for this mobile number.\n"
                )
                x = questionary.confirm(
                    "Do you want to enter previous OTP?").ask()

                if x:
                    new_req = False
                    response = fileData

    if new_req:
        response = asyncio.run(login(str(inputNumber["phonenumber"])))
        print(
            f"{Fore.YELLOW}Sending OTP to {Fore.GREEN}{inputNumber['phonenumber']}{Fore.YELLOW}."
        )
    

    if (
        response["data"]["status"] == 1
        or response["data"]["status"] == 9
        or response["data"]["message"] == "Sent"
    ):
        with open(requestFilePath, "w") as file:
            json.dump(response["data"], file, indent=4)

        if new_req:
            print(f"{Fore.GREEN}OTP sent successfully.")

        questions1 = [
            {
                "type": "text",
                "name": "otp",
                "message": "Enter Received OTP:",
                "validate": lambda input: validate_otp(input),
            }
        ]

        token = questionary.prompt(questions1)

        response1 = asyncio.run(verify_otp(
            str(inputNumber["phonenumber"]),
            response["data"],
            token["otp"],
        ))

        if "status" in response1["data"] and response1["data"]["status"] == 2 and "suspended" in response1["data"] and not response1["data"]["suspended"]:
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}Your installationId: {Fore.GREEN}{response1['data']['installationId']}"
            )

            with open(authKeyFilePath, "w") as file:
                json.dump(response1["data"], file, indent=3)

            print(f"{Fore.GREEN}Logged in successfully.")
            os.remove(requestFilePath)
        elif "status" in response1['data'] and response1["data"]["status"] == 11 or response1["data"]["status"] == 40101:
            print(f"{Fore.RED}! Invalid OTP")
            print(
                f"OTP not valid. Enter the 6-digit OTP received on {inputNumber['phonenumber']}."
            )
        elif "status" in response1["data"] and response1["data"]["status"] == 7:
            print(f"{Fore.RED}Retries limit exceeded")
            print(
                f"Retries on secret code reached for {inputNumber['phonenumber']}."
            )
        elif "suspended" in response1["data"] and response1["data"]["suspended"] == True:
            print(f"{Fore.RED}Oops... Your account is suspended.")
            print("Your account has been suspended by Truecaller.")
        elif "message" in response1["data"]:
            print(f"{Fore.RED}{response1['data']['message']}")
        else:
            print(json.dumps(response1, indent=4))
    elif "status" in response and response["data"]["status"] == 6 or response["data"]["status"] == 5:
        if os.path.exists(requestFilePath):
            os.remove(requestFilePath)
        print(
            f"{Fore.RED}You have exceeded the limit of verification attempts.\nPlease try again after some time."
        )
    else:
        print(f"{Fore.RED}{response['data']['message']}")


def searcFunction(args):
    if not check_for_file():
        print(Fore.MAGENTA + Style.BRIGHT +
              "Please login to your account." + Style.RESET_ALL)
        sys.exit()

    try:
        with open(authKeyFilePath, "r") as auth_key_file:
            data = auth_key_file.read()
            json_auth_key = json.loads(data)
            country_code = json_auth_key["phones"][0]["countryCode"]
            installation_id = json_auth_key["installationId"]

        # Perform the search operation
        search_result = asyncio.run(search_phonenumber(
            args.search, country_code, installation_id))

        if args.name and not args.email:
            try:
                name = search_result["data"]['data'][0]['name']
            except (AttributeError, IndexError, KeyError):
                name = "Unknown Name"

            print(
                name if args.raw else f"{Fore.BLUE + Style.BRIGHT}Name: {Fore.GREEN}{name}{Style.RESET_ALL}")

        elif not args.name and args.email:
            try:
                data = search_result["data"].get("data")
                if data and len(data) > 0:
                    internet_addresses = data[0].get("internetAddresses")
                    if internet_addresses and len(internet_addresses) > 0:
                        email = internet_addresses[0].get("id")
                    else:
                        email = "Unknown Email"
                else:
                    email = "Unknown Email"

            except (AttributeError, IndexError, KeyError):
                email = "Unknown Email"

            print(
                email if args.raw else f"{Fore.BLUE + Style.BRIGHT}Email: {Fore.GREEN}{email}{Style.RESET_ALL}")
        else:
            print(search_result if args.raw else json.dumps(
                search_result, indent=2))
    except Exception as error:
        print(Fore.RED + str(error) + Style.RESET_ALL)


def bulkSearchFunction(args):
    if not check_for_file():
        print(Fore.MAGENTA + Style.BRIGHT +
              "Please login to your account." + Style.RESET_ALL)
        sys.exit()
    try:
        with open(authKeyFilePath, "r") as auth_key_file:
            data = auth_key_file.read()
            json_auth_key = json.loads(data)

            countryCode = json_auth_key["phones"][0]["countryCode"]
            installationId = json_auth_key["installationId"]

        # Perform bulk search operation
        search_result = asyncio.run(bulk_search(
            str(args.bs), countryCode, installationId))

        print(json.dumps(search_result)
              if args.raw else json.dumps(search_result, indent=2))

    except Exception as error:
        print(error)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        usage="\n%(prog)s login (Login to Truecaller).\n%(prog)s -s [number] (command to search a number)."
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("login", help="Login to Truecaller")

    parser.add_argument("-s", "--search", metavar="NUMBER",
                        help="Phone number to search")

    parser.add_argument(
        "-r", "--raw", help="Print raw output", action="store_true")
    parser.add_argument("--bs", "--bulksearch", metavar="NUMBERS",
                        help="Make a bulk number search")
    parser.add_argument(
        "-e", "--email", help="Print email assigned to the phone number", action="store_true")
    parser.add_argument(
        "-n", "--name", help="Print name assigned to the phone number", action="store_true")

    parser.add_argument("-i", "--installationid",
                        help="Show your InstallationId", action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="Show additional information", action="count")

    args = parser.parse_args()

    if args.command == "login":
        loginFuntion()
    elif args.search:
        searcFunction(args)
    elif args.bs:
        bulkSearchFunction(args)
    elif args.installationid:
        if not check_for_file():
            print(Fore.MAGENTA + Style.BRIGHT +
                  "Please login to your account." + Style.RESET_ALL)
            sys.exit()

        try:
            with open(authKeyFilePath, "r") as auth_key_file:
                data = auth_key_file.read()
                json_auth_key = json.loads(data)

                installationId = json_auth_key["installationId"]

                if args.raw:
                    print(installationId)
                else:
                    print(Fore.BLUE + Style.BRIGHT + "Your InstallationId: " +
                          Style.RESET_ALL + Fore.GREEN + installationId + Style.RESET_ALL)
        except Exception as error:
            print(Fore.RED + "An error occurred." + Style.RESET_ALL)
            print(error)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

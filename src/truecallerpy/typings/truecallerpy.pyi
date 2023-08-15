import random
import requests
from typing import Dict, List, Union
import phonenumbers
from phonenumbers import parse as parse_phone_number
from phonenumbers.phonenumberutil import region_code_for_country_code
from ..data.phones_list import get_random_device

def generate_random_string(length: int) -> str:
    """
    Generate a random string of the given length.

    Args:
        length (int): The length of the random string.

    Returns:
        str: The generated random string.
    """
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(characters) for _ in range(length))


def login(phone_number: str) -> Dict[str, Union[str, int]]:
    """
    Login to Truecaller.

    Args:
        phone_number (str): Phone number in international format.

    Returns:
        dict: The login response containing the requestId used for OTP verification.

    Raises:
        ValueError: If the phone number is invalid.
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    pn = parse_phone_number(phone_number, None)
    device = get_random_device()

    if not pn or not pn.country_code or not pn.national_number:
        raise ValueError("Invalid phone number.")

    post_url = "https://account-asia-south1.truecaller.com/v2/sendOnboardingOtp"

    data = {
        "countryCode": str(region_code_for_country_code(pn.country_code)),
        "dialingCode": pn.country_code,
        "installationDetails": {
            "app": {
                "buildVersion": 5,
                "majorVersion": 11,
                "minorVersion": 7,
                "store": "GOOGLE_PLAY",
            },
            "device": {
                "deviceId": generate_random_string(16),
                "language": "en",
                "manufacturer": device["manufacturer"],
                "model": device["model"],
                "osName": "Android",
                "osVersion": "10",
                "mobileServices": ["GMS"],
            },
            "language": "en",
        },
        "phoneNumber": str(pn.national_number),
        "region": "region-2",
        "sequenceNo": 2,
    }

    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "clientsecret": "lvc22mp3l1sfv6ujg83rd17btt",
    }

    response = requests.post(post_url, json=data, headers=headers)
    return response.json()


def verify_otp(phone_number: str, json_data: Dict[str, str], otp: str) -> Dict[str, Union[str, int]]:
    """
    Verify the OTP (One-Time Password) for phone number verification.

    Args:
        phone_number (str): The phone number in international format.
        json_data (dict): The JSON response data from the login request containing the requestId.
        otp (str): The OTP to verify.

    Returns:
        dict: The verification response containing the result of the OTP verification.

    Raises:
        ValueError: If the phone number is invalid.
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    try:
        parsed_number = parse_phone_number(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Phone number should be in international format.")

        country_code = str(region_code_for_country_code(
            parsed_number.country_code))
        dialing_code = parsed_number.country_code
        phone_number = str(parsed_number.national_number)

        post_data = {
            "countryCode": country_code,
            "dialingCode": dialing_code,
            "phoneNumber": phone_number,
            "requestId": json_data["requestId"],
            "token": otp,
        }

        headers = {
            "content-type": "application/json; charset=UTF-8",
            "accept-encoding": "gzip",
            "user-agent": "Truecaller/11.75.5 (Android;10)",
            "clientsecret": "lvc22mp3l1sfv6ujg83rd17btt",
        }

        url = "https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp"

        response = requests.post(url, json=post_data, headers=headers)
        return response.json()

    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError("Invalid phone number.")


def search(phone_number: str, country_code: str, installation_id: str) -> Dict[str, any]:
    """
    Search for a phone number using Truecaller API.

    Args:
        phone_number (str): The phone number to search.
        country_code (str): The country code of the phone number.
        installation_id (str): The installation ID for authorization.

    Returns:
        dict: The search result containing information about the phone number.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    phone_number = parse_phone_number(phone_number, country_code)
    significant_number = phone_number.national_number

    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "Authorization": f"Bearer {installation_id}"
    }
    params = {
        "q": str(significant_number),
        "countryCode": phone_number.country_code,
        "type": 4,
        "locAddr": "",
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json"
    }
    response = requests.get(
        "https://search5-noneu.truecaller.com/v2/search", params=params, headers=headers)

    response_data = response.json()
    return response_data


def bulk_search(phone_numbers: List[str], country_code: str, installation_id: str) -> Dict[str, any]:
    """
    Perform bulk search for a list of phone numbers using Truecaller API.

    Args:
        phone_numbers (List[str]): The list of phone numbers to search.
        country_code (str): The country code of the phone numbers.
        installation_id (str): The installation ID for authorization.

    Returns:
        dict: The bulk search result containing information about the phone numbers.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "Authorization": f"Bearer {installation_id}"
    }
    params = {
        "q": phone_numbers,
        "countryCode": country_code,
        "type": 14,
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json"
    }
    response = requests.get(
        "https://search5-noneu.truecaller.com/v2/bulk", params=params, headers=headers)

    response_data = response.json()
    return response_data

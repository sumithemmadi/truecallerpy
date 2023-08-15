import httpx
import random
from phonenumbers import parse as parse_phone_number
from phonenumbers.phonenumberutil import region_code_for_country_code
from .data.phones_list import get_random_device


async def generate_random_string(length: int) -> str:
    """
    Generate a random string of the given length.

    Args:
        length (int): The length of the random string.

    Returns:
        str: The generated random string.
    """
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(characters) for _ in range(length))


async def login(phone_number: str) -> dict:
    """
    Login to Truecaller.

    Args:
        phone_number (str): Phone number in international format.

    Returns:
        dict: The login response containing the requestId used for OTP verification.
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
                "deviceId": await generate_random_string(16),
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
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(post_url, json=data, headers=headers)
        
        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "data": response.json()
        }
    except httpx.HTTPError as exc:
        error_message = "An HTTP error occurred: " + str(exc)
        return {
            "status_code": exc.response.status_code if hasattr(exc, "response") else None,
            "error": "HTTP Error",
            "message": error_message
        }

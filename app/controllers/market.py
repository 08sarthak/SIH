from app.helpers import api_helpers
from typing import *


async def display_market_trends():
    http_method = "GET"
    api_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
    Format = "format=json"
    access_token = "579b464db66ec23bdd000001b4e6b405f9e145584bff0a3824f781e5"
    result = api_helpers.execute_api(http_method,api_URL,Format,access_token)
    return result


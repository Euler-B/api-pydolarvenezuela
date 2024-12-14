import requests
from typing import Literal, Optional
from curl_cffi import requests as cffi

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'
}

HEADERS_GRAPHQL = {
    "accept": "*/*",
    "accept-language": "es-ES,es;q=0.7",
    "apollographql-client-name": "web",
    "apollographql-client-version": "1.0.0",
    "content-type": "application/json",
}

DATA_GRAPHQL = {
    "operationName": "getCountryConversions",
    "variables": {
        "countryCode": "VE"
    },
    "query": """
    query getCountryConversions($countryCode: String!) {
      getCountryConversions(payload: {countryCode: $countryCode}) {
        _id
        baseCurrency {
          code
          decimalDigits
          name
          rounding
          symbol
          symbolNative
          __typename
        }
        country {
          code
          dial_code
          flag
          name
          __typename
        }
        conversionRates {
          baseValue
          official
          principal
          rateCurrency {
            code
            decimalDigits
            name
            rounding
            symbol
            symbolNative
            __typename
          }
          rateValue
          type
          __typename
        }
        dateBcvFees
        dateParalelo
        dateBcv
        createdAt
        __typename
      }
    }
    """
}

def request(
        method: Literal["GET", "POST"], 
        page_url: tuple, 
        params: Optional[dict] = None,
        headers: Optional[dict] = USER_AGENT,
        verify: Optional[bool] = True, 
        data: Optional[dict] = None,
        json: Optional[dict] = None) -> bytes:
    page, url = page_url

    headers = headers if page != "Al Cambio" else HEADERS_GRAPHQL
    json = json if page != "Al Cambio" else DATA_GRAPHQL

    if page in ["Al Cambio", "Cripto Dolar"]:
        response = cffi.request(method, url, headers=headers, params=params, json=json, data=data, impersonate='chrome110', timeout=10.0, verify=verify)
    else:
        if not verify:
            requests.packages.urllib3.disable_warnings()
        
        response = requests.request(method, url, headers=headers, params=params, json=json, data=data, timeout=10.0, verify=verify)

    response.raise_for_status()
    return response.content

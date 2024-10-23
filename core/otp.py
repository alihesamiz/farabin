import requests
import json


def main(phone_number, otp):
    print(phone_number)
    print(otp)
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
        "code": "0vdhr2n9d5b2j78",
        "sender": "+983000505",
        "recipient": phone_number,
        "variable": {
            "verification-code": int(otp)
        }
    })
    headers = {
        'apikey': 'BXb2ovSeYtiAbfVT26gEb50Dmix_-nhAAQRp2v5yfXs=',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

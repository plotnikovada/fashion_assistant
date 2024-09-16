import time
import requests
import json


while True:
    body = {
        "yandexPassportOauthToken": "y0_AgAAAAAqzZeGAATuwQAAAAEAlbhDAABcUpNXr0FHDIWihJ2CDt3Bb8khgQ"
    }
    resp = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                     json = body)
    IAM_TOKEN = json.loads(resp.text)["iamToken"]
    with open("IAM_TOKEN.txt", "w") as f:
        f.write(IAM_TOKEN)
    time.sleep(60*60*8)

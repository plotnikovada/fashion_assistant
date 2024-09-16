import requests
import json
import os

def translate(text):
    with open("IAM_TOKEN.txt", "r") as f:
        IAM_TOKEN = f.readline()
    folder_id = 'b1gpckadibkg1s8qkpgg'
    target_language = 'ru'
    texts = [text]

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    print(response.text)
    return json.loads(response.text)["translations"][0]['text']

print(translate("a pink dress with long train"))

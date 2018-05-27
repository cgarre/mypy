import requests
import json

headers = {
    'Authorization' : 'Bearer 107-bUqUuWzXNlTzkjeu0urxg',
    'Content-type': 'application/json'
}
url = "https://www.yammer.com/api/v1/messages.json"
resp = requests.get(url,headers=headers)

if(resp.ok):
    jData = json.loads(resp.content)

    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for key in jData:
        print(key)
else:
    resp.raise_for_status()



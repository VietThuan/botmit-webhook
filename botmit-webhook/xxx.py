import json

import apiai

CLIENT_ACCESS_TOKEN = '7093eea13b024b409f77dd7bc4929662'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    session_id = "12345678"

    request = ai.text_request()

    request.lang = 'de'  # optional, default value equal 'en'

    request.query = "hôm nay có những ai sinh nhật"
    request.session_id = session_id
    userInfo = {
        "name": "userInfo",
        "lifespan": "1000",
        "parameters": {
            "userID": "New-Guid",
            "companyCode": "ApiTest"
        }
    }
    request.contexts.append(userInfo)

    response = request.getresponse()

    print(json.dumps(json.loads(response.read()), indent=4))

main()

import json
import os
import subprocess
import traceback
from urllib.parse import quote
from pprint import pprint


def query(q,ssID):
    #    command = "curl --request GET \
    #  --url 'http://117.6.16.176/botmit/bot_v2?message={}' \
    #  --header 'BranchID: 00000000-0000-0000-0000-000000000000' \
    #  --header 'BranchID-Hrm: 00000000-0000-0000-0000-000000000000' \
    #  --header 'companycode: misajsc' \
    #  --header 'content-type: application/json' \
    #  --header 'UserID: 27B9659B-01BE-4304-9AD4-AFADF024D4C5' \
    #  # --header 'UserID: 8e5fd60e-b93f-4595-8027-b9de55b2de87' \
    #  --header 'gender: 0' \
    #  --header 'token: 6cfcbc64-0dfe-45b1-b860-5a0aef7ac829' \
    #  --data ''"
    command = "curl 'https://api.dialogflow.com/v1/query?v=20170712&query={}&lang=en&sessionId={}&timezone=Asia/Saigon' -H 'Authorization:Bearer 7093eea13b024b409f77dd7bc4929662'"
    str = command.format(quote(q),ssID)
    p = subprocess.Popen(str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    try:
        print(out.decode())
        obj = json.loads(out.decode())  # ['data']

        return obj['result']['fulfillment']['speech']
    except:
        print(out.decode())
        print(traceback.format_exc())


def process_file(file, out):
    import csv
    lines = csv.reader(open(file, newline=''))
    ssID = file[5:-4]
    with open(out, "w") as text_file:
        for v in lines:
            if len(v) == 0 or len(v[0]) == 0:
                continue
            print(v[0])
            v = v[0].strip()

            if v is not None:
                try:
                    ret = query(v,ssID)
                except:
                    ret = traceback.format_exc()
                print("    ==>" + str(ret))
                print("{}\t\t\t{}".format(v, str(ret)), file=text_file)


for file in os.listdir("test"):
    if file.endswith(".txt"):
        out_file = file[0:-4] + "_out.txt"
        process_file(os.path.join("test", file), os.path.join("test", out_file))



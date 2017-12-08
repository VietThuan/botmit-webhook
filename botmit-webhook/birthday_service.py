token = '55F87A13-2416-4D8E-8B42-903FC6C07DD5'

import requests
import json

# url = "https://testapicfo.amis.vn/api/GetBirthdayEmployee"
#
# payload = "{\n  \"Token\": \"55F87A13-2416-4D8E-8B42-903FC6C07DD5\",\n  \"UserID\": \"8E5FD60E-B93F-4595-8027-B9DE55B2DE87\",\n  \"OrganizationUnitID\": \"00000000-0000-0000-0000-000000000000\",\n  \"CompanyCode\": \"misajsc\"\n}"
# headers = {'content-type': 'application/json'}
#
# response = requests.request("POST", url, data=payload, headers=headers)
# import json
# obj=json.loads(response.text)
# list=json.loads(obj['Data'])
# # for v in list:
# #     v['EmployeeId']=v['EmployeeID']
# #     v.pop('EmployeeID')
# print(list[0] )


class BirthdayService:
    def get_list_birthday(self, com_code, user_id, orgid):

        # Goi toi service cua AMIS
        url = "https://testapicfo.amis.vn/api/GetBirthdayEmployee"
        # payload = "{\n  \"Token\": \"" + token + "\",\n  \"UserID\": \"" + user_id +"\",\n  \"OrganizationUnitID\": \"" + orgid + "\",\n  \"CompanyCode\": \""+ com_code +"\"\n}"
        payload = "{\n  \"Token\": \"55F87A13-2416-4D8E-8B42-903FC6C07DD5\",\n  \"UserID\": \"8E5FD60E-B93F-4595-8027-B9DE55B2DE87\",\n  \"OrganizationUnitID\": \"00000000-0000-0000-0000-000000000000\",\n  \"CompanyCode\": \"misajsc\"\n}"

        headers = {'content-type': 'application/json'}
        response = requests.request("POST", url, data=payload, headers=headers)
        obj = json.loads(response.text)
        list = json.loads(obj['Data'])
        # list += list
        print(len(list))
        print(list)

        return list

    def get_lasted_birthday_message(self, com_code, user_id, orgid):

        tmp = 1
        if tmp != 0:
            return 'chúc mừng sinh nhật em! Chúc em luôn mạnh khỏe, hạnh phúc và luôn thành công trong công việc.'
        return

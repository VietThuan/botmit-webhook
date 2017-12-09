import logging

from amis_config import WebhookConfig

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
cfg = WebhookConfig()


class BirthdayService:
    # Goi toi service cua Amis de lay so nguoi sinh nhat trong ngay
    def get_list_birthday(self, com_code, user_id, orgid):
        try:
            response_text = ""
            if __debug__:
                url = "https://testapicfo.amis.vn/api/GetBirthdayEmployee"
                payload = {
                    'Token': cfg.AMIS_TOKEN_SERVICE,
                    'UserID': '8E5FD60E-B93F-4595-8027-B9DE55B2DE87',
                    'OrganizationUnitID': '00000000-0000-0000-0000-000000000000',
                    'CompanyCode': 'misajsc'
                }
            else:
                url = "{}GetBirthdayEmployee".format(cfg.AMIS_URL_SERVICE)
                payload = {
                    'Token': cfg.AMIS_TOKEN_SERVICE,
                    'UserID': user_id,
                    'OrganizationUnitID': orgid,
                    'CompanyCode': com_code
                }

            headers = {'content-type': 'application/json'}

            # Goi toi service cua AMIS
            response = requests.request("POST", url, data =json.dumps(payload), headers=headers)
            response_text = response.text
            obj = json.loads(response.text)
            list = json.loads(obj['Data'])
            return list
        except Exception as ex:
            logging.error("Error when call {} input {} output {} exception: {}".
                          format(url, str(payload), response_text, str(ex)))
            return None # lay loi thi coi nhu la ko co mau truoc do


    def get_lasted_birthday_message(self, com_code, user_id, orgid):

        try:
            response_text = ""
            if __debug__:
                url = "https://testapicfo.amis.vn/api/GetCurrentSMSTemplate"
                payload = {
                    'Token': cfg.AMIS_TOKEN_SERVICE,
                    'UserID': '8E5FD60E-B93F-4595-8027-B9DE55B2DE87',
                    'OrganizationUnitID': '00000000-0000-0000-0000-000000000000',
                    'CompanyCode': 'misajsc'
                }
            else:
                url = "{}GetCurrentSMSTemplate".format(cfg.AMIS_URL_SERVICE)
                payload = {
                    'Token': cfg.AMIS_TOKEN_SERVICE,
                    'UserID': user_id,
                    'OrganizationUnitID': orgid,
                    'CompanyCode': com_code
                }

            headers = {'content-type': 'application/json'}
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            response_text = response.text
            obj = json.loads(response.text)
            if obj['Data'] is not None:
                return obj['Data']['SMSTemplateName']
            else:
                return None

        except Exception as ex:
            logging.error("Error when call {} input {} output {} exception: {}".
                          format(url, str(payload), response_text, str(ex)))
            return None # lay loi thi coi nhu la ko co mau truoc do


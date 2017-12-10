# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import threading
import traceback

from future.standard_library import install_aliases
import json

install_aliases()

import pycommon
import os
from flask import Flask, jsonify
from flask import request
from amis_config import WebhookConfig
from birthday_service import BirthdayService

# Flask app should start in global layout
app = Flask(__name__)

cfg = WebhookConfig()

service = BirthdayService()

#
tra_loi_khong_co_ai_sn = """Thưa {get_customer_prefix_name} hôm nay không có nhân viên nào sinh nhật. {get_customer_prefix_name} có cần em giúp gì nữa không ạ?"""

tra_loi_sinh_nhat_mot_nguoi = """Thưa {get_customer_prefix_name}, hôm nay là sinh nhật anh/chị {name} - {depart}, \
{get_customer_prefix_name} có muốn gửi lời chúc đến nhân viên này không ạ?"""

tra_loi_sinh_nhat_khong_qua_nam_nguoi = """Thưa {get_customer_prefix_name}, hôm nay là sinh nhật {num_employees} nhân viên. \
Đó là: {list_employees}, {get_customer_prefix_name} có muốn gửi lời chúc đến tất cả hay nhân viên nào không ạ?"""

tra_loi_sinh_nhat_tren_nam_nguoi = """Thưa {get_customer_prefix_name}, hôm nay là sinh nhật {num_employees} nhân viên. \
Đó là: {list_employees}. Còn {num_employees_else} nhân viên, {get_customer_prefix_name} có muốn hiển thị hết không ạ?"""

tra_loi_sinh_nhat_so_nguoi_con_lai = """Còn có: {list_employees_else}, {get_customer_prefix_name} có muốn gửi lời chúc \
đến những nhân viên sinh nhật hôm nay không ạ?"""

tra_loi_sinh_nhat_su_dung_mau_tin_truoc_do = """Em có sẵn rất nhiều tin nhắn mẫu. {get_customer_prefix_name} có muốn sử dụng không ạ?"""
tra_loi_sinh_nhat_khong_co_mau_tin_truoc_do = """{get_customer_prefix_name} có muốn sử dụng mẫu tin nhắn {sms_templatename} không ạ?"""


def get_param_user_info(req):
    com_code, user_id, orgid = None, None, None
    for v in req['result']['contexts']:
        if v['name'] == 'userinfo':
            com_code, user_id, orgid = v['parameters']['companyCode'], v['parameters']['userID'], \
                                       v['parameters']['organizationUnitID']

    return com_code, user_id, orgid

# Cho phép gọi event lên cho DF
def invoker_event_intents(session_id, event_name):
    import time
    time.sleep(1)
    s = 'curl \
               -H "Authorization: Bearer {}" \
               "https://api.dialogflow.com/v1/query?v={}&e={}&timezone={}&lang={}&sessionId={}"'
    repaced = s.format(cfg.DF_CLIENT_ACCESS_TOKEN, cfg.DF_API_VERSION,event_name, cfg.DF_API_TIMEZONE, cfg.DF_API_LANG,
                       session_id)
    if __debug__:
        print(pycommon.execute_curl(repaced))
    else:
        pycommon.execute_curl(repaced)

def insert_context_to_DF(contextName, session_id,value):
    import time
    time.sleep(1)
    # headers = {
    #     'Authorization': 'Bearer {}'.format(cfg.DF_CLIENT_ACCESS_TOKEN),
    #     'Content-Type': 'application/json',
    # }
    #
    # params = (
    #     ('sessionId', session_id),
    # )
    # data = {
    #     "name": contextName,
    #     "parameters": "{}".format(json.dumps(value)),
    #     "lifespan":100
    # }
    #
    # # data = '[\n  {\n    lifespan: 3,\n    name: pick-fruit,\n    parameters: {\n      fruit: Kiwi\n    }\n  }\n]'
    # import requests
    # print(requests.post('https://api.dialogflow.com/v1/contexts&sessionId={}'.format(session_id), headers=headers, data=data).content)

    listID = None
    for item in value:
        if listID is None:
            listID = item['EmployeeID']
        else:
            listID = listID + "_" + item['EmployeeID']

    s = 'curl -X POST \
                   "https://api.dialogflow.com/v1/contexts?sessionId={4}" \
                   -H "Authorization: Bearer {0}" \
                   -H "Content-Type: application/json" \
                   -d "[{"lifespan":{1},"name":"{2}","parameters":{"EmployeeID":"{3}"}}]"'

    repaced = pycommon.keymap_replace(s,
                                         {"0": cfg.DF_CLIENT_ACCESS_TOKEN,
                                          "1": 100,
                                          "2":contextName,
                                          "3":listID,
                                          "4":session_id})
    # repaced = s.format(cfg.DF_CLIENT_ACCESS_TOKEN,contextName,json.dumps(value),session_id)

    if __debug__:
        print(pycommon.execute_curl(repaced))
    else:
        pycommon.execute_curl(repaced)


# -------------------------------------------------Handle actions-------------------------------------------------------

# Xu ly action nguoi dung muon goi tin nhan chuc mung sinh nhat cho 1 người
def action_user_want_send_msg(action, req):
    com_code, user_id, orgid = get_param_user_info(req)
    lasted_mesage = service.get_lasted_birthday_message(com_code, user_id, orgid)
    if lasted_mesage is None:
        t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_chua_co_mau_tin"))
        req['result']['fulfillment']['speech'] = tra_loi_sinh_nhat_su_dung_mau_tin_truoc_do

    else:
        t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_co_mau_tin"))
        req['result']['fulfillment']['speech'] = pycommon.keymap_replace(tra_loi_sinh_nhat_su_dung_mau_tin_truoc_do,
                                                                         {"sms_templatename": lasted_mesage})

    t.daemon = True
    t.start()
    return req

# Xử lý action lấy danh sách người có sinh nhật
def action_get_list_employee_bithday(action, req):
    com_code, user_id, orgid = get_param_user_info(req)
    list_birthday = service.get_list_birthday(com_code, user_id, orgid)

    print("Có tất cả {} người sinh nhật!".format(len(list_birthday)))

    if len(list_birthday) == 0:
        req['result']['fulfillment']['speech'] = tra_loi_khong_co_ai_sn

    elif len(list_birthday) == 1:
        req['result']['fulfillment']['data'] = list_birthday
        req['result']['fulfillment']['speech'] = pycommon.keymap_replace(tra_loi_sinh_nhat_mot_nguoi,
                                                                         {"name": list_birthday[0]['FullName'],
                                                                          "depart": list_birthday[0][
                                                                              'OrganizationUnitMapPath']})
    else:
        req['result']['fulfillment']['actions'] = gen_response_with_actions(list_birthday)
        if len(list_birthday) >5:
            t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_sn_nhieuhon5"))
        else:
            t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_sn_khongqua5"))
        t.daemon = True
        t.start()
    #Luu thong tin nguoi sinh nhat vao de su dung khi gui thong tin sinh nhat
    insert_context_to_DF("sn_save_list_emloyees",req['sessionId'],list_birthday)
    # req['result']['contexts'].append({
    #     "name": "sn_save_list_emloyees",
    #     "parameters": "{}".format(json.dumps(list_birthday)),
    #     "lifespan":100
    #
    # })

        # = format(json.dumps(list_birthday))
    return req

#Trường hợp hiện thị nốt những người trong danh sách (> 5)
def action_show_employees_to_end(action, req):
    
    com_code, user_id, orgid = get_param_user_info(req)
    list_birthday = service.get_list_birthday(com_code, user_id, orgid)
    data = []
    data.append(
        {
            "name": "show_birthday",
            "data": "{}".format(json.dumps(list_birthday[5:]))
        }
    )
    data.append(
        {
            "name": "speak",
            "data": {
                "message": "{get_customer_prefix_name} có muốn gửi lời chúc đến những nhân viên sinh nhật hôm nay không ạ?",
                "speak_link": None
            }
        }
    )
    return req

# Todo đang xu ly truong họp gui tin nhan cho nhieu nguoi
# Người dùng muốn gửi lời chúc sinh nhật cho trường hợp nhiều hơn 1 người
def action_user_want_send_msg_to_employees(action, req):
    com_code, user_id, orgid = get_param_user_info(req)
    lasted_mesage = service.get_lasted_birthday_message(com_code, user_id, orgid)
    if lasted_mesage is None:
        t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_chua_co_mau_tin"))
        req['result']['fulfillment']['speech'] = tra_loi_sinh_nhat_su_dung_mau_tin_truoc_do

    else:
        t = threading.Thread(target=invoker_event_intents, args=(req['sessionId'], "event_co_mau_tin"))
        req['result']['fulfillment']['speech'] = pycommon.keymap_replace(tra_loi_sinh_nhat_su_dung_mau_tin_truoc_do,
                                                                         {"sms_templatename": lasted_mesage})

    t.daemon = True
    t.start()
    return req

# Mapping action trong DF với hàm của webhook
action_resolve = {
    "input.lay_danh_sach_nguoi_sinh_nhat": action_get_list_employee_bithday,
    "input.hoi_sinh_nhat_co": action_user_want_send_msg,
    "SN_NHIEU_HON_1NV_CHUC_MUNG_ALL": action_user_want_send_msg,
    "SN_NHIEUHON5.SN_HOI_SINH_NHAT-NhieuHon5-yes": action_show_employees_to_end,
    "SN_NHIEU_HON_1NV_GUI_CHUC-MUNG": action_user_want_send_msg_to_employees
}

# -------------------------------------------------End handle actions---------------------------------------------------
#Tạo câu trả lời cho trường hợp > 1 nhân viên (Cả trường hợp > 5 nv)
def gen_response_with_actions(list_birthday):

    data = []

    data.append({
        "name": "speak",
        "data": {
            "message": pycommon.keymap_replace(
                "Thưa {get_customer_prefix_name}, Hôm nay có {count} nhân viên sinh nhật",
                {"count": len(list_birthday)}),
            "speak_link": None
        }
    })
    data.append(
        {
            "name": "show_birthday",
            "data": "{}".format(json.dumps(list_birthday[:5] if len(list_birthday) > 5 else list_birthday))
        }
    )
    data.append(
        {
            "name": "speak",
            "data": {
                "message": "{get_customer_prefix_name} có muốn em liệt kê nốt không ạ?" if len(list_birthday) > 5 \
                    else "{get_customer_prefix_name} có muốn gửi lời chúc đến những nhân viên sinh nhật hôm nay không ạ?",
                "speak_link": None
            }
        }
    )
    return data


@app.route('/webhook', methods=['POST'])
def webhook():
    import json
    req = request.get_json(silent=True, force=True)

    action = req['result']['action']

    try:
        if action in action_resolve:
            req = action_resolve[action](action, req)
    except:
        print(traceback.format_exc())
    req['result']['fulfillment']['messages'][0]['speech'] = req['result']['fulfillment']['speech']
    print(json.dumps(req['result']['contexts'], indent=4))

    return jsonify(req['result']['fulfillment'])


if __name__ == '__main__':
    port = int(os.getenv('PORT', 10001))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)

import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

def dingding(api_name):
    # 第一步，把timestamp+"\n"+密钥当做签名字符串，使用HmacSHA256算法计算签名，然后进行Base64 encode，最后再把签名参数再进行urlEncode，得到最终的签名（需要使用UTF-8字符集）。
    timestamp = str(round(time.time() * 1000))
    secret = '保密'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)

    # 第二步，把 timestamp和第一步得到的签名值拼接到URL中。
    Webhook_url = "https://oapi.dingtalk.com/robot/send"
    payload = {
        'access_token': '保密',
        'timestamp': timestamp,
        'sign': sign
    }
    print(payload)

    # 第三步，发送消息text类型或者link类型、markdown类型、跳转ActionCard类型
    body = {
        "msgtype": "text",
        "text": {
            "content": "测试内容：%s" % api_name
        },
        "at": {
            "isAtAll": False
        }
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    r = requests.post(Webhook_url, params=payload, headers=headers, json=body)
    print(r.url)
    print(r.text)

app_key = 'X'
app_secret = 'X'
agent_id = 'X'

def get_access():
    """
    获取token
    :return:
    """
    url = "https://oapi.dingtalk.com/gettoken?appkey={0}&appsecret={1}".format(app_key, app_secret)
    jo = json.loads(requests.get(url).text)
    return jo['access_token']


def get_dp(token):
    """
    获取部门列表
    :param token:
    :return:
    """
    url = "https://oapi.dingtalk.com/department/list?access_token=" + token
    # url = "https://oapi.dingtalk.com/topapi/v2/department/get?access_token=" + token
    dp = json.loads(requests.get(url).text)
    return dp['department']


def get_users(token, dept_id):
    """
    获取部门用户userid列表
    :param token:
    :param dept_id:
    :return:
    """
    url = "https://oapi.dingtalk.com/user/getDeptMember?access_token={0}&deptId={1}".format(token, dept_id)
    user_list = json.loads(requests.get(url).text)
    return user_list['userIds']


def get_user_info(token, user_id):
    """
    根据userid获取用户详情
    :param token:
    :param userId:
    :return:
    """
    url = "https://oapi.dingtalk.com/user/get?access_token={0}&userid={1}".format(token, user_id)
    info = json.loads(requests.get(url).text)
    return info

def post_active_card(content, userid):
    token = get_access()
    """
        token, user_id, start_time, end_time, cursor, size
        """
    Webhook_url = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"
    payload = {
        'access_token': token,
    }
    # print(payload)

    # 第三步，发送消息text类型或者link类型、markdown类型、跳转ActionCard类型
    body = {
        "msg": {
                 "msgtype": "action_card",
                 "action_card": {
                 "title": "test",
                 "markdown": content,
                 "btn_orientation": "0",
                 "btn_json_list": [
            {
                "title": "确认",
                "action_url": "https://www.dingtalk.com"
            }
        ]
                 }
        },
        "to_all_user": "false",
        "agent_id": 'X',
        "userid_list": userid
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    info = json.loads(requests.post(Webhook_url, params=payload, headers=headers, json=body).text)
    # print(info)
    return info

if __name__ == '__main__':
    # 使用方法
    # dingding('Hello World')
    token = get_access()
    dp = get_dp(token)
    for d in dp:
        users = get_users(token, d['id'])
        for u in users:
            user_info_dict = get_user_info(token, u)









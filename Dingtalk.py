import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

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

dingding('Hello World')




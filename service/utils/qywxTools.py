# -*- encoding:utf-8 -*-
import os
import time
import requests
import json
from requests_toolbelt import MultipartEncoder
import yaml
from xml.dom.minidom import parseString
from Crypto.Cipher import AES
import base64,hashlib, json
from config.qywx import ENCODINGAESKEY, TOKEN, CROP_ID, AGENT_ID, SECRET

class Push:
    def __init__(self):
        self.agentid = AGENT_ID
        self.corpsecret = SECRET
        self.corpid = CROP_ID
        self.EncodingAESKey = ENCODINGAESKEY

        self.access_token, self.expires_in, self.get_time = self.init_access_token()


    def init_access_token(self):
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=self.corpid, corpsecret=self.corpsecret))
        data = json.loads(response.text)
        access_token = data['access_token']
        expires_in = data['expires_in']
        return access_token, expires_in, time.time()

    def updata_access_token(self):
        # 检查token有没有过期
        time_diff = time.time() - self.get_time
        if time_diff > self.expires_in:
            response = requests.get(
                "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                    corpid=self.corpid, corpsecret=self.corpsecret))
            data = json.loads(response.text)
            access_token = data['access_token']
            expires_in = data['expires_in']
            self.access_token, self.expires_in, self.get_time = access_token, expires_in, time.time()

        # 上传临时文件素材接口，图片也可使用此接口，20M上限
    def post_file(self, filepath, filename):
        response = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                corpid=self.corpid, corpsecret=self.corpsecret))
        data = json.loads(response.text)
        access_token = data['access_token']

        post_file_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file".format(
            access_token=access_token)

        m = MultipartEncoder(
            fields={'file': (filename, open(rf'{filepath}/{filename}', 'rb'), 'multipart/form-data')},
        )
        os.remove(rf'{filepath}/{filename}')

        r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
        js = json.loads(r.text)
        # print("upload " + js['errmsg'])
        if js['errmsg'] != 'ok':
            return None
        return js['media_id']

    # 向应用发送图片接口，_message为上传临时素材后返回的media_id
    def send_img(self, filepath, filename, useridlist=['name1|name2']):
        _message = self.post_file(filepath, filename)
        useridstr = "|".join(useridlist)
        self.updata_access_token()

        json_dict = {
            "touser": useridstr,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": _message,
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.access_token), data=json_str)
        # print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'

    # 向应用发送文字消息接口，_message为字符串
    def send_text(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)  # userid 在企业微信-通讯录-成员-账号
        self.updata_access_token()
        json_dict = {
            "touser": useridstr,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": _message
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.access_token), data=json_str)
        # print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'

def get_msg(msg):
    # 解析接收到的消息
    msg_dict = {}

    doc = parseString(msg)
    collection = doc.documentElement
    name_xml = collection.getElementsByTagName("FromUserName")
    msg_dict["userName"] = name_xml[0].childNodes[0].data

    time_xml = collection.getElementsByTagName("CreateTime")
    msg_dict["sendTime"] = time_xml[0].childNodes[0].data

    type_xml = collection.getElementsByTagName("MsgType")
    msg_type = type_xml[0].childNodes[0].data
    msg_dict["msgType"] = msg_type

    if msg_type == "text":
        msg_xml = collection.getElementsByTagName("Content")
    elif msg_type == "image":
        msg_xml = collection.getElementsByTagName("PicUrl")
    elif msg_type == "voice":
        msg_xml = collection.getElementsByTagName("Format")
    # 位置消息、视频消息略过
    elif msg_type == "link":
        msg_xml = collection.getElementsByTagName("Url")
    else: msg_xml = None

    if msg_xml: msg_dict["message"] = msg_xml[0].childNodes[0].data

    return msg_dict

# 检查base64编码后数据位数是否正确
def check_base64_len(base64_str):
    len_remainder = 4 - (len(base64_str) % 4)
    if len_remainder == 0:
        return base64_str
    else:
        for temp in range(0,len_remainder):
            base64_str = base64_str + "="
        return base64_str
# 解密并提取消息正文
def msg_base64_decrypt(ciphertext_base64,key_base64):
    # 处理密文、密钥和iv
    ciphertext_bytes = base64.b64decode(check_base64_len(ciphertext_base64))
    key_bytes = base64.b64decode(check_base64_len(key_base64))
    iv_bytes = key_bytes[:16]

    # 解密
    decr = AES.new(key_bytes,AES.MODE_CBC,iv_bytes)
    plaintext_bytes = decr.decrypt(ciphertext_bytes)

    # 截取数据，判断消息正文字节数
    msg_len_bytes = plaintext_bytes[16:20]
    msg_len = int.from_bytes(msg_len_bytes,byteorder='big', signed=False)

    # 根据消息正文字节数截取消息正文，并转为字符串格式
    msg_bytes = plaintext_bytes[20:20+msg_len]
    msg = str(msg_bytes,encoding='utf-8')

    return msg

# 消息体签名校验
def check_msg_signature(msg_signature,token,timestamp,nonce,echostr):
    # 使用sort()从小到大排序[].sort()是在原地址改值的，所以如果使用li_s = li.sort()，li_s是空的，li的值变为排序后的值]
    li = [token,timestamp,nonce,echostr]
    li.sort()
    # 将排序结果拼接
    li_str = li[0]+li[1]+li[2]+li[3]

    # 计算SHA-1值
    sha1 = hashlib.sha1()
    # update()要指定加密字符串字符代码，不然要报错：
    # "Unicode-objects must be encoded before hashing"
    sha1.update(li_str.encode("utf8"))
    sha1_result = sha1.hexdigest()

    # 比较并返回比较结果
    if sha1_result == msg_signature:
        return True
    else:
        return False

def checkURL(msg_signature, timestamp, nonce, echostr):
    EncodingAESKey = ENCODINGAESKEY
    token = TOKEN

    # 获取消息体签名校验结果
    check_result = check_msg_signature(msg_signature, token, timestamp, nonce, echostr)
    if check_result:
        decrypt_result = msg_base64_decrypt(echostr, EncodingAESKey)
        return int(decrypt_result)
    else:
        return ""
from fastapi import APIRouter, Request
from service.utils.CheckURL import checkURL
from service.utils.WXBizMsgCrypt3 import WXBizMsgCrypt
from pydantic import BaseModel
from config.qywx import TOKEN, ENCODINGAESKEY, CROP_ID

qywechat = APIRouter()

class Item(BaseModel):
    data: str

@qywechat.get("/qywx", summary="企业微信的验证接口", description="用于验证服务器有效性",
          response_description= "约定的验证密钥",)
async def vertify(msg_signature: str, timestamp: str, nonce: str, echostr: str):

    return checkURL(msg_signature, timestamp, nonce, echostr)

@qywechat.post("/qywx")
async def reply(msg_signature: str, timestamp: str, nonce: str, item: Item):

    data = item.data.encode('utf-8')
    print(data)
    ret, sMsg = WXBizMsgCrypt(TOKEN, ENCODINGAESKEY, CROP_ID).DecryptMsg(data,msg_signature,timestamp, nonce)

    return {"shop": "bed"}
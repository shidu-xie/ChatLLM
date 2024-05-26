from fastapi import APIRouter, Request
from service.utils.CheckURL import checkURL

qywechat = APIRouter()


@qywechat.get("/qywx", summary="企业微信的验证接口", description="用于验证服务器有效性",
          response_description= "约定的验证密钥",)
async def vertify(msg_signature: str, timestamp: str, nonce: str, echostr: str):

    return checkURL(msg_signature, timestamp, nonce, echostr)


@qywechat.post("/qywx")
def shop_food():
    return {"shop": "bed"}
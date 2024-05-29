from fastapi import APIRouter, Request, Body
from service.utils.WXBizMsgCrypt3 import WXBizMsgCrypt
from service.utils.qywxTools import get_msg, checkURL
from pydantic import BaseModel
from config.qywx import TOKEN, ENCODINGAESKEY, CROP_ID
from service.bot.ChatBot import chatBot
import threading

user_model = {}
mybot = chatBot()

qywechat = APIRouter()

class Item(BaseModel):
    data: bytes

@qywechat.get("/qywx", summary="企业微信的验证接口", description="用于验证服务器有效性",
          response_description= "约定的验证密钥",)
async def vertify(msg_signature: str, timestamp: str, nonce: str, echostr: str):

    return checkURL(msg_signature, timestamp, nonce, echostr)

@qywechat.post("/qywx")
async def reply(msg_signature: str, timestamp: str, nonce: str, data: bytes = Body()):
    data = data.decode('utf-8')
    ret, sMsg = WXBizMsgCrypt(TOKEN, ENCODINGAESKEY, CROP_ID).DecryptMsg(data,msg_signature,timestamp, nonce)
    # 接收消息失败
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        return ("failed")

    msg_info = get_msg(sMsg)
    user_llm_type = user_model.get(msg_info["name"], "chat")

    # 创建子线程，通过子线程生成回答并回复给用户
    sub_thread = threading.Thread(target=mybot.reply, args=(msg_info, user_llm_type,))
    sub_thread.start()

    return ""


# 该函数来查看请求的内容
# async def get_headers(request: Request):
#     headers = request.headers
#     body = await request.body()
#     # 在这里可以对请求体进行处理
#     print(f"请求体内容：{body}")
#     print(type(body))
#     print(request.body())
#     return headers
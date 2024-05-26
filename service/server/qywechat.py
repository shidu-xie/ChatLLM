from fastapi import APIRouter, Request
from service.utils.CheckURL import checkURL

qywechat = APIRouter()


@qywechat.get("/qywx", summary="企业微信的验证接口", description="用于验证服务器有效性",
          response_description= "约定的验证密钥",)
async def vertify(request: Request):
    return checkURL(request)


@qywechat.post("/qywx")
def shop_food():
    return {"shop": "bed"}
from fastapi import APIRouter, Request
from service.utils.CheckURL import checkURL

qywx = APIRouter()


@qywx.get("/qywx")
def vertify(request: Request):
    print(checkURL(request))
    return checkURL(request)


@qywx.post("/qywx")
def shop_food():
    return {"shop": "bed"}
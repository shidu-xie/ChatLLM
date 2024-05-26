from typing import Union

from fastapi import FastAPI
import uvicorn
import sys
SERVICE_PATH = "/root/ChatLLM"
# SERVICE_PATH = "D:\projects\ChatLLM\ChatLLM"
sys.path.append(SERVICE_PATH)
from service.server.qywechat import qywechat


app = FastAPI()

app.include_router(qywechat, prefix="", tags=["企业微信接口", ])


if __name__ == '__main__':
    uvicorn.run("chatllm:app", host="0.0.0.0", port=7777, reload=True)


from typing import Union

from fastapi import FastAPI
import uvicorn

from server import qywx

app = FastAPI()

app.include_router(qywx, prefix="", tags=["企业微信接口", ])


if __name__ == '__main__':
    uvicorn.run("chatllm:app", host="0.0.0.0", port=7777, reload=True)


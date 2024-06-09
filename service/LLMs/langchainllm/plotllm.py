import random
from http import HTTPStatus
import dashscope
from dashscope import Generation
#
dashscope.api_key = "sk-7af7ba01a1c14dc5b62a8d1d429ddf87"

def call_with_messages():
    messages = [{'role': 'system',
                 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '我哥欠我10000块钱，给我生成起诉书。'}]
    response = dashscope.Generation.call(
        "farui-plus",
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response.output.choices[0].message["content"])
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()


# from langchain_openai import ChatOpenAI
# import os
#
# def get_response():
#     llm = ChatOpenAI(
#         api_key="sk-7af7ba01a1c14dc5b62a8d1d429ddf87", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", # 填写DashScope base_url
#         model="farui-plus"
#         )
#     messages = [
#         {"role":"system","content":"You are a helpful assistant."},
#         {"role":"user","content":"我哥欠我10000块钱，给我生成起诉书。"}
#     ]
#     response = llm.invoke(messages)
#     print(response.json(ensure_ascii=False))
#
# if __name__ == "__main__":
#     get_response()

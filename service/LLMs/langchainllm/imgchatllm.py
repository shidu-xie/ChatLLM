from openai import OpenAI
import os
from collections import defaultdict, deque

class ImageChatLLM:
    def __init__(self, APIKEY):

        self.client = OpenAI(
            api_key=APIKEY,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
        )
        # 存储用户的聊天记录
        self.memory = defaultdict(list)
        # 存储用户发送的图片
        self.user_url = defaultdict(deque(maxlen=5))

        self.system = [{'role': 'system',
                       "content": [{
                           "type": "text",
                           "text": "你是一个聪明的小助手，能够准确的认识图片，识别图片的内容。请用你的聪明才智帮助其他人吧"}]}]

    def reply(self, userid, content):

        if len(self.user_url[userid]) == 0 and len(self.memory[userid]) == 0:
            return "请先发送图片，再提问吧"

        while len(self.user_url[userid]) > 0:
            self.memory[userid].append({"role": "user","content": [
                {"type": "image_url",
                 "image_url": {"url": self.user_url[userid].get()}},
            ]})
        self.memory[userid].append({"role": "user", "content": [
            {"type": "text", "text": content}
        ]})

        completion = self.client.chat.completions.create(model="qwen-plus", messages= self.system + self.memory[userid])

        result = completion.choices[0].message.content[0]["text"]

        self.memory[userid].append({"role": "assistant", "content": [
            {"type": "text", "text": content}
        ]})

        self.delete_memory(userid)
        return result

    def delete_memory(self, user):
        if len(self.memory[user]) > 10:
            for index, dialogo in enumerate(self.memory[user]):
                if dialogo["role"] == "assistant":
                    break
            self.memory[user] = [] if index >= 8 else self.memory[user][index + 1:]
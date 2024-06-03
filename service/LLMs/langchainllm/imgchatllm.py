from openai import OpenAI
import os
from collections import defaultdict
os.environ["OPENAI_API_KEY"] = "sk-7af7ba01a1c14dc5b62a8d1d429ddf87"




class ImageChatLLM:
    def __init__(self, APIKEY):

        self.client = OpenAI(
            api_key=APIKEY,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
        )
        # 存储用户的聊天记录
        self.memory = defaultdict(list)

        self.system = [{"role":"system",
                        "content": "You are a very smart assistant, capable of accurately understanding images. Please use your intelligence to help those in need."}]

    def reply(self, userid, content):

        self.memory[userid].append({"role": "user","content": content})


        completion = self.client.chat.completions.create(model="qwen-plus", messages= self.system + self.memory[userid])

        result = completion.model_dump_json().choices[0].message.content

        self.memory[userid].append({"role":"assistant", "content":result})

        self.delete_memory(userid)
        return result

    def delete_memory(self, user):
        if len(self.memory[user]) > 10:
            for index, dialogo in enumerate(self.memory[user]):
                if dialogo["role"] == "assistant":
                    break
            self.memory[user] = [] if index >= 8 else self.memory[user][index + 1:]
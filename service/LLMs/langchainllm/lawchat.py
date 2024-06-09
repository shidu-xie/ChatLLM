from openai import OpenAI
from collections import defaultdict, deque
from http import HTTPStatus
import dashscope

class LawChatLLM:
    def __init__(self):

        # 存储用户的聊天记录
        self.memory = defaultdict(list)

        self.system = [{'role': 'system',
                       "content": "你是一个从业多年的资深法律专家，拥有非常丰富且专业的法律知识，请利用你的知识帮助用户，为用户答疑解惑。"}]

    def get_reply(self, prompt, APIKEY):

        dashscope.api_key = APIKEY

        response = dashscope.Generation.call(
            "farui-plus",
            messages=prompt,
            result_format='message',  # set the result to be "message" format.
        )
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message["content"]
        else:
            return 'Failed, status_code: %s, code: %s, message: %s' % (response.status_code, response.code, response.message)

    def reply(self, userid, content, APIKEY):

        self.memory[userid].append({"role": "user", "content":content})

        res = self.get_reply(self.system + self.memory[userid], APIKEY)

        self.memory[userid].append({"role": "assistant", "content": [
            {"type": "text", "text": content}
        ]})

        self.delete_memory(userid)
        return res

    def delete_memory(self, user):
        if len(self.memory[user]) > 10:
            for index, dialogo in enumerate(self.memory[user]):
                if dialogo["role"] == "assistant":
                    break
            self.memory[user] = [] if index >= 8 else self.memory[user][index + 1:]
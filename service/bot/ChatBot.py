from service.utils.qywxTools import Push
from service.LLMs.langchainllm.chatllm import ChatLLM
from config.apiconfig import ZHIPU_APIKEY
from random import choice
import threading
import os

class chatBot:
    def __init__(self):
        self.chatLLMS = [ChatLLM(x) for x in ZHIPU_APIKEY]

        self.app = Push()

    def reply(self, msg_info, llm_type):

        if msg_info["msgType"] == "text":
            if llm_type == "chat":
                result = choice(self.chatLLMS).reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
        else:
            pass

        # if llm_type == "chat"
        #
        # res = self.bot.reply(name, msg)
        # png_ = f'../temp/{thread_id}.png'
        # if os.path.exists(png_):
        #     self.app.send_img('../temp', f'{thread_id}.png', [name])
        # else:
        #     if "```" in res: res = res.replace("```", '')
        #     print(res)
        #     self.app.send_text(res, [name])

# print(type("nihao") == str)
from service.utils.qywxTools import Push
from service.LLMs.langchainllm.chatllm import zhipuChatLLM, aliChatLLM
from service.LLMs.langchainllm.text2pic import Text2PicLLM

from config.apiconfig import ZHIPU_APIKEY, Ali_APIKEY
from random import choice
import threading
import os

class chatBot:
    def __init__(self):
        self.zhipuchatLLMS = [zhipuChatLLM(x) for x in ZHIPU_APIKEY]
        self.alichatLLMS = [aliChatLLM(x) for x in Ali_APIKEY]

        self.text2picLLM = Text2PicLLM(Ali_APIKEY[0])

        self.app = Push()

        self.user_model = {}
        self.user_url = {}
        self.user_docs = {}

    def reply(self, msg_info):

        user_llm_type = self.user_model.get(msg_info["userName"], "alichat")

        if msg_info["msgType"] == "text":
            if msg_info["message"] == "切换模型":
                self.app.send_text("输入以下指令切换模型：\n1、“智谱”切换智谱清言聊天模型\n2、“通义”切换通义千问聊天模型\n"
                                   "3、“画图”切换文生图模型\n4、“图解”切换图文对话模型\n5、“文档”切换文档对话模型", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "画图模型":
                self.user_model[msg_info["userName"]] = "plot"
                self.app.send_text("已切换到画图模型，开始画画吧！\n如输入“帮我画一只喜羊羊”", [msg_info["userName"]])
                return None

            if user_llm_type == "alichat":
                result = choice(self.alichatLLMS).reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "zhipuchat":
                result = choice(self.zhipuchatLLMS).reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "text2pic":
                result = self.text2picLLM.reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "imgchat":
                pass

        elif msg_info["msgType"] == "image":
            if user_llm_type == "text2pic":
                # 存储url到对话记忆中
                self.text2picLLM.memory[msg_info["userName"]].append({"role":"user", "content":msg_info["message"]})
                return None
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
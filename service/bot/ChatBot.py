from service.utils.qywxTools import Push
from service.LLMs.langchainllm.chatllm import zhipuChatLLM, aliChatLLM
from service.LLMs.langchainllm.imgchatllm import ImageChatLLM
from service.LLMs.langchainllm.text2img import simple_call
from service.LLMs.langchainllm.lawchat import LawChatLLM
from config.apiconfig import ZHIPU_APIKEY, Ali_APIKEY, FIGURE_PATH
from random import choice
import threading
import os
from collections import defaultdict, deque

class chatBot:
    def __init__(self):
        self.zhipuchatLLMS = [zhipuChatLLM(x) for x in ZHIPU_APIKEY]
        self.alichatLLMS = [aliChatLLM(x) for x in Ali_APIKEY]

        self.imagechatLLM = ImageChatLLM(Ali_APIKEY[0])

        self.lawchatLLM = LawChatLLM()

        self.app = Push()

        self.user_model = {}
        self.user_docs = {}

    def reply(self, msg_info):

        user_llm_type = self.user_model.get(msg_info["userName"], "alichat")
        print(msg_info["message"])
        if msg_info["msgType"] == "text":
            if msg_info["message"] == "切换模型":
                self.app.send_text("输入以下指令切换模型：\n1、“智谱”切换智谱清言聊天模型\n2、“通义”切换通义千问聊天模型\n"
                                   "3、“画图”切换文生图模型\n4、“图解”切换图文对话模型\n5、“文档”切换文档对话模型"
                                   "\n6、“法律”切换法律大模型", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "智谱":
                self.user_model[msg_info["userName"]] = "zhipuchat"
                self.app.send_text("已切换到智谱聊天模型，开始聊天吧！\n如输入“喜羊羊是什么羊”", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "通义":
                self.user_model[msg_info["userName"]] = "alichat"
                self.app.send_text("已切换到阿里通义千问聊天模型，开始聊天吧！\n如输入“喜羊羊是什么羊”", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "画图":
                self.user_model[msg_info["userName"]] = "text2pic"
                self.app.send_text("已切换到画图模型，开始画画吧！\n如输入“帮我画一只喜羊羊”", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "图解":
                self.user_model[msg_info["userName"]] = "imgchat"
                self.app.send_text("已切换到图文对话模型，开始聊天吧！\n请先发送图片吧", [msg_info["userName"]])
                return None
            elif msg_info["message"] == "法律":
                self.user_model[msg_info["userName"]] = "lawchat"
                self.app.send_text("已切换到法律大模型，有什么问题都可以提问哟", [msg_info["userName"]])
                return None


            if user_llm_type == "alichat":
                result = choice(self.alichatLLMS).reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "zhipuchat":
                result = choice(self.zhipuchatLLMS).reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "text2pic":
                self.app.send_text("画图需要一点时间（约30s），请稍等", [msg_info["userName"]])
                res = simple_call(msg_info["message"], choice(Ali_APIKEY), msg_info["userName"])
                if res == "Finish":
                    self.app.send_img(FIGURE_PATH, f"{msg_info['userName']}.png", [msg_info["userName"]])
                else:
                    self.app.send_text(res, [msg_info["userName"]])

            elif user_llm_type == "imgchat":
                result = self.imagechatLLM.reply(msg_info["userName"], msg_info["message"])
                self.app.send_text(result, [msg_info["userName"]])
            elif user_llm_type == "lawchat":
                result = self.lawchatLLM.reply(msg_info["userName"], msg_info["message"], choice(Ali_APIKEY))
                self.app.send_text(result, [msg_info["userName"]])

        elif msg_info["msgType"] == "image":
            if user_llm_type == "imgchat":
                # 存储url到缓存中
                self.imagechatLLM.user_url[msg_info["userName"]].append(msg_info["message"])
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
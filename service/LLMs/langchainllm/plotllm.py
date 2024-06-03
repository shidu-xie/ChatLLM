from zhipuai import ZhipuAI
from langchain_community.llms import Tongyi
# llm = Tongyi()
# llm.invoke("hello")
#
# client = ZhipuAI(api_key="2080cdf67b80167d3951876f2ac750cd.rJTLus5x9J3JhJzR")  # 请填写您自己的APIKey
#
# response = client.images.generations(
#     model="cogview-3",  # 填写需要调用的模型名称
#     prompt="一只可爱的小猫咪",
# )
#
# print(response.data[0].url)
# import os
#
# os.environ["DASHSCOPE_API_KEY"] = "sk-7af7ba01a1c14dc5b62a8d1d429ddf87"
# from langchain_community.llms import Tongyi
# LLM = Tongyi(model_name="qwen-plus", verbose=True)
# print(LLM.model_name)
# print(LLM.invoke("你是什么时候发布的？请具体回答。"))
# from langchain_openai import ChatOpenAI
# messages= [
#             {
#               "role": "user",
#               "content": [
#                 {
#                   "type": "text",
#                   "text": "这是什么"
#                 },
#                 {
#                   "type": "image_url",
#                   "image_url": {
#                     "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
#                   }
#                 }
#               ]
#             }
#           ]
# llm =ChatOpenAI(
#     # temperature=0.95,
#     model="qwen-vl-plus",
#     openai_api_key="sk-7af7ba01a1c14dc5b62a8d1d429ddf87",
#     openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1"
#                 )
#
# print(llm.invoke(messages))


from openai import OpenAI
import os
# os.environ["OPENAI_API_KEY"] = "sk-7af7ba01a1c14dc5b62a8d1d429ddf87"
def get_response():
    client = OpenAI(
        api_key="sk-7af7ba01a1c14dc5b62a8d1d429ddf87",  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages= [{"role":"system",
                        "content": "You are a very smart assistant, capable of accurately understanding images. Please use your intelligence to help those in need."},
            {
              "role": "user",
              "content": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
           {
               "role": "user",
               "content": "这是什么"}

          ],
        top_p=0.8,
)
    print(completion.choices[0].message.content)

if __name__ == '__main__':
    get_response()
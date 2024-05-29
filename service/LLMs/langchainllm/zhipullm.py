from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent, ConversationalAgent, AgentExecutor
from langchain_openai import ChatOpenAI
import langchain
from langchain.chains import LLMChain
from redis import Redis
from langchain_community.cache import RedisCache
from langchain_community.chat_message_histories import RedisChatMessageHistory
from random import choice
import yaml
from service.LLMs.tools import exchange
import threading

# langchain.debug = True
langchain.agent_cache = RedisCache(redis_=Redis())


class ChatBot:
    def __init__(self):

        self.tools = [exchange()]
        self.llm =ChatOpenAI(
            temperature=0.95,
            model="glm-4",
            openai_api_key="d72b538cc671dbcee294ce0777084e1e.zfqkyFuCVL0F2ZVi",
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
                        )
        self.agent = self.get_agent()

    def reply(self, userid, content):
        message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0", ttl=600, session_id=userid
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=5
        )

        agent_chain = AgentExecutor(
            agent=self.agent, tools=self.tools, verbose=True, memory=memory, max_iterations=4,
            handle_parsing_errors=True
        )

        return agent_chain.invoke(input=content)

    def get_agent(self):
        prefix = """Assistant is a large language model (GLM4) trained by ZhiPuAI.

        Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics, especially skilled in financial matters. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

        Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

        Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics, especially skilled in financial matters. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

        TOOLS:
        ------
        (For real-time issues in the financial field, Assistant would use tools each time to ensure the accuracy of the responses.)

        Assistant has access to the following tools:"""

        FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

        ```
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ```

        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

        ```
        Thought: Do I need to use a tool? No
        AI: [your response here]
        ```"""

        suffix = """Begin!
        Please answer in Chinese!

        Previous conversation history:
        {chat_history}

        New input: {input}
        {agent_scratchpad}"""

        prompt = ConversationalAgent.create_prompt(
            self.tools,
            prefix=prefix,
            suffix=suffix,
            format_instructions=FORMAT_INSTRUCTIONS,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        agent = ConversationalAgent(llm_chain=llm_chain, tools=self.tools, verbose=True)
        return agent
import time
start = time.time()
bot = ChatBot()
print(time.time() - start)
print(bot.reply('222', '你好'))
print(time.time() - start)
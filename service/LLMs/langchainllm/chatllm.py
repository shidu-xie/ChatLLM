from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory

class ChatLLM:

    TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{chat_history}
Friend: {input}
AI Assistant:"""

    PROMPT = PromptTemplate(input_variables=["history", "input"], template=TEMPLATE)

    def __init__(self, APIKEY: str):

        self.llm = ChatOpenAI(
            temperature=0.95,
            model="glm-4",
            openai_api_key=APIKEY,
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
        )

    def reply(self, userid, content):

        message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0", ttl=600, session_id=f'{userid}_chat'
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=5, ai_prefix="AI Assistant", human_prefix="Friend"
        )

        conversation = ConversationChain(
            prompt=ChatLLM.PROMPT,
            llm=self.llm,
            verbose=True,
            memory=memory,
        )

        return conversation.invoke(content)["response"]



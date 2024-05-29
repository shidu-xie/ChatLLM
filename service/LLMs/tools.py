from langchain.tools import BaseTool

class exchange(BaseTool):
    name = "exchange llm"
    description = ("use this tool when you want to exchange model.")

    def _run(self):
        return "已切换至GPT模型"
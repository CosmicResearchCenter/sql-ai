from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam,ChatCompletionToolChoiceOptionParam
# import openai
from typing import List,Iterable
import sys
# sys.path.append('..')
from app.config.config import OPENAI_API_KEY,OPENAI_BASE_URL,LLM_MODEL
from app.schemas.sql import SQLAnswer,SQLAnswes
from typing import Union, Generator,AsyncGenerator

class OpenAILLM:
    def __init__(self, api_key: str=OPENAI_API_KEY,base_url:str=OPENAI_BASE_URL,model:str=LLM_MODEL) -> None:
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.messages: List[Iterable[dict]] = []
        self.model = model

    def setPrompt(self, prompt: str):
        message = {"role": "system", "content": prompt}
        self.messages.append(message)
        
    def addHistory_User(self, content: str):
        message = {"role": "user", "content": content}
        self.messages.append(message)

    def addHistory_Assistant(self, content: str):
        message = {"role": "assistant", "content": content}
        self.messages.append(message)

    def ChatToBot(self, content: str)->SQLAnswes:
        self.addHistory_User(content)
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=self.messages,
            response_format=SQLAnswes,
        )

        event = completion.choices[0].message.parsed
        return event
    def ChatByChat(self, content: str, is_stream: bool) -> Union[str, Generator[str, None, None]]:
        """与 GPT-4 交互，支持流式返回"""
        # 添加用户输入到历史记录
        self.addHistory_User(content)

        # 调用 GPT-4 API
        if is_stream:
            return self._stream_response()
        else:
            return self._standard_response()

    def _standard_response(self) -> str:
        """标准模式：一次性返回整个响应"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=False
        )
        message_content = response.choices[0].message.content
        # 将助手的响应添加到历史记录
        self.addHistory_Assistant(message_content)
        
        return message_content

    async def _stream_response(self) -> AsyncGenerator[str, None]:
        """流模式：逐步返回响应"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        
        async for chunk in response:
            delta_content = chunk.choices[0].delta.get("content")
            if delta_content:
                yield delta_content
if __name__ == "__main__":
    openai = OpenAILLM()
    openai.setPrompt("你是一个高级数据库工程师，致力于帮助用户写SQL语句。")
    print(openai.ChatByChat("请帮我写一个查询所有学生的SQL语句", False))
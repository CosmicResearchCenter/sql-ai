from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam,ChatCompletionToolChoiceOptionParam
# import openai
from typing import List,Iterable
import sys
# sys.path.append('..')
from app.config.config import OPENAI_API_KEY,OPENAI_BASE_URL,LLM_MODEL
from app.schemas.sql import SQLAnswer,SQLAnswes

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

if __name__ == "__main__":
    openai = OpenAILLM()
    openai.setPrompt("你是一个高级数据库工程师，致力于帮助用户写SQL语句。")
    content = """表：Logs
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
在 SQL 中，id 是该表的主键。
id 是一个自增列。
 

找出所有至少连续出现三次的数字。

返回的结果表中的数据可以按 任意顺序 排列。

需要多种方法解决这个问题。
"""
    answer = openai.ChatToBot(content)
    for a in answer.answers:
        print("SQL Statement: ")
        print(a.sql_statement) 
        print("---"*20)
        print("Explanation:")
        print(a.explanation)
        print("---"*20)
    
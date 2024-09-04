from fastapi import APIRouter
from app.core.llm.llm import OpenAILLM
from app.schemas.query import QueryRequset, QueryResponse



router = APIRouter()

@router.post("/query")
def query(query: QueryRequset):
    ai_client = OpenAILLM()
    ai_client.setPrompt("你是一个数据库高级工程师，专门为用户解答SQL相关问题。")
    
    content = f"""
        请你根据下面的问题，写出SQL语句和解释。回答的解释请使用中文解释。如果有多种写法，可以给出多种答案。
        问题{query.query}
    """

    response = ai_client.ChatToBot(content)

    return QueryResponse(code=200, data=response.to_dict(), message="success")

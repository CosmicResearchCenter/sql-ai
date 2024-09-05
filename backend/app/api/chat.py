from fastapi import APIRouter,WebSocket
from app.core.llm.llm import OpenAILLM
from app.schemas.query import QueryRequset, QueryResponse
from app.schemas.chat import Question,Answer


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

def chat(question: Question):
    ai_client = OpenAILLM()
    ai_client.setPrompt("你是一个数据库高级工程师，专门为用户解答SQL相关问题。")

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # OpenAI GPT-4 生成器
    async def openai_stream():
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ],
            stream=True
        )
        for chunk in completion:
            # 返回 GPT-4 生成的 delta 内容
            yield chunk.choices[0].delta.get("content", "")

    try:
        async for chunk in openai_stream():
            await websocket.send_text(chunk)  # 将数据发送给前端
            await asyncio.sleep(0.1)  # 模拟流式延迟
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
    
@router.post("/chat")
async def chat(request: Question):
    """
    标准返回的聊天接口
    """
    if request.is_stream:
        return {"error": "Use WebSocket for streaming responses"}
    llm_client = OpenAILLM()
    llm_client.setPrompt("你是一个数据库高级工程师，专门为用户解答SQL相关问题。")
    response = llm_client.ChatByChat(request.question, is_stream=False)
    return Answer(answer=response)


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket 实现的流式返回
    """
    await websocket.accept()
    
    try:
        data = await websocket.receive_json()
        content = data.get("content", "")
        
        if not content:
            await websocket.send_text("Error: No content provided")
            await websocket.close()
            return
        llm_client = OpenAILLM()
        llm_client.setPrompt("你是一个数据库高级工程师，专门为用户解答SQL相关问题。")
        
        stream_response = llm_client.ChatByChat(content, is_stream=True)

        # 流式返回内容
        async for chunk in stream_response:
            await websocket.send_text(chunk)
            
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

from pydantic import BaseModel

class Question(BaseModel):
    question: str
    is_stream: bool = False

class Answer(BaseModel):
    answer: str
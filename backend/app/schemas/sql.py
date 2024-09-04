from pydantic import BaseModel
from typing import List, Any


class SQLAnswer(BaseModel):
    sql_statement:str
    explanation:str
class SQLAnswes(BaseModel):
    answers:List[SQLAnswer]
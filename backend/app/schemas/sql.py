from pydantic import BaseModel
from typing import List, Any


class SQLAnswer(BaseModel):
    sql_statement:str
    explanation:str
class SQLAnswes(BaseModel):
    answers:List[SQLAnswer]

    def to_dict(self):
        return [
                {
                    "sql_statement": answer.sql_statement,
                    "explanation": answer.explanation
                } for answer in self.answers]
    
from pydantic import BaseModel
from typing import Any,List,Dict,Tuple
class QueryRequset(BaseModel):
    query: str

class QueryResponse(BaseModel):
    code: int
    data: List[Dict[str, Any]]
    message: str

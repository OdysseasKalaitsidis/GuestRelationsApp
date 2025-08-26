from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    email_content: str

class ChatResponse(BaseModel):
    response: str
    relevant_documents: Optional[list] = None

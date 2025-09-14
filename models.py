from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a single message in a chat conversation."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Message timestamp")
    

class Chat(BaseModel):
    """Represents a chat session between a user and the AI."""
    chat_id: str = Field(..., description="Unique identifier for the chat")
    user_id: str = Field(..., description="Unique identifier for the user")
    title: str = Field(..., description="Title of the chat")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the chat")
    created_at: datetime = Field(default_factory=datetime.now, description="Chat creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    

class SearchRequest(BaseModel):
    """Request model for the search endpoint."""
    user_id: str = Field(..., description="User identifier")
    chat_id: str = Field(..., description="Chat identifier")
    question: str = Field(..., description="User's question")

class SearchResponse(BaseModel):
    """Response model for the search endpoint."""
    messages: List[Message] = Field(..., description="List of messages in the chat")

class ChatTitleUpdateRequest(BaseModel):
    """Request model for updating chat title."""
    chat_title: str = Field(..., description="New title for the chat")
 
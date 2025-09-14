import logging
from typing import List, Optional
from repositories import InMemoryChatRepository
from models import Chat, Message, SearchRequest, SearchResponse
from chatbot import Chatbot

# Get logger for this module
logger = logging.getLogger(__name__)

class ChatService:
    """
    Service layer for chat operations.
    
    Handles business logic and coordinates between repository and chatbot.
    """
    
    def __init__(self, chat_repository: InMemoryChatRepository, chatbot: Chatbot):
        self.chat_repository = chat_repository
        self.chatbot = chatbot
        self.logger = logger
        self.logger.info("ChatService initialized")

    async def search(self, request: SearchRequest) -> SearchResponse:
        """
        Process a search request and return the complete chat history.
        
        Args:
            request: Search request with user_id, chat_id, and question
            
        Returns:
            SearchResponse containing all messages in the chat
        """
        try:
            self.logger.info(f"Processing search for user {request.user_id}, chat {request.chat_id}")
            
            # Get or create the chat
            chat = self.chat_repository.get_or_create_chat(
                request.user_id, 
                request.chat_id,
                title=f"Chat {request.chat_id}"
            )
            
            # Add user message to chat
            user_message = Message(role="user", content=request.question)
            chat = self.chat_repository.add_message_to_chat(
                request.user_id, 
                request.chat_id, 
                user_message
            )
            
            # Get previous messages (excluding the current user message for AI context)
            previous_messages = chat.messages[:-1] if len(chat.messages) > 1 else []
            
            # Get AI response using previous messages for context
            ai_response = await self.chatbot.ainvoke(request.question, previous_messages)
            
            # Add AI response to chat
            ai_message = Message(role="assistant", content=ai_response)
            final_chat = self.chat_repository.add_message_to_chat(
                request.user_id, 
                request.chat_id, 
                ai_message
            )
            
            self.logger.info(f"Search completed for chat {request.chat_id}")
            
            # Return all messages in the chat
            return SearchResponse(messages=final_chat.messages)
            
        except Exception as e:
            self.logger.error(f"Error processing search request: {e}")
            raise

    def get_chat(self, user_id: str, chat_id: str) -> Optional[Chat]:
        """Get a specific chat for a user."""
        try:
            return self.chat_repository.get_chat(user_id, chat_id)
        except Exception as e:
            self.logger.error(f"Error getting chat: {e}")
            return None
    
    def get_user_chats(self, user_id: str) -> List[Chat]:
        """Get all chats for a user."""
        try:
            return self.chat_repository.get_user_chats(user_id)
        except Exception as e:
            self.logger.error(f"Error getting user chats: {e}")
            return []
    
    def delete_chat(self, user_id: str, chat_id: str) -> bool:
        """Delete a chat for a user."""
        try:
            return self.chat_repository.delete_chat(user_id, chat_id)
        except Exception as e:
            self.logger.error(f"Error deleting chat: {e}")
            return False
    
    def update_chat_title(self, user_id: str, chat_id: str, title: str) -> Optional[Chat]:
        """Update the title of a chat."""
        try:
            return self.chat_repository.update_chat_title(user_id, chat_id, title)
        except Exception as e:
            self.logger.error(f"Error updating chat title: {e}")
            return None
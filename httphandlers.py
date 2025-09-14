import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from models import (
    Chat, SearchRequest, ChatTitleUpdateRequest, SearchResponse
)
from services import ChatService

# Get logger for this module
logger = logging.getLogger(__name__)

def init_http_handlers(app: FastAPI, chat_service: ChatService):
    """
    Initialize the HTTP handlers.
    """
    @app.get("/")
    async def get_root():
        """
        Root endpoint.
        """
        logger.info("Root endpoint accessed")
        return {"message": "Hello, World!"}

    @app.post("/search", response_model=SearchResponse)
    async def post_search(request: SearchRequest):
        """
        Search endpoint that processes a user question and returns AI response.
        """
        logger.info(f"Search request received - User: {request.user_id}, Chat: {request.chat_id}, Question: {request.question[:50]}...")
        return await chat_service.search(request)


    @app.get("/searches/{user_id}/chats/{chat_id}", response_model=Chat)
    async def get_chat(user_id: str, chat_id: str):
        """
        Retrieve a single chat for a user.
        """
        logger.info(f"Get chat request - User: {user_id}, Chat: {chat_id}")
        chat = chat_service.get_chat(user_id, chat_id)
        if chat is None:
            logger.warning(f"Chat {chat_id} not found for user {user_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Chat {chat_id} not found for user {user_id}"
            )
        return chat


    @app.get("/searches/{user_id}", response_model=List[Chat])
    async def get_user_chats(user_id: str):
        """
        Retrieve all chats for a user.
        """
        logger.info(f"Get user chats request - User: {user_id}")
        return chat_service.get_user_chats(user_id)


    @app.delete("/searches/{user_id}/chats/{chat_id}")
    async def delete_chat(user_id: str, chat_id: str):
        """
        Delete a single chat for a user.
        """
        logger.info(f"Delete chat request - User: {user_id}, Chat: {chat_id}")
        deleted = chat_service.delete_chat(user_id, chat_id)
        if not deleted:
            logger.warning(f"Chat {chat_id} not found for deletion, user {user_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Chat {chat_id} not found for user {user_id}"
            )
        return {"message": f"Chat {chat_id} deleted successfully", "deleted": True}

    @app.patch("/searches/{user_id}/chats/{chat_id}", response_model=Chat)
    async def patch_chat_title(user_id: str, chat_id: str, title_update: ChatTitleUpdateRequest):
        """
        Update the title of a chat.
        """
        logger.info(f"Update chat title request - User: {user_id}, Chat: {chat_id}, New Title: {title_update.chat_title}")
        updated_chat = chat_service.update_chat_title(user_id, chat_id, title_update.chat_title)
        if updated_chat is None:
            logger.warning(f"Chat {chat_id} not found for title update, user {user_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Chat {chat_id} not found for user {user_id}"
            )
        return updated_chat

    @app.get("/health")
    async def health_check():
        """
        Health check endpoint.
        """
        logger.debug("Health check endpoint accessed")
        return {
            "status": "healthy",
            "service": "AI Chatbot Search API",
            "version": "1.0.0"
        }

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """
        Global exception handler for unhandled errors.
        """
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "type": type(exc).__name__
            }
        )
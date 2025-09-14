"""
Main FastAPI application for the chatbot search application.
"""
import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

from httphandlers import init_http_handlers
from repositories import InMemoryChatRepository
from chatbot import Chatbot
from services import ChatService

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging():
    """Setup logging configuration based on environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")
    return logger

# Setup logging
logger = setup_logging()

# Initialize repositories
chat_repository = InMemoryChatRepository()
chatbot = Chatbot()
chat_service = ChatService(chat_repository, chatbot)

# Create FastAPI application
app = FastAPI()

# Initialize HTTP handlers
init_http_handlers(app, chat_service)

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting AI Chatbot Search API on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )

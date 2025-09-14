import os
import logging
from typing import List

from langchain.chat_models import init_chat_model
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from models import Message

# Get logger for this module
logger = logging.getLogger(__name__)

class Chatbot:
    """
    Chatbot service for AI-powered conversations using LangChain.
    """
    
    def __init__(self):
        """Initialize the chatbot with LLM configuration."""
        self.logger = logger
        self.logger.info("Chatbot initialized")
        
        # LLM configuration
        llm_config = {
            "model": os.getenv("LLM_MODEL_NAME"),
            "model_provider": os.getenv("LLM_MODEL_PROVIDER"),
            "temperature": 0,
            "max_tokens": 1000,
        }
        
        try:
            self.llm = init_chat_model(**llm_config)
            self.logger.info(f"LLM initialized with model: {llm_config['model']}")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM: {e}")
            raise
        
        # Conversation template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Answer questions clearly and concisely."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        
        # Conversation chain (without memory - we'll build it dynamically)
        self.conversation_chain = self.prompt | self.llm | StrOutputParser()

    def _convert_messages_to_langchain(self, messages: List[Message]) -> List:
        """
        Convert our Message objects to LangChain message format.
        
        Args:
            messages: List of Message objects
            
        Returns:
            List of LangChain message objects
        """
        langchain_messages = []
        
        for msg in messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
            else:
                # Handle any other roles as human messages
                self.logger.warning(f"Unknown message role: {msg.role}, treating as human")
                langchain_messages.append(HumanMessage(content=msg.content))
        
        return langchain_messages

    async def ainvoke(self, user_message: str, previous_messages: List[Message]) -> str:
        """
        Chat with the LLM using provided message history.
        
        Args:
            user_message: The current user input
            previous_messages: List of previous messages to build context
            
        Returns:
            AI response text
        """
        try:
            self.logger.debug(f"Processing message with {len(previous_messages)} previous messages")
            
            # Build chat history from previous messages
            chat_history = self._convert_messages_to_langchain(previous_messages)
            
            # Invoke the conversation chain with the built history
            response = await self.conversation_chain.ainvoke({
                "input": user_message,
                "chat_history": chat_history
            })
            
            self.logger.debug(f"Generated response: {response[:100]}...")
            return response
            
        except Exception as e:
            self.logger.error(f"Error during AI invocation: {e}")
            raise

    def invoke(self, user_message: str, previous_messages: List[Message]) -> str:
        """
        Synchronous version of ainvoke for compatibility.
        
        Args:
            user_message: The current user input
            previous_messages: List of previous messages to build context
            
        Returns:
            AI response text
        """
        try:
            self.logger.debug(f"Processing sync message with {len(previous_messages)} previous messages")
            
            # Build chat history from previous messages
            chat_history = self._convert_messages_to_langchain(previous_messages)
            
            # Invoke the conversation chain with the built history
            response = self.conversation_chain.invoke({
                "input": user_message,
                "chat_history": chat_history
            })
            
            self.logger.debug(f"Generated sync response: {response[:100]}...")
            return response
            
        except Exception as e:
            self.logger.error(f"Error during sync AI invocation: {e}")
            raise
 
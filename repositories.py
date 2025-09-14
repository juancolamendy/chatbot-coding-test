import logging
from typing import List, Optional, Dict
from datetime import datetime
from models import Chat, Message

# Get logger for this module
logger = logging.getLogger(__name__)


class InMemoryChatRepository:
    """
    In-memory repository for chat management.
    
    This repository provides CRUD operations for chats using in-memory storage.
    In production, this would be replaced with a proper database implementation.
    """
    
    def __init__(self):
        """Initialize the repository with empty storage."""
        # Store chats as a nested dictionary: {user_id: {chat_id: Chat}}
        self.chats: Dict[str, Dict[str, Chat]] = {}
        logger.info("InMemoryChatRepository initialized")
    
    def create_chat(self, chat: Chat) -> Chat:
        """
        Create a new chat.
        
        Args:
            chat: Chat object to create
            
        Returns:
            Created chat object
            
        Raises:
            ValueError: If chat with same ID already exists for the user
        """
        if chat.user_id not in self.chats:
            self.chats[chat.user_id] = {}
        
        if chat.chat_id in self.chats[chat.user_id]:
            logger.warning(f"Chat {chat.chat_id} already exists for user {chat.user_id}")
            raise ValueError(f"Chat {chat.chat_id} already exists for user {chat.user_id}")
        
        # Set timestamps
        chat.created_at = datetime.now()
        chat.updated_at = datetime.now()
        
        self.chats[chat.user_id][chat.chat_id] = chat
        logger.info(f"Created chat {chat.chat_id} for user {chat.user_id}")
        return chat
    
    def get_chat(self, user_id: str, chat_id: str) -> Optional[Chat]:
        """
        Get a specific chat for a user.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            
        Returns:
            Chat object if found, None otherwise
        """
        if user_id not in self.chats or chat_id not in self.chats[user_id]:
            logger.debug(f"Chat {chat_id} not found for user {user_id}")
            return None
        
        chat = self.chats[user_id][chat_id]
        logger.debug(f"Retrieved chat {chat_id} for user {user_id}")
        return chat
    
    def get_user_chats(self, user_id: str) -> List[Chat]:
        """
        Get all chats for a specific user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of chat objects for the user
        """
        if user_id not in self.chats:
            logger.debug(f"No chats found for user {user_id}")
            return []
        
        chats = list(self.chats[user_id].values())
        logger.debug(f"Retrieved {len(chats)} chats for user {user_id}")
        return chats
    
    def update_chat(self, chat: Chat) -> Chat:
        """
        Update an existing chat.
        
        Args:
            chat: Updated chat object
            
        Returns:
            Updated chat object
            
        Raises:
            ValueError: If chat doesn't exist
        """
        if chat.user_id not in self.chats or chat.chat_id not in self.chats[chat.user_id]:
            logger.warning(f"Cannot update chat {chat.chat_id} for user {chat.user_id} - not found")
            raise ValueError(f"Chat {chat.chat_id} not found for user {chat.user_id}")
        
        # Update timestamp
        chat.updated_at = datetime.now()
        
        self.chats[chat.user_id][chat.chat_id] = chat
        logger.info(f"Updated chat {chat.chat_id} for user {chat.user_id}")
        return chat
    
    def update_chat_title(self, user_id: str, chat_id: str, new_title: str) -> Chat:
        """
        Update the title of a specific chat.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            new_title: New title for the chat
            
        Returns:
            Updated chat object
            
        Raises:
            ValueError: If chat doesn't exist
        """
        if user_id not in self.chats or chat_id not in self.chats[user_id]:
            logger.warning(f"Cannot update title for chat {chat_id} - not found")
            raise ValueError(f"Chat {chat_id} not found for user {user_id}")
        
        chat = self.chats[user_id][chat_id]
        chat.title = new_title
        chat.updated_at = datetime.now()
        
        logger.info(f"Updated title for chat {chat_id} to '{new_title}'")
        return chat
    
    def add_message_to_chat(self, user_id: str, chat_id: str, message: Message) -> Chat:
        """
        Add a message to a specific chat.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            message: Message to add
            
        Returns:
            Updated chat object
            
        Raises:
            ValueError: If chat doesn't exist
        """
        if user_id not in self.chats or chat_id not in self.chats[user_id]:
            logger.warning(f"Cannot add message to chat {chat_id} - not found")
            raise ValueError(f"Chat {chat_id} not found for user {user_id}")
        
        chat = self.chats[user_id][chat_id]
        chat.messages.append(message)
        chat.updated_at = datetime.now()
        
        logger.info(f"Added message to chat {chat_id} for user {user_id}")
        return chat
    
    def delete_chat(self, user_id: str, chat_id: str) -> bool:
        """
        Delete a specific chat for a user.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            
        Returns:
            True if chat was deleted, False if not found
        """
        if user_id not in self.chats or chat_id not in self.chats[user_id]:
            logger.warning(f"Cannot delete chat {chat_id} - not found")
            return False
        
        del self.chats[user_id][chat_id]
        
        # If user has no more chats, remove user entry
        if not self.chats[user_id]:
            del self.chats[user_id]
        
        logger.info(f"Deleted chat {chat_id} for user {user_id}")
        return True
    
    def delete_user_chats(self, user_id: str) -> int:
        """
        Delete all chats for a specific user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of chats deleted
        """
        if user_id not in self.chats:
            logger.debug(f"No chats to delete for user {user_id}")
            return 0
        
        deleted_count = len(self.chats[user_id])
        del self.chats[user_id]
        
        logger.info(f"Deleted {deleted_count} chats for user {user_id}")
        return deleted_count
    
    def get_or_create_chat(self, user_id: str, chat_id: str, title: str = None) -> Chat:
        """
        Get an existing chat or create a new one if it doesn't exist.
        
        Args:
            user_id: User identifier
            chat_id: Chat identifier
            title: Title for new chat (if created)
            
        Returns:
            Existing or newly created chat object
        """
        existing_chat = self.get_chat(user_id, chat_id)
        if existing_chat:
            logger.debug(f"Retrieved existing chat {chat_id} for user {user_id}")
            return existing_chat
        
        # Create new chat
        chat_title = title or f"Chat {chat_id}"
        new_chat = Chat(
            chat_id=chat_id,
            user_id=user_id,
            title=chat_title,
            messages=[]
        )
        
        self.create_chat(new_chat)
        logger.info(f"Created new chat {chat_id} for user {user_id}")
        return new_chat
    
    def get_all_chats(self) -> List[Chat]:
        """
        Get all chats across all users.
        
        Returns:
            List of all chat objects
        """
        all_chats = []
        for user_chats in self.chats.values():
            all_chats.extend(user_chats.values())
        
        logger.debug(f"Retrieved {len(all_chats)} total chats")
        return all_chats
    
    def get_chat_count(self, user_id: str = None) -> int:
        """
        Get the count of chats.
        
        Args:
            user_id: If provided, count chats for specific user only
            
        Returns:
            Number of chats
        """
        if user_id:
            count = len(self.chats.get(user_id, {}))
            logger.debug(f"User {user_id} has {count} chats")
            return count
        
        total_count = sum(len(user_chats) for user_chats in self.chats.values())
        logger.debug(f"Total chat count: {total_count}")
        return total_count
    
    def get_user_count(self) -> int:
        """
        Get the count of users with chats.
        
        Returns:
            Number of users with chats
        """
        count = len(self.chats)
        logger.debug(f"User count: {count}")
        return count
    
    def clear_all_chats(self) -> int:
        """
        Clear all chats from the repository.
        
        Returns:
            Number of chats cleared
        """
        total_count = sum(len(user_chats) for user_chats in self.chats.values())
        self.chats.clear()
        
        logger.warning(f"Cleared all {total_count} chats from repository")
        return total_count
    
    def search_chats_by_title(self, title_query: str, user_id: str = None) -> List[Chat]:
        """
        Search chats by title.
        
        Args:
            title_query: Title search query (case-insensitive partial match)
            user_id: If provided, search only in user's chats
            
        Returns:
            List of matching chat objects
        """
        matching_chats = []
        title_query_lower = title_query.lower()
        
        if user_id:
            # Search in specific user's chats
            if user_id in self.chats:
                for chat in self.chats[user_id].values():
                    if title_query_lower in chat.title.lower():
                        matching_chats.append(chat)
        else:
            # Search in all chats
            for user_chats in self.chats.values():
                for chat in user_chats.values():
                    if title_query_lower in chat.title.lower():
                        matching_chats.append(chat)
        
        logger.debug(f"Found {len(matching_chats)} chats matching title query '{title_query}'")
        return matching_chats

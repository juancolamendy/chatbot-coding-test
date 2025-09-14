.PHONY: help install run dev test clean lint format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	uv sync

run: ## Run the development server
	uv run python main.py

dev: ## Run the development server with auto-reload
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	uv run pytest

lint: ## Run linting
	uvx ruff check

format: ## Format code
	uvx ruff format

install-dev: ## Install development dependencies
	uv sync --dev

env: ## Create environment file from example
	cp env.example .env
	@echo "Environment file created from env.example"
	@echo "Please edit .env with your configuration"

# Testing endpoints with curl
test-root: ## Test root endpoint
	curl -X GET "http://localhost:8000/"

test-search: ## Test search endpoint
	curl -X POST "http://localhost:8000/search" \
		-H "Content-Type: application/json" \
		-d '{"user_id": "test_user", "chat_id": "test_chat", "question": "What is AI?"}'

test-search-1: ## Test search endpoint
	curl -X POST "http://localhost:8000/search" \
		-H "Content-Type: application/json" \
		-d '{"user_id": "test_user", "chat_id": "test_chat", "question": "Who are the first researchers?"}'

test-get-chat: ## Test get single chat endpoint
	curl -X GET "http://localhost:8000/searches/test_user/chats/test_chat"

test-get-user-chats: ## Test get all user chats endpoint
	curl -X GET "http://localhost:8000/searches/test_user"

test-delete-chat: ## Test delete chat endpoint
	curl -X DELETE "http://localhost:8000/searches/test_user/chats/test_chat"

test-update-chat-title: ## Test update chat title endpoint
	curl -X PATCH "http://localhost:8000/searches/test_user/chats/test_chat" \
		-H "Content-Type: application/json" \
		-d '{"chat_title": "Updated Chat Title"}'

test-health: ## Test health check endpoint
	curl -X GET "http://localhost:8000/health"

test-all: ## Test all endpoints
	@echo "Testing all endpoints..."
	@echo "1. Testing root endpoint..."
	@make test-root
	@echo ""
	@echo "2. Testing search endpoint..."
	@make test-search
	@echo ""
	@echo "3. Testing get chat endpoint..."
	@make test-get-chat
	@echo ""
	@echo "4. Testing get user chats endpoint..."
	@make test-get-user-chats
	@echo ""
	@echo "5. Testing update chat title endpoint..."
	@make test-update-chat-title
	@echo ""
	@echo "6. Testing health check endpoint..."
	@make test-health
	@echo ""
	@echo "7. Testing delete chat endpoint..."
	@make test-delete-chat
	@echo ""
	@echo "✅ All endpoint tests completed!"

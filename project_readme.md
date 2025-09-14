# Project

## Dependencies
[Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

## Project structure
main.py: entry point
moodels.py: model definitions
chatbot.py: chatbot module
services: services for business orchestration
httphandlers: handlers for http requests (FastAPI)
repositories: implementation of CRUD data. Clients to external backing services (DB services, caching, HTTP/GRPC services)
utils: common utility functions.
.env: env variable settings
pyproject.toml: project/Python dependencies

```sh
make install
```

## Update env vars
```sh
make env
## adjust according to your providers
## For other providers check langchain documentation
```

## Run server
```sh
make run
```

## Search
```sh
make test-search
curl -X POST "http://localhost:8000/search" \
                -H "Content-Type: application/json" \
                -d '{"user_id": "test_user", "chat_id": "test_chat", "question": "What is AI?"}'
{"messages":[{"role":"user","content":"What is AI?","timestamp":"2025-08-15T18:08:02.461399"},{"role":"assistant","content":"AI, or artificial intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.","timestamp":"2025-08-15T18:08:03.078310"}]}


make test-search-1
curl -X POST "http://localhost:8000/search" \
                -H "Content-Type: application/json" \
                -d '{"user_id": "test_user", "chat_id": "test_chat", "question": "Who are the first researchers?"}'
{"messages":[{"role":"user","content":"What is AI?","timestamp":"2025-08-15T18:08:02.461399"},{"role":"assistant","content":"AI, or artificial intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.","timestamp":"2025-08-15T18:08:03.078310"},{"role":"user","content":"Who are the first researchers?","timestamp":"2025-08-15T18:08:27.980146"},{"role":"assistant","content":"The field of AI has many contributors, but some of the earliest and most influential researchers include:\n\n*   **Alan Turing:** Proposed the Turing Test to evaluate machine intelligence.\n*   **John McCarthy:** Coined the term \"artificial intelligence\" and organized the Dartmouth Workshop.\n*   **Marvin Minsky:** Co-founded the MIT AI Lab and made significant contributions to AI theory.\n*   **Allen Newell and Herbert A. Simon:** Developed the Logic Theorist and GPS, early AI programs.","timestamp":"2025-08-15T18:08:29.857882"}]}%
```

# Get chat
```sh
make test-get-chat
curl -X GET "http://localhost:8000/searches/test_user/chats/test_chat"
{"chat_id":"test_chat","user_id":"test_user","title":"Chat test_chat","messages":[{"role":"user","content":"What is AI?","timestamp":"2025-08-15T18:08:02.461399"},{"role":"assistant","content":"AI, or artificial intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.","timestamp":"2025-08-15T18:08:03.078310"},{"role":"user","content":"Who are the first researchers?","timestamp":"2025-08-15T18:08:27.980146"},{"role":"assistant","content":"The field of AI has many contributors, but some of the earliest and most influential researchers include:\n\n*   **Alan Turing:** Proposed the Turing Test to evaluate machine intelligence.\n*   **John McCarthy:** Coined the term \"artificial intelligence\" and organized the Dartmouth Workshop.\n*   **Marvin Minsky:** Co-founded the MIT AI Lab and made significant contributions to AI theory.\n*   **Allen Newell and Herbert A. Simon:** Developed the Logic Theorist and GPS, early AI programs.","timestamp":"2025-08-15T18:08:29.857882"}],"created_at":"2025-08-15T18:08:02.461275","updated_at":"2025-08-15T18:08:29.857911"}%
```

# Get chats
```sh
make test-get-user-chats
curl -X GET "http://localhost:8000/searches/test_user"
[{"chat_id":"test_chat","user_id":"test_user","title":"Chat test_chat","messages":[{"role":"user","content":"What is AI?","timestamp":"2025-08-15T18:08:02.461399"},{"role":"assistant","content":"AI, or artificial intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.","timestamp":"2025-08-15T18:08:03.078310"},{"role":"user","content":"Who are the first researchers?","timestamp":"2025-08-15T18:08:27.980146"},{"role":"assistant","content":"The field of AI has many contributors, but some of the earliest and most influential researchers include:\n\n*   **Alan Turing:** Proposed the Turing Test to evaluate machine intelligence.\n*   **John McCarthy:** Coined the term \"artificial intelligence\" and organized the Dartmouth Workshop.\n*   **Marvin Minsky:** Co-founded the MIT AI Lab and made significant contributions to AI theory.\n*   **Allen Newell and Herbert A. Simon:** Developed the Logic Theorist and GPS, early AI programs.","timestamp":"2025-08-15T18:08:29.857882"}],"created_at":"2025-08-15T18:08:02.461275","updated_at":"2025-08-15T18:08:29.857911"}]
```

# Update title
```sh
make test-update-chat-title
curl -X PATCH "http://localhost:8000/searches/test_user/chats/test_chat" \
                -H "Content-Type: application/json" \
                -d '{"chat_title": "Updated Chat Title"}'
{"chat_id":"test_chat","user_id":"test_user","title":"Updated Chat Title","messages":[{"role":"user","content":"What is AI?","timestamp":"2025-08-15T18:08:02.461399"},{"role":"assistant","content":"AI, or artificial intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.","timestamp":"2025-08-15T18:08:03.078310"},{"role":"user","content":"Who are the first researchers?","timestamp":"2025-08-15T18:08:27.980146"},{"role":"assistant","content":"The field of AI has many contributors, but some of the earliest and most influential researchers include:\n\n*   **Alan Turing:** Proposed the Turing Test to evaluate machine intelligence.\n*   **John McCarthy:** Coined the term \"artificial intelligence\" and organized the Dartmouth Workshop.\n*   **Marvin Minsky:** Co-founded the MIT AI Lab and made significant contributions to AI theory.\n*   **Allen Newell and Herbert A. Simon:** Developed the Logic Theorist and GPS, early AI programs.","timestamp":"2025-08-15T18:08:29.857882"}],"created_at":"2025-08-15T18:08:02.461275","updated_at":"2025-08-15T18:10:19.815998"}
```

# Delete chat
```sh
make test-delete-chat
curl -X DELETE "http://localhost:8000/searches/test_user/chats/test_chat"
{"message":"Chat test_chat deleted successfully","deleted":true}
```

# Get chat again
```sh
make test-get-chat
curl -X GET "http://localhost:8000/searches/test_user/chats/test_chat"
{"detail":"Chat test_chat not found for user test_user"}%

make test-get-user-chats
curl -X GET "http://localhost:8000/searches/test_user"
[]%
```
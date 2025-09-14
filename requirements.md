# Requirements

## Functional requirements
- chatbot should be able to answer a user's question and be aware of previous questions
- system should store and retrieve past chat histories

## Entities
[Chat]
- chat id: chat id
- user ID: ID of the user (string object) 
- chat title: title of the chat (string object)
- messages: array of question-answer pairs where the answer includes a bot response as well as other fields like search results

# API
- POST /search
Request payload
```js
{
    'user_id': "user_id",
    'chat_id': "chat_id",
    'question': "question"
}
```
Response payload
```json
{
    "messages": [
        {
            "role": "user",
            "content": "<first_question>"
        },
        {
            "role": "assistant",
            "content": "<first_response>"
        },
        {
            "role": "user",
            "content": "<current_question>"
        }
    ]    
}
```

- GET /searches/{user_id}/chats/{chat_id}
Retrieve a single chat of an user (specified with their user ID)

- GET /searches/{user_id}
Retrieve all chats of an user

- DELETE /searches/{user_id}/chats/{chat_id}

- PATCH /searches/{user_id}/chats/{chat_id} 
Request payload
{
    "chat_title": "the chat title"
}

## Non-functional requirements
### Technologies
- web server (FastAPI)
- model and validation (Pydantic)
- language: Python

### Security
API Key in the header: `X-API-Key': '<api-key>`
Save API as config in the `.env` file. (`e7e0734b-98e5-468e-ba0e-0ac800088746<__>1QwX5qETU8N2v5f4zKakO3rt`)

## Questions
### Q1
Requirement: system should store and retrieve past chat histories
Question:
Should I store past chat histories in memory to simplify? Or it's required a durable medium such as db?
If I can use in memory db. Then, in the design session, I can talk more about DB technologies I could use for this solution.

### Q2
In the example, you provide `curl --location 'https://chat-api.you.com/smart'` but the description says the endpoint is `POST /search`, so I will asume `/search` as the endpoint.

### Q3
I need to have chat id for GET request filtering. Should chat IDs be auto-generated (UUID) or provided by the client?

### Q4
The `/search enpoint` suggests it should save and return the AI response. Should the response include:
- Just the new AI response?
- The updated chat with all messages?
- Both the AI response and the updated chat object?

### Q5
What should happen when chat_id or user_id don't exist?
Should I return an empty json `{}`

### Q6
Can you please elaborate a little further the references to other fiedls like search results? => chat: array of question-answer pairs where the answer includes a bot response as well as other fields like search results

### Q7
Any validation rules to perform on:
- User IDs (format, length)?
- Chat titles (max length, allowed characters)?
- Questions (max length, content validation)?

### Q8
Which LLM provider use for the chatbot?
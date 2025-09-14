# takehome-backend

Source: https://github.com/Su-Sea/takehome-backend-JuanC-

Build a web server that runs an AI chatbot application, preferably using Python. The chatbot should be able to answer a user's question and be aware of previous questions within the same chat. The system should store and retrieve past chat histories for each user and allow simple CRUD operations on the chat objects.

A chat consists of the following fields at the minimum:
- user ID: ID of the user (string object) 
- chat title: title of the chat (string object)
- chat: array of question-answer pairs where the answer includes a bot response as well as other fields like search results

We leave you the freedom to structure your data model to your choosing. You can also add other fields to the models when you think they are relevant to the service. We do not expect any UI for this take-home. A simple web server with the specified API routes is sufficient. 

## API routes

Your app should expose a few routes:
- POST /search:
The search endpoint should take an `user_id`, `chat_id`, and `question` as payload. During the search, it should fetch any past messages of the chat, call the AI chatbot and then save and return the response.

    The AI chatbot should be called the following way using the following API key (`e7e0734b-98e5-468e-ba0e-0ac800088746<__>1QwX5qETU8N2v5f4zKakO3rt`): 
    ```
    curl --location 'https://chat-api.you.com/smart' \
    --header 'X-API-Key': '<api-key>', \
    --header 'Content-Type: application/json' \
    --data '{
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
    }'
    ```

- GET route to retrieve a single chat of an user (specified with their user ID)
- GET route to retrieve all chats of an user
- DELETE route to a single chat of an user.
- PATCH route to update the title of a chat

Bonus points:
- If you think the system would benefit from more or other routes, feel free to add them to the ones listed above.

## Closing remarks
  
During the review session, you will:
- Discuss your design approach: Explain your database choice, API design, and how you addressed scalability, security, and extensibility.
- Walk through your implementation, explaining your logic and any trade-offs you made.
- Answer follow-up questions: Be prepared to discuss edge cases, potential improvements, and how your solution could evolve for larger-scale use.

When you're finished, upload any code you used to set up or run your code to this repository with notes on how to run the program locally. We'll try to run it before your review session, which you can schedule by sending an email to nushi@you.com (cc tom@you.com, jasonharrison@you.com, shiv@you.com) with the subject "[Backend Takehome Finished] YOUR_NAME" and your availability.

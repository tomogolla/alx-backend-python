# Django REST API - Messaging App

This project implements a robust and RESTful API for a simple messaging application using Django and Django REST Framework. It provides core functionalities for user management, initiating and managing conversations, and sending messages.

---

## Table of Contents

- [Features](#features)
- [API Endpoints](#api-endpoints)
  - [Users](#users)
  - [Conversations](#conversations)
  - [Messages](#messages)
- [Authentication](#authentication)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Testing the API](#testing-the-api)
- [Models Overview](#models-overview)
- [Future Enhancements](#future-enhancements)

---

## Features

### User Management

- **List Users**: Retrieve a list of all users (excluding the authenticated user for non-staff).
- **Retrieve User Profile**: Access details of a specific user by their ID.

### Conversation Management

- **List Conversations**: View all conversations the authenticated user is part of.
- **Retrieve Conversation Details**: Get full details of a specific conversation, including messages.
- **Create Direct Messages (DMs)**: Initiate 2-person conversations or reuse existing ones.

### Message Management

- **List Messages**: Retrieve messages from conversations the user participates in.
- **Send Messages**: Create new messages. Automatically manages the 2-person conversation context.

---


---

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Users

#### `GET /api/users/` — `users_list`
Retrieve all registered users (excludes the authenticated user for non-staff).

#### `GET /api/users/{user_id}/`
Retrieve detailed profile of a specific user.

---

### Conversations

#### `GET /conversations/` — `conversations_list`
List all conversations the authenticated user is a participant of.

#### `POST /conversations/` — `conversations_create`
Initiate a new direct conversation or return existing one.

**Request Example**:
```json
{
  "target_user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Optional Chat Name"
}
```

#### `GET /conversations/{conversation_id}/` — `conversations_read`
Retrieve a specific conversation with its messages in chronological order.

#### `PUT /conversations/{conversation_id}/` — `conversations_update`
Fully update the details of a conversation.

#### `PATCH /conversations/{conversation_id}/` — `conversations_partial_update`
Partially update details of a specific conversation.

#### `DELETE /conversations/{conversation_id}/` — `conversations_delete`
Delete a specific conversation.

---

### Messages

#### `GET /conversations/{conversation_pk}/messages/` — `conversations_messages_list`
Retrieve all messages in a conversation.

#### `POST /conversations/{conversation_pk}/messages/` — `conversations_messages_create`
Send a new message within a conversation.

#### `GET /conversations/{conversation_pk}/messages/{message_id}/` — `conversations_messages_read`
Retrieve a specific message within a conversation.

#### `PUT /conversations/{conversation_pk}/messages/{message_id}/` — `conversations_messages_update`
Fully update a specific message.

#### `PATCH /conversations/{conversation_pk}/messages/{message_id}/` — `conversations_messages_partial_update`
Partially update a specific message.

#### `DELETE /conversations/{conversation_pk}/messages/{message_id}/` — `conversations_messages_delete`
Delete a specific message.


## Authentication

This API uses Django REST Framework’s default authentication mechanisms:

- **Session Authentication**: Best for web apps using Django login.
- **Basic Authentication**: Available for development/testing.

> ⚠️ For production, use Token-based authentication (e.g., JWT).

---

## Setup and Installation

1. **Clone the repository**:
```bash
git clone <repository_url>
cd <repository_directory>
```

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- Windows:
  ```bash
  .env\Scriptsctivate
  ```

4. **Install dependencies**:
```bash
pip install Django djangorestframework
# Optional for PostgreSQL
pip install psycopg2-binary
```

5. **Configure settings**:
- Add `'chats'` and `'rest_framework'` to `INSTALLED_APPS`.
- Set `AUTH_USER_MODEL = 'chats.User'`.
- Configure REST framework and auth settings as needed.

6. **Apply migrations**:
```bash
python manage.py makemigrations chats
python manage.py migrate
```

7. **Create a superuser**:
```bash
python manage.py createsuperuser
```

---

## Running the Application

```bash
python manage.py runserver
```

Access the API at: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## Testing the API

### Tools:
- **DRF Browsable API**: User-friendly web interface.
- **curl**: Command-line testing.
- **Postman/Insomnia**: GUI clients for API testing.

### Example `curl` Requests:

**Get current user profile**:
```bash
curl -X GET "http://127.0.0.1:8000/api/me/"   -H "Cookie: sessionid=<SESSION_ID>; csrftoken=<CSRF_TOKEN>"
```

**Send a message**:
```bash
curl -X POST "http://127.0.0.1:8000/api/messages/"   -H "Content-Type: application/json"   -H "Cookie: sessionid=<SESSION_ID>; csrftoken=<CSRF_TOKEN>"   -d '{
        "target_user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "message_body": "Hello from curl! This is a test message."
      }'
```

---

## Models Overview

### User
- Custom `AbstractUser`.
- `UUIDField` (`user_id`) as primary key.
- Fields: `email`, `phone_number`, `bio`.

### Conversation
- `UUIDField` (`conversation_id`) as primary key.
- Optional `name` field.
- `ManyToManyField` to `User` as `participants`.

### Message
- `UUIDField` (`message_id`) as primary key.
- `ForeignKey` to `Conversation` and `User` (sender).
- Fields: `message_body`, `sent_at`, `is_read`.

---

## Future Enhancements

- ✅ **Real-time Communication**: WebSockets (Django Channels).
- 🔐 **Advanced Authentication**: Token-based (e.g., JWT).
- 👥 **Group Chat**: Multi-user conversation creation.
- 👁 **Read Receipts**: Track read/unread status.
- 🔔 **Push Notifications**: Alert users to new messages.
- 🔍 **Search and Filtering**: Search messages by keyword/date.
- 📄 **Pagination for Nested Messages**: For long conversations.
- 📎 **Media Attachments**: Support images, videos, etc.
- 🧪 **Comprehensive Testing**: Unit and integration tests.

---
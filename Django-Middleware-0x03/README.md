

```markdown
# Django Middleware Project - ALX Backend Python

This project showcases custom Django middleware implementations for logging, access control, and request throttling. Each middleware is designed to enhance observability, security, and reliability in a chat messaging application.

## 📁 Directory Structure

```

Django-Middleware-0x03/
├── chats/
│   ├── middleware.py     # All middleware implementations
│   └── views.py          # Chat endpoints (assumed)
├── requests.log          # Logs from RequestLoggingMiddleware
├── manage.py
├── settings.py
└── ...

````

---

## ✅ Middleware Implementations

### 1. **RequestLoggingMiddleware**

Logs every incoming request’s timestamp, user (if authenticated), and the request path.

- **File**: `chats/middleware.py`
- **Log File**: `requests.log`

#### ✨ Logged Format:
```text
2025-07-16 20:13:45 - User: john@example.com - Path: /chats/
````

#### 🔧 Setup:

```python
MIDDLEWARE = [
    ...
    'chats.middleware.RequestLoggingMiddleware',
]
```

---

### 2. **RestrictAccessByTimeMiddleware**

Restricts chat access to business hours only: **6:00 AM – 9:00 PM**. Access outside this window results in a **403 Forbidden** error.

* **File**: `chats/middleware.py`

#### ❌ Blocked Response:

```json
{
  "error": "Access to chat is not allowed outside permitted hours (6AM to 9PM)."
}
```

#### 🔧 Setup:

```python
MIDDLEWARE = [
    ...
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
]
```

---

### 3. **OffensiveLanguageMiddleware (Rate Limiting Middleware)**

Limits users to **5 messages per minute** based on their IP address. This helps reduce spam and offensive content flooding.

* **File**: `chats/middleware.py`

#### ❌ Blocked Response:

```json
{
  "error": "Rate limit exceeded. You can only send 5 messages per minute."
}
```

#### 🧠 Logic:

* Applies to all `POST` requests under `/chats/`
* Tracks timestamps by IP address
* Uses `X-Forwarded-For` header or `REMOTE_ADDR`

#### 🔧 Setup:

```python
MIDDLEWARE = [
    ...
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
]
```

---

## 🧪 Testing with Postman

You can use [Postman](https://www.postman.com/) or `curl` to test the middleware behavior.

### ✔️ Auth Test:

1. Authenticate using `/login/` to get JWT token.
2. Access private routes like `/conversations/`.
3. Verify unauthorized access is blocked.

### ✔️ Message Rate Limiting:

1. Send >5 messages within a minute to `/chats/messages/`
2. Ensure you're blocked after 5 requests (HTTP 429).

### ✔️ Time Restriction:

1. Attempt to access `/chats/` during restricted hours (e.g., 2:00 AM).
2. You should receive a 403 Forbidden.

---

## 🛠 Requirements

* Python 3.8+
* Django 4.x
* DRF (Django REST Framework) for chat endpoints
* `requests.log` file should be writable by Django process

---

## 🤝 Contributing

Pull requests are welcome. If you encounter bugs or wish to improve performance, please open an issue first.

---

## 📜 License

This project is part of the ALX Software Engineering Program and follows the MIT License.

---

## ✍️ Author

**Thomas Ogolla**
[GitHub](https://github.com/tomogolla) • [LinkedIn](https://linkedin.com/in/tomogolla)

```

---


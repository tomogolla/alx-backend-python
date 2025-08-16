Overview
In this project, learners will explore the complete lifecycle of designing and implementing robust RESTful APIs using Django. They will begin with scaffolding the project environment and progressively move through identifying and defining data models, establishing database relationships, and setting up clean, scalable URL routing. Emphasis is placed on following Django’s best practices to ensure maintainable and production-ready codebases.

This project serves as a foundation for any backend developer aiming to master API development using the Django framework and prepares learners to build secure, scalable systems that follow modern architectural patterns.

Project Objectives
By the end of this project, learners will be able to:

Scaffold a Django project using industry-standard project structures.
Identify, define, and implement scalable data models using Django’s ORM.
Establish one-to-many, many-to-many, and one-to-one relationships between models.
Create clean and modular Django apps.
Set up and configure URL routing for APIs using Django’s path and include functions.
Follow best practices in file structure, code organization, and documentation.
Build a maintainable API layer using Django REST Framework (optional enhancement).
Validate and test APIs with real data using tools like Postman or Swagger.
Learning Outcomes
Upon completing this project, learners will:

Understand the structure of a Django project and how to scaffold it properly.
Be able to design relational database schemas based on feature requirements.
Gain confidence in using Django models and migrations to persist data.
Build and route API endpoints that adhere to RESTful conventions.
Separate concerns by organizing views, serializers (if using DRF), and URL configurations.
Understand and apply modular development strategies by separating logic into reusable apps.
Follow Django’s naming and configuration conventions to improve code readability and team collaboration.
Key Implementation Phases
Project Setup and Environment Configuration

Create a virtual environment
Install Django
Scaffold the project with django-admin startproject and python manage.py startapp
Configure settings.py (INSTALLED_APPS, middleware, CORS, etc.)
Defining Data Models

Identify core models based on requirements (e.g., User, Property, Booking)
Use Django ORM to define model classes
Add field types, constraints, and default behaviors
Apply migrations and use Django Admin for verification
Establishing Relationships

Implement foreign keys, many-to-many relationships, and one-to-one links
Use related_name, on_delete, and reverse relationships effectively
Use Django shell to test object relations
URL Routing

Define app-specific routes using urls.py
Use include() to modularize routes per app
Follow RESTful naming conventions: /api/properties/, /api/bookings/<id>/
Create nested routes when necessary
Best Practices and Documentation

Use views.py to separate logic and ensure Single Responsibility
Document endpoints using README or auto-generated documentation tools
Keep configuration settings modular (e.g., using .env or settings/ directory structure)
Use versioned APIs (e.g., /api/v1/) to future-proof development
Best Practices for Scaffolding and Structuring Projects
Area	Best Practices
Project Structure	Keep a modular structure with reusable apps, consistent naming, and organized folders (apps/, core/, etc.)
Environment Config	Use .env files and django-environ to manage secret keys and settings
Models	Avoid business logic in models; use helper functions or managers when necessary
Migrations	Commit migration files and test them on a fresh database
Routing	Namespace routes and separate admin/API/user-related URLs for clarity
Security	Use ALLOWED_HOSTS, avoid hardcoding credentials, and enable CORS properly
Testing	Use Django’s test client or tools like Postman to validate endpoints early and often
Documentation	Add inline comments, maintain a clear README, and use tools like Swagger or DRF’s built-in docs
Tasks
0. Project set up
mandatory
Objective: create a new django project and install django rest framework

Instructions:

Initialize a new django project django-admin startproject messaging_app

Install django REST Framework and set it up in the settings.py

Create a new app for the messaging functionality. (python manage.py startapp chats)

Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
File: messaging_app/*
1. Define data Models
mandatory
Objective: Design the models for users, messages, and conversations.

Instructions:

Using the tables definition described above,

Create the user Model an extension of the Abstract user for values not defined in the built-in Django User model
Create the conversation model that tracks which users are involved in a conversation
Create the message model containing the sender, conversation as defined in the shared schema attached to this project
Database Specification

Entities and Attributes

User

    user_id (Primary Key, UUID, Indexed)
    first_name (VARCHAR, NOT NULL)
    last_name (VARCHAR, NOT NULL)
    email (VARCHAR, UNIQUE, NOT NULL)
    password_hash (VARCHAR, NOT NULL)
    phone_number (VARCHAR, NULL)
    role (ENUM: 'guest', 'host', 'admin', NOT NULL)
    created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
Message

    message_id (Primary Key, UUID, Indexed)
    sender_id (Foreign Key, references User(user_id))
    message_body (TEXT, NOT NULL)
    sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
Conversation

conversation_id (Primary Key, UUID, Indexed)
participants_id (Foreign Key, references User(user_id)
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
Constraints:

    User Table: Unique constraint on email, non-null constraints on required fields.
    Property Table: Foreign key constraint on host_id, non-null constraints on essential attributes.
    Booking Table: Foreign key constraints on property_id and user_id, status must be one of pending, confirmed, or canceled.
    Payment Table: Foreign key constraint on booking_id, ensuring payment is linked to valid bookings.
    Review Table: Constraints on rating values and foreign keys for property_id and user_id.
    Message Table: Foreign key constraints on sender_id and recipient_id.
Indexing:

**Primary Keys:** Indexed automatically.
**Additional Indexes:** Indexes on email (User), property_id (Property and Booking), and booking_id (Booking and Payment)
Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
File: messaging_app/chats/models.py
2. Create serializers to define the many to many relationships
mandatory
Objective: build serializers for the models

Instructions:

Create Serializers for Users, conversation and message

Ensure nested relationships are handled properly, like including messages within a conversation

Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
File: messaging_app/chats/serializers.py
3. Build api endpoints with views
mandatory
Objective: implement API endpoints for conversations and messages

Instructions:

Using viewsets from rest-framework Create viewsets for listing conversations (ConversationViewSet) and messages (MessageViewSet)

Implement the endpoints to create a new conversation and send messages to an existing one

Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
File: messaging_app/chats/views.py
4. Set up url routing
mandatory
Objective: configure URLS for the conversations and messages

Instructions:

Using Django rest framework DefaultRouter to automatically create the conversations and messages for your viewsets

Navigate to the main project’s urls.py i.e messaging_app/urls.py and include your created routes with path as api

Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
File: messaging_app/chats/urls.py
5. Run the application to fix errors
mandatory
Objective: run and test the applications

Instructions:

Run python manage.py makemigrations, python manage.py migrate, python manage.py runserver to test and run the application

Fix any error or bugs produced

Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
6. Manual Review
mandatory
Repo:

GitHub repository: alx-backend-python
Directory: messaging_app
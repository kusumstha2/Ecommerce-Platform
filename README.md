# Main System Overview
### Introduction
- The main system of this project is a Django-powered platform designed to manage all core features for the application. The system includes user authentication with JWT and login with Google, data processing, real-time notifications, payment management , and more, depending on the specific purpose of the project.


### Installation
- Prerequisites
- Python 3.x
- Django

- Celery 
- Install Redis locally or use a hosted service like Redis Labs.


### Apply migrations
- py manage.py makemigrations
- py manage.py migrate

### Create superuser
- py manage.py createsuperuser

### To run server
- py manage.py runserver


### Set up a virtual environment:
- python -m venv env.
### Install Dependencies
- pip install -r requirements.txt

### Start the Redis server if you haven't already:
- redis-server

### Install Redis  and Celery dependencies:
- pip install redis django-redis

- pip install celery redis

### Start Celery worker in a separate terminal window:
- celery -A your_project_name worker --loglevel=info

### Fast Data Retrieval with Redis (Cache-Aside Approach)
- This project uses Redis to cache frequently accessed data, reducing database load and improving performance.

#### How It Works
- Check Redis for data (cache hit → return data).

- If not found (cache miss), fetch from the database, store in Redis, then return.


### Data Searching & Filtering System
- This project implements an efficient search and filtering system in Django, using Redis for full-text search and PostgreSQL (pgvector) for vector search.

### How It Works
- Client Request → The user searches for data.

- Django Server → Processes the request and queries the appropriate search system.

- Full-Text Search (Redis) → Used for fast text-based search.

- Response → Returns the relevant results to the client.

### Emailing 

- It uses emailing when a subscription is taken using CELERY

### For Notification 
- FCM token is saved

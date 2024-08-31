# Interests Chat Application

## Overview

This project is a minimal full-stack web application that demonstrates user authentication, interest management, and real-time chat functionality. The application is built using Django for the backend and Javascript for the frontend, with WebSockets used for real-time communication.

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **Interest Management**: Users can send, accept, or reject interest requests.
- **Real-Time Chat**: Users can chat with each other in real-time once an interest request is accepted. Chat icon will appear near the accepted requests and user can click the icon to chat with that user

## Technologies Used

- **Backend**: Django
- **Frontend**: Javascript
- **Real-Time Communication**: Django Channels and WebSockets
- **Database**: SQLite (default), but can be configured to use PostgreSQL or other databases

## Prerequisites

- Python 3.8+
- Django 4.0+
- Django Channels 4.0+
- Django REST Framework
- Redis (for channel layer in production)

## Installation

### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/G-Guru-Prasad/InterestsProject
    cd InterestsProject
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the project server:**

    ```bash
    daphne -p 8000 InterestsProject.asgi:application
    ```

## Configuration

### Django Settings

- **WebSocket Configuration:** Ensure that your `settings.py` includes the appropriate channel layer configuration if you're using Redis or other backend.

    ```python
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
    ```

- **ASGI Configuration:** Update `asgi.py` to include the routing for Django Channels.

    ```python
    import os
    import interestsapp.routing as routing
    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    from channels.security.websocket import AllowedHostsOriginValidator

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InterestsProject.settings')

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })
    ```

## Usage

1. **Register a new user**: Navigate to the registration page and create an account.
2. **Log in**: Use your credentials to log in.
3. **Send interest requests**: Browse the user list and send interest requests.
4. **Accept/Reject interests**: View received interests and take action.
5. **Start chatting**: Once an interest is accepted, use the chat interface to communicate in real-time.

## Testing

To run tests for the Django application:

```bash
python manage.py test
```

## User Interface Notes

1. User should accept the request to chat with a person
2. Once accepted, user will see chat icon near the request
3. User will be able to send message by clicking send or by clicking 'Enter'
4. User will also be able to send chats in real time 

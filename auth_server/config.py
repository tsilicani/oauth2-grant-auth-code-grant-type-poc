import os
from datetime import timedelta

# Authorization server configuration
AUTH_SERVER_HOST = "localhost"
AUTH_SERVER_PORT = 8000
AUTH_SERVER_URL = f"http://{AUTH_SERVER_HOST}:{AUTH_SERVER_PORT}"

# Client application configuration (normally this would be in a database)
REGISTERED_CLIENTS = {
    "client123": {
        "client_secret": "secret123",
        "redirect_uris": ["http://localhost:8002/callback"]
    }
}

# Mock user database (in a real app, this would be in a secure database)
USERS = {
    "user123": {
        "password": "password123",
        "name": "Test User"
    }
}

# Token settings
TOKEN_EXPIRATION = timedelta(minutes=60)

# In-memory storage for authorization codes and tokens
auth_codes = {}  # Format: {code: {"client_id": "...", "user_id": "...", "redirect_uri": "..."}}
access_tokens = {}  # Format: {token: {"client_id": "...", "user_id": "..."}}

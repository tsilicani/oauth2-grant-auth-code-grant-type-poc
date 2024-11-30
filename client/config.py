import os

# Client application configuration
CLIENT_HOST = "localhost"
CLIENT_PORT = 8002
CLIENT_URL = f"http://{CLIENT_HOST}:{CLIENT_PORT}"

# OAuth 2.0 client credentials
CLIENT_ID = "client123"
CLIENT_SECRET = "secret123"

# Authorization server endpoints
AUTH_SERVER_URL = "http://localhost:8000"
AUTHORIZATION_ENDPOINT = f"{AUTH_SERVER_URL}/authorize"
TOKEN_ENDPOINT = f"{AUTH_SERVER_URL}/token"

# Resource server endpoint
RESOURCE_SERVER_URL = "http://localhost:8001"
PROFILE_ENDPOINT = f"{RESOURCE_SERVER_URL}/api/profile"

# OAuth 2.0 settings
REDIRECT_URI = f"{CLIENT_URL}/callback"
SCOPE = "profile"  # Not used in this simple implementation

import os

# Resource server configuration
RESOURCE_SERVER_HOST = "localhost"
RESOURCE_SERVER_PORT = 8001
RESOURCE_SERVER_URL = f"http://{RESOURCE_SERVER_HOST}:{RESOURCE_SERVER_PORT}"

# Authorization server configuration
AUTH_SERVER_URL = "http://localhost:8000"

# Mock protected resources (in a real app, this would be in a database)
PROTECTED_RESOURCES = {
    "user123": {
        "name": "Test User",
        "email": "test@example.com",
        "profile": "This is a protected resource for Test User"
    }
}

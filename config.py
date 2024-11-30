# Server configurations
HOST = "localhost"

# Authorization server
AUTH_SERVER_PORT = 8123
AUTH_SERVER_URL = f"http://{HOST}:{AUTH_SERVER_PORT}"

# Resource server
RESOURCE_SERVER_PORT = 8234
RESOURCE_SERVER_URL = f"http://{HOST}:{RESOURCE_SERVER_PORT}"

# Client application
CLIENT_PORT = 8345
CLIENT_URL = f"http://{HOST}:{CLIENT_PORT}"

# OAuth 2.0 endpoints
AUTHORIZATION_ENDPOINT = f"{AUTH_SERVER_URL}/authorize"
TOKEN_ENDPOINT = f"{AUTH_SERVER_URL}/token"
VERIFY_TOKEN_ENDPOINT = f"{AUTH_SERVER_URL}/verify_token"
PROFILE_ENDPOINT = f"{RESOURCE_SERVER_URL}/api/profile"
CALLBACK_ENDPOINT = f"{CLIENT_URL}/callback"

# OAuth 2.0 client credentials
CLIENT_ID = "client123"
CLIENT_SECRET = "secret123"

# Mock user database
USERS = {"tony": {"password": "passwordSuperSecret"}}

# Mock protected resources
PROTECTED_RESOURCES = {
    "tony": {
        "name": "Test User",
        "email": "test@example.com",
        "profile": "This is a protected resource for Test User",
    }
}

# Server configurations
HOST = "localhost"

# Authorization server
AUTH_SERVER_PORT = 8123
AUTH_SERVER_URL = f"http://{HOST}:{AUTH_SERVER_PORT}"

# Resource server
RESOURCE_SERVER_PORT = 8234

# Client application
CLIENT_PORT = 8345
CLIENT_URL = f"http://{HOST}:{CLIENT_PORT}"

# OAuth 2.0 endpoints
AUTHORIZATION_ENDPOINT = f"{AUTH_SERVER_URL}/authorize"
TOKEN_ENDPOINT = f"{AUTH_SERVER_URL}/token"
VERIFY_TOKEN_ENDPOINT = f"{AUTH_SERVER_URL}/verify_token"
CALLBACK_ENDPOINT = f"{CLIENT_URL}/callback"

# OAuth 2.0 client credentials
CLIENT_ID = "client123"
CLIENT_SECRET = "secret123"

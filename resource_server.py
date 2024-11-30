import jwt
from flask import Flask, jsonify, request

import config

# Mock protected resources
PROTECTED_RESOURCES = {
    "tony": {
        "name": "Test User",
        "email": "test@example.com",
        "profile": "This is a protected resource for Test User",
    }
}

# Load public key for verifying JWT
with open("public_key.pem", "r") as key_file:
    PUBLIC_KEY = key_file.read()

app = Flask(__name__)


def verify_token(token):
    """Verify the JWT access token using the public key"""
    try:
        decoded_token = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid


@app.route("/api/profile", methods=["GET"])
def get_profile():
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "missing_token"}), 401

    token = auth_header.split(" ")[1]

    # Verify token locally using public key
    token_info = verify_token(token)
    if not token_info:
        return jsonify({"error": "invalid_token"}), 401

    # Get user information
    user_id = token_info.get("user_id")
    if user_id not in PROTECTED_RESOURCES:
        return jsonify({"error": "user_not_found"}), 404

    # Return protected resource
    return jsonify(PROTECTED_RESOURCES[user_id])


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.RESOURCE_SERVER_PORT, debug=True)

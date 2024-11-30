import requests
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

app = Flask(__name__)


def verify_token(token):
    """Verify the access token with the authorization server"""
    response = requests.post(config.VERIFY_TOKEN_ENDPOINT, data={"token": token})
    return response.json() if response.status_code == 200 else None


def get_token_from_header():
    """Extract the access token from the Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ")[1]


@app.route("/api/profile", methods=["GET"])
def get_profile():
    # Extract token from Authorization header
    token = get_token_from_header()
    if not token:
        return jsonify({"error": "missing_token"}), 401

    # Verify token with authorization server
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

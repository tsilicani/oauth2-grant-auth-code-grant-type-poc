from flask import Flask, request, jsonify
import requests
import config

app = Flask(__name__)

def verify_token(token):
    """Verify the access token with the authorization server"""
    response = requests.post(
        f"{config.AUTH_SERVER_URL}/verify_token",
        data={"token": token}
    )
    return response.json() if response.status_code == 200 else None

def get_token_from_header():
    """Extract the access token from the Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]

@app.route('/api/profile', methods=['GET'])
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
    user_id = token_info.get('user_id')
    if user_id not in config.PROTECTED_RESOURCES:
        return jsonify({"error": "user_not_found"}), 404

    # Return protected resource
    return jsonify(config.PROTECTED_RESOURCES[user_id])

@app.route('/api/health', methods=['GET'])
def health_check():
    """Public endpoint for health checking"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(
        host=config.RESOURCE_SERVER_HOST,
        port=config.RESOURCE_SERVER_PORT,
        debug=True
    )

from flask import Flask, request, jsonify, render_template_string, redirect, session
import secrets
from datetime import datetime
import config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# HTML template for the login and consent page
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>OAuth 2.0 Authorization</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .form-group { margin-bottom: 15px; }
        input { padding: 8px; width: 100%; box-sizing: border-box; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Authorization Request</h2>
        <p>Client <strong>{{ client_id }}</strong> is requesting access to your account.</p>
        
        <form method="post">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <input type="submit" value="Authorize" class="btn">
        </form>
    </div>
</body>
</html>
'''

def generate_code():
    """Generate a secure random authorization code"""
    return secrets.token_urlsafe(32)

def generate_token():
    """Generate a secure random access token"""
    return secrets.token_urlsafe(32)

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        # Verify client_id and redirect_uri
        client_id = request.args.get('client_id')
        redirect_uri = request.args.get('redirect_uri')
        response_type = request.args.get('response_type')

        if not client_id or client_id not in config.REGISTERED_CLIENTS:
            return jsonify({"error": "invalid_client"}), 400

        if not redirect_uri or redirect_uri not in config.REGISTERED_CLIENTS[client_id]['redirect_uris']:
            return jsonify({"error": "invalid_redirect_uri"}), 400

        if response_type != 'code':
            return jsonify({"error": "unsupported_response_type"}), 400

        # Store request parameters in session
        session['client_id'] = client_id
        session['redirect_uri'] = redirect_uri

        # Show login form
        return render_template_string(LOGIN_TEMPLATE, client_id=client_id)

    elif request.method == 'POST':
        # Verify user credentials
        username = request.form.get('username')
        password = request.form.get('password')

        if not username in config.USERS or config.USERS[username]['password'] != password:
            return "Invalid credentials", 401

        # Generate authorization code
        auth_code = generate_code()
        
        # Store authorization code
        config.auth_codes[auth_code] = {
            "client_id": session['client_id'],
            "user_id": username,
            "redirect_uri": session['redirect_uri'],
            "expires_at": datetime.utcnow() + config.TOKEN_EXPIRATION
        }

        # Redirect back to client with auth code
        redirect_uri = session['redirect_uri']
        return redirect(f"{redirect_uri}?code={auth_code}")

@app.route('/token', methods=['POST'])
def token():
    # Verify client credentials
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    code = request.form.get('code')
    grant_type = request.form.get('grant_type')

    if not client_id or not client_secret:
        return jsonify({"error": "invalid_request"}), 400

    if client_id not in config.REGISTERED_CLIENTS or \
       config.REGISTERED_CLIENTS[client_id]['client_secret'] != client_secret:
        return jsonify({"error": "invalid_client"}), 401

    if grant_type != 'authorization_code':
        return jsonify({"error": "unsupported_grant_type"}), 400

    if not code or code not in config.auth_codes:
        return jsonify({"error": "invalid_grant"}), 400

    auth_code_data = config.auth_codes[code]
    
    # Verify the authorization code belongs to this client
    if auth_code_data['client_id'] != client_id:
        return jsonify({"error": "invalid_grant"}), 400

    # Verify the authorization code hasn't expired
    if datetime.utcnow() > auth_code_data['expires_at']:
        return jsonify({"error": "invalid_grant"}), 400

    # Generate access token
    access_token = generate_token()
    
    # Store token information
    config.access_tokens[access_token] = {
        "client_id": client_id,
        "user_id": auth_code_data['user_id'],
        "expires_at": datetime.utcnow() + config.TOKEN_EXPIRATION
    }

    # Remove used authorization code
    del config.auth_codes[code]

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": int(config.TOKEN_EXPIRATION.total_seconds())
    })

@app.route('/verify_token', methods=['POST'])
def verify_token():
    """Endpoint for resource server to verify access tokens"""
    token = request.form.get('token')
    
    if not token or token not in config.access_tokens:
        return jsonify({"error": "invalid_token"}), 401

    token_data = config.access_tokens[token]
    
    # Check if token has expired
    if datetime.utcnow() > token_data['expires_at']:
        del config.access_tokens[token]
        return jsonify({"error": "token_expired"}), 401

    return jsonify({
        "valid": True,
        "user_id": token_data['user_id'],
        "client_id": token_data['client_id']
    })

if __name__ == '__main__':
    app.run(host=config.AUTH_SERVER_HOST, port=config.AUTH_SERVER_PORT, debug=True)

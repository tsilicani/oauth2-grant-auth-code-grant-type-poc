from flask import Flask, redirect, request, session, render_template_string
import requests
import secrets
import config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# HTML template for the home page
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>OAuth 2.0 Client</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; }
        .profile { margin-top: 20px; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>OAuth 2.0 Client Application</h2>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        
        {% if not access_token %}
            <a href="{{ auth_url }}" class="btn">Login with OAuth</a>
        {% else %}
            <div class="profile">
                <h3>Protected Resource:</h3>
                <pre>{{ profile | tojson(indent=2) }}</pre>
                <a href="/logout" class="btn" style="background: #dc3545;">Logout</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    # Get profile data if we have an access token
    profile = None
    error = None
    
    if 'access_token' in session:
        # Try to fetch protected resource
        response = requests.get(
            config.PROFILE_ENDPOINT,
            headers={'Authorization': f"Bearer {session['access_token']}"}
        )
        if response.status_code == 200:
            profile = response.json()
        else:
            error = "Failed to fetch profile data"
            session.pop('access_token', None)

    # Generate authorization URL
    auth_url = (
        f"{config.AUTHORIZATION_ENDPOINT}"
        f"?response_type=code"
        f"&client_id={config.CLIENT_ID}"
        f"&redirect_uri={config.REDIRECT_URI}"
    )

    return render_template_string(
        HOME_TEMPLATE,
        auth_url=auth_url,
        access_token=session.get('access_token'),
        profile=profile,
        error=error
    )

@app.route('/callback')
def callback():
    # Get authorization code from query parameters
    code = request.args.get('code')
    if not code:
        return redirect('/')

    # Exchange authorization code for access token
    response = requests.post(
        config.TOKEN_ENDPOINT,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': config.REDIRECT_URI,
            'client_id': config.CLIENT_ID,
            'client_secret': config.CLIENT_SECRET,
        }
    )

    if response.status_code == 200:
        # Store the access token in session
        token_data = response.json()
        session['access_token'] = token_data['access_token']
    
    return redirect('/')

@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(
        host=config.CLIENT_HOST,
        port=config.CLIENT_PORT,
        debug=True
    )

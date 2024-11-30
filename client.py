from flask import Flask, redirect, render_template_string, request, session
import requests
import secrets

import config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OAuth 2.0 Client</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h2>OAuth 2.0 Client Application</h2>
        {% if error %}
            <div style="color: red; margin-bottom: 20px;">
                Error: {{ error }}
            </div>
        {% endif %}
        
        {% if not access_token %}
            <p>Click below to start the OAuth 2.0 Authorization Code Flow:</p>
            <a href="{{ auth_url }}" class="btn">Login with OAuth</a>
        {% else %}
            <p>Successfully authenticated!</p>
            <h3>Protected Resource:</h3>
            <pre>{{ protected_resource }}</pre>
            <form action="/logout" method="post" style="margin-top: 20px;">
                <input type="submit" value="Logout" class="btn" style="background: #dc3545;">
            </form>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    error = request.args.get("error")
    protected_resource = None

    # If we have an access token, try to get the protected resource
    if "access_token" in session:
        response = requests.get(
            config.PROFILE_ENDPOINT,
            headers={"Authorization": f"Bearer {session['access_token']}"},
        )
        if response.status_code == 200:
            protected_resource = response.json()
        else:
            error = "Failed to fetch protected resource"
            session.pop("access_token", None)

    # Build authorization URL
    auth_url = (
        f"{config.AUTHORIZATION_ENDPOINT}"
        f"?response_type=code"
        f"&client_id={config.CLIENT_ID}"
        f"&redirect_uri={config.CALLBACK_ENDPOINT}"
    )

    return render_template_string(
        HOME_TEMPLATE,
        auth_url=auth_url,
        access_token=session.get("access_token"),
        protected_resource=protected_resource,
        error=error,
    )


@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return redirect(f"/?error={error}")

    code = request.args.get("code")
    if not code:
        return redirect("/?error=missing_code")

    # Exchange authorization code for access token
    response = requests.post(
        config.TOKEN_ENDPOINT,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": config.CLIENT_ID,
            "client_secret": config.CLIENT_SECRET,
            "redirect_uri": config.CALLBACK_ENDPOINT,
        },
    )

    if response.status_code != 200:
        return redirect("/?error=token_exchange_failed")

    # Store the access token in session
    token_data = response.json()
    session["access_token"] = token_data["access_token"]

    return redirect("/")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("access_token", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.CLIENT_PORT, debug=True)

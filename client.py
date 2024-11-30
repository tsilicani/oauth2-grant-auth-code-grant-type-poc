import secrets

import requests
from flask import Flask, redirect, render_template_string, request, session

import config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OAuth 2.0 Client</title>
    <link rel="stylesheet" href="https://unpkg.com/boltcss/bolt.min.css" />
    <style>
        .flex-center {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .client-card {
            width: 100%;
            max-width: 600px;
        }
        .code {
            max-width: 100%;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <main class="flex-center">
        <div class="card client-card">
            <h2>OAuth 2.0 Client Application</h2>
            {% if error %}
                <div class="alert alert-error">
                    Error: {{ error }}
                </div>
            {% endif %}
            {% if not access_token %}
                <p>Click below to start the OAuth 2.0 Authorization Code Flow:</p>
                <a href="{{ auth_url }}" class="btn btn-primary">Login with OAuth</a>
            {% else %}
                <div class="alert alert-success">Successfully authenticated!</div>
                <h3>Protected Resource:</h3>
                <pre class="code">{{ protected_resource | tojson(indent=2) }}</pre>
                <form action="/logout" method="post" style="margin-top: 20px;">
                    <button type="submit" class="btn btn-error">Logout</button>
                </form>
            {% endif %}
        </div>
    </main>
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
            f"http://{config.HOST}:{config.RESOURCE_SERVER_PORT}/api/profile",
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

# OAuth 2.0 Authorization Code Grant Type Demo

A simple educational demonstration of the OAuth 2.0 Authorization Code Grant Type flow using Python and Flask.

## Overview

This project implements a complete OAuth 2.0 Authorization Code Grant Type flow with three components:
- Authorization Server (auth_server.py)
- Resource Server (resource_server.py)
- Client Application (client.py)

## Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Client as Client App<br/>(8345)
    participant Auth as Auth Server<br/>(8123)
    participant Resource as Resource Server<br/>(8234)

    User->>Client: Click Login with OAuth
    Client->>Auth: 1. Redirect to /authorize<br/>client_id, redirect_uri
    User->>Auth: 2. Enter credentials<br/>(tony/passwordSuperSecret)
    Auth->>Client: 3. Redirect with auth code
    Client->>Auth: 4. POST /token<br/>code, client_id, client_secret
    Auth->>Client: 5. Return access token
    Client->>Resource: 6. GET /api/profile<br/>Authorization: Bearer token
    Resource->>Auth: 7. Verify token
    Auth->>Resource: 8. Token valid, user_id
    Resource->>Client: 9. Return protected resource
    Client->>User: 10. Display data
```

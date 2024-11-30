# OAuth 2.0 Authorization Code Grant Type Demo

A simple educational demonstration of the OAuth 2.0 Authorization Code Grant Type flow using Python and Flask.

## Overview

This project implements a complete OAuth 2.0 Authorization Code Grant Type flow with three components:
- Authorization Server (auth_server.py)
- Resource Server (resource_server.py)
- Client Application (client.py)

## Enhanced Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Browser as Browser<br/>(Client UI)
    participant Client as Client Server<br/>(8345)
    participant Auth as Auth Server<br/>(8123)
    participant Resource as Resource Server<br/>(8234)
    User->>Browser: Click Login with OAuth
    Browser->>Auth: GET /authorize<br/>client_id, redirect_uri
    User->>Auth: Enter credentials<br/>(tony/passwordSuperSecret)
    Auth->>Browser: Redirect to client with auth code
    Note over Auth,Browser: Auth Code is a temporary code<br/>used to obtain an access token securely
    Browser->>Client: Send auth code to client server
    Client->>Auth: POST /token<br/>code, client_id, client_secret
    Auth->>Client: Return JWT access token
    Note over Client,Resource: JWT is used to<br/>access protected resources without exposing it in the URL
    Client->>Resource: GET /api/profile<br/>Authorization: Bearer JWT token
    Resource->>Resource: Verify JWT using public key
    Resource->>Client: Return protected resource
    Client->>Browser: Display data to user
```

This diagram illustrates the OAuth 2.0 flow, emphasizing the role of the authorization code in securely exchanging user credentials for an access token. It highlights the separation between the browser and client server, ensuring the access token is not exposed in the URL and is verified locally using a public key.

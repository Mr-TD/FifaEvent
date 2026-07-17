"""
StadiumIQ — Google OAuth Authentication Routes
Sign in with Google for personalized experience
"""

import json
import logging
import urllib.parse
import urllib.request

from flask import Blueprint, current_app, jsonify, redirect, request, session

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login")
def login():
    """Initiate Google OAuth flow.

    Redirects the user to Google's OAuth consent screen. Requires
    ``GOOGLE_OAUTH_CLIENT_ID`` to be set in the application config.

    Returns:
        Redirect to Google OAuth URL, or JSON error if not configured.
    """
    client_id = current_app.config.get("GOOGLE_OAUTH_CLIENT_ID", "")
    if not client_id:
        return jsonify({"error": "Google OAuth not configured", "message": "Set GOOGLE_OAUTH_CLIENT_ID in .env"}), 400

    redirect_uri = request.host_url.rstrip("/") + "/auth/callback"
    scope = "openid email profile"

    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
        f"response_type=code&"
        f"scope={urllib.parse.quote(scope)}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return redirect(auth_url)


@auth_bp.route("/auth/callback")
def callback():
    """Handle Google OAuth callback.

    Exchanges the authorization code for tokens, fetches user info,
    and stores it in the session.

    Returns:
        Redirect to the home page on success, or with an error parameter on failure.
    """
    code = request.args.get("code")
    if not code:
        return redirect("/?auth_error=no_code")

    client_id = current_app.config.get("GOOGLE_OAUTH_CLIENT_ID", "")
    client_secret = current_app.config.get("GOOGLE_OAUTH_CLIENT_SECRET", "")
    redirect_uri = request.host_url.rstrip("/") + "/auth/callback"

    # Exchange code for tokens
    try:
        token_data = urllib.parse.urlencode(
            {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
        ).encode()

        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=token_data)
        with urllib.request.urlopen(req) as response:
            tokens = json.loads(response.read().decode())

        # Get user info
        access_token = tokens.get("access_token", "")

        user_req = urllib.request.Request(
            "https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"}
        )
        with urllib.request.urlopen(user_req) as response:
            user_info = json.loads(response.read().decode())

        # Store in session
        session["user"] = {
            "name": user_info.get("name", ""),
            "email": user_info.get("email", ""),
            "picture": user_info.get("picture", ""),
            "id": user_info.get("id", ""),
        }
        session["logged_in"] = True

        return redirect("/")

    except Exception as e:
        logger.warning("OAuth error: %s", e)
        return redirect("/?auth_error=token_exchange")


@auth_bp.route("/auth/logout")
def logout():
    """Log out user by clearing session data."""
    session.pop("user", None)
    session.pop("logged_in", None)
    return redirect("/")


@auth_bp.route("/auth/status")
def auth_status():
    """Get current authentication status.

    Returns:
        JSON with ``logged_in`` boolean and user profile data if authenticated.
    """
    if session.get("logged_in"):
        return jsonify(
            {
                "logged_in": True,
                "user": session.get("user", {}),
            }
        )
    return jsonify({"logged_in": False})

# ----------------------------------------------
# MODULE auth - Authentication via SIAM API
# ----------------------------------------------

import json
import urllib.request
import urllib.error


API_URL = "https://www.cnm.es/users/siam/api/auth/login"
TIMEOUT = 10  # seconds


def authenticate(username, password):
    """
    Authenticate user against SIAM API.

    Sends a POST request with username (or email) and password.
    The API returns whether the login is correct and the username.

    Args:
        username: username or email
        password: user password

    Returns:
        dict with keys:
            - success (bool): True if authentication succeeded
            - username (str): the authenticated username (empty if failed)
            - message (str): status message
    """
    result = {
        "success": False,
        "username": "",
        "message": ""
    }

    payload = {
        "username": username,
        "password": password
    }

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)

            if response.status == 200:
                if data.get("success", False):
                    result["success"] = True
                    result["username"] = data.get("username", username)
                    result["message"] = "Login correct"
                else:
                    result["message"] = data.get("message", "Invalid credentials")
            else:
                result["message"] = data.get("message", f"Server error (HTTP {response.status})")

    except urllib.error.HTTPError as e:
        try:
            error_body = json.loads(e.read().decode("utf-8"))
            error_message = error_body.get("message", "")
        except Exception:
            error_message = ""
        if e.code == 401:
            result["message"] = error_message if error_message else "Invalid username or password"
        elif e.code == 403:
            result["message"] = error_message if error_message else "Access denied. Contact the laboratory manager."
        elif e.code == 404:
            result["message"] = error_message if error_message else "User not found"
        else:
            result["message"] = error_message if error_message else f"Server error (HTTP {e.code})"
    except urllib.error.URLError as e:
        result["message"] = f"Connection error: {e.reason}"
    except json.JSONDecodeError:
        result["message"] = "Invalid response from server"
    except Exception as e:
        result["message"] = f"Connection error: {str(e)}"

    return result

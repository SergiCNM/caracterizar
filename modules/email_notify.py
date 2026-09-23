# ----------------------------------------------
# MODULE email_notify - Send email notification
# via SIAM API with optional .dat attachment
# ----------------------------------------------

import json
import logging
import mimetypes
import os
import urllib.request
import urllib.error

DEFAULT_API_URL = "https://www.cnm.es/users/siam/api/email/process-notification"
TIMEOUT = 30  # seconds

log = logging.getLogger(__name__)


def _build_multipart_boundary():
    """Genera un boundary único para multipart/form-data."""
    import uuid
    return f"----WebKitFormBoundary{uuid.uuid4().hex}"


def send_email_notification(payload, dat_filepath=None, api_url=None):
    """
    Send email notification to SIAM API via multipart/form-data POST.

    Args:
        payload: dict with notification fields:
            - username, process_name, lot_name, wafer_name, mask_name,
              instrument, test, prober, wafermap, temperature, humidity,
              status (success/error), message, dice_measured, dice_total
        dat_filepath: optional path to .dat file to attach
        api_url: override default API URL (from config.toml)

    Returns:
        dict with keys:
            - success (bool): True if API accepted the request
            - message (str): status message
    """
    result = {
        "success": False,
        "message": ""
    }

    url = api_url if api_url else DEFAULT_API_URL
    log.info(f"Email notification -> {url} (attachment: {os.path.basename(dat_filepath) if dat_filepath else 'none'})")

    boundary = _build_multipart_boundary()
    body = b""

    # Add each field from payload as form data
    for key, value in payload.items():
        body += (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    # Add .dat file attachment if provided
    if dat_filepath and os.path.isfile(dat_filepath):
        filename = os.path.basename(dat_filepath)
        content_type, _ = mimetypes.guess_type(dat_filepath)
        if content_type is None:
            content_type = "text/plain"

        try:
            with open(dat_filepath, "rb") as f:
                file_data = f.read()
            body += (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8")
            body += file_data
            body += b"\r\n"
            log.debug(f"Attachment '{filename}' added ({len(file_data)} bytes)")
        except Exception as ex:
            msg = f"Error reading attachment: {ex}"
            log.error(msg)
            result["message"] = msg
            return result

    # Closing boundary
    body += f"--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )

    resp_body = ""
    resp_status = 0

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            resp_status = response.status
            content_type = response.getheader("Content-Type", "")
            resp_body = response.read().decode("utf-8", errors="replace")
            log.debug(f"HTTP {resp_status} | Content-Type: {content_type} | Body: {resp_body[:200]}")

            try:
                data = json.loads(resp_body)
            except json.JSONDecodeError:
                msg = f"Invalid JSON response (HTTP {resp_status}, Content-Type: {content_type}). Body: {resp_body[:300]}"
                log.warning(msg)
                result["message"] = msg
                return result

            if resp_status == 200:
                if data.get("success", False):
                    result["success"] = True
                    result["message"] = "Email notification sent"
                    log.info("Email notification sent successfully")
                else:
                    result["message"] = data.get("message", "Server rejected email")
            else:
                result["message"] = data.get("message", f"Server error (HTTP {resp_status})")

    except urllib.error.HTTPError as e:
        resp_status = e.code
        try:
            error_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            error_body = ""
        log.warning(f"HTTP Error {e.code}")

        try:
            error_data = json.loads(error_body)
            error_message = error_data.get("message", "")
        except Exception:
            error_message = ""
        result["message"] = error_message if error_message else f"HTTP error {e.code}"
    except urllib.error.URLError as e:
        msg = f"Connection error: {e.reason}"
        log.error(msg)
        result["message"] = msg
    except Exception as e:
        msg = f"Error sending notification: {str(e)}"
        log.error(msg)
        result["message"] = msg

    return result

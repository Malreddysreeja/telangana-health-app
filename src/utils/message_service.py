# src/utils/message_service.py

import os
from twilio.rest import Client

def send_health_message(recipient_number: str, message_body: str, via_whatsapp: bool = False):
    """
    Send health awareness messages via SMS or WhatsApp using Twilio API.

    Args:
        recipient_number (str): Phone number with country code (e.g., +919876543210)
        message_body (str): The message content to send.
        via_whatsapp (bool): If True, send via WhatsApp; otherwise via SMS.

    Returns:
        dict: API response or error message.
    """

    try:
        # Load credentials
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_phone = os.getenv("TWILIO_PHONE")

        if not all([account_sid, auth_token, twilio_phone]):
            return {"status": "error", "message": "Missing Twilio environment variables"}

        # Initialize client
        client = Client(account_sid, auth_token)

        # Format the "from_" and "to" numbers
        if via_whatsapp:
            from_number = f"whatsapp:{twilio_phone}"
            to_number = f"whatsapp:{recipient_number}"
        else:
            from_number = twilio_phone
            to_number = recipient_number

        # Send message
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        return {"status": "success", "sid": message.sid}

    except Exception as e:
        return {"status": "error", "message": str(e)}

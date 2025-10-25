# layers/whatsapp_handler.py
import requests
import json
import logging
from config import config

logger = logging.getLogger(__name__)


class WhatsAppHandler:
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/v17.0/{config.WHATSAPP_PHONE_NUMBER_ID}"
        self.headers = {
            "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        logger.info("📱 WhatsApp Handler initialized")

    def send_text_message(self, to, message):
        """Send text message via WhatsApp API"""
        if not config.WHATSAPP_TOKEN or config.WHATSAPP_TOKEN.startswith('your_'):
            logger.warning("⚠️  Cannot send message - WhatsApp token not configured")
            return None

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "text": {"body": message}
        }

        try:
            logger.info(f"📤 Sending message to {to}")
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info("✅ Message sent successfully")
                return response.json()
            else:
                logger.error(f"❌ Message send failed: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return None

    def process_webhook(self, data):
        """Process incoming webhook from WhatsApp"""
        try:
            logger.info("🔄 Processing webhook data...")

            # Extract the important parts from webhook data
            entry = data.get('entry', [])[0] if data.get('entry') else {}
            changes = entry.get('changes', [])[0] if entry.get('changes') else {}
            value = changes.get('value', {})

            # Check if this is a message
            if 'messages' in value:
                message = value['messages'][0]
                return self._process_message(message)
            else:
                logger.info("ℹ️  Webhook received but no messages found")
                return {'processed': False}

        except Exception as e:
            logger.error(f"❌ Webhook processing error: {e}")
            return {'processed': False, 'error': str(e)}

    def _process_message(self, message):
        """Process individual message from webhook"""
        try:
            message_type = message.get('type')
            sender = message.get('from')
            message_id = message.get('id')

            logger.info(f"💬 Received {message_type} message from {sender}")

            if message_type == 'text':
                text = message['text']['body']
                logger.info(f"📝 Message content: {text}")

                # Here we'll integrate with the bot logic later
                # For now, just acknowledge receipt
                response = f"Thanks for your message: '{text}'. Bot logic integration coming in Step 2.3!"
                self.send_text_message(sender, response)

                return {
                    'processed': True,
                    'message_type': 'text',
                    'sender': sender,
                    'content': text
                }

            elif message_type == 'image':
                logger.info("🖼️ Image message received")
                # Handle image messages (receipts)
                self.send_text_message(sender, "I received your image! Receipt processing coming soon.")
                return {
                    'processed': True,
                    'message_type': 'image',
                    'sender': sender
                }

            else:
                logger.info(f"ℹ️  Unhandled message type: {message_type}")
                self.send_text_message(sender,
                                       f"I received your {message_type} message. Currently I only process text and images.")
                return {
                    'processed': True,
                    'message_type': message_type,
                    'sender': sender
                }

        except Exception as e:
            logger.error(f"❌ Message processing error: {e}")
            return {'processed': False, 'error': str(e)}

    def mark_message_as_read(self, message_id):
        """Mark message as read in WhatsApp"""
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False
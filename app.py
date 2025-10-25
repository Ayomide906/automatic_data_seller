# app.py
from flask import Flask, request, jsonify
import logging
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config import config
from layers.whatsapp_handler import WhatsAppHandler
from layers.basic_handler import BasicMessageHandler

# Initialize Flask app
app = Flask(__name__)

# Initialize handlers
whatsapp_handler = WhatsAppHandler()
bot_handler = BasicMessageHandler()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Verify webhook for WhatsApp Business API
    This endpoint is called by WhatsApp during webhook setup
    """
    try:
        # Parse query parameters
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        logger.info(f"🔐 Webhook verification attempt: mode={mode}, token={token}")

        # Check if verification tokens match
        if mode == 'subscribe' and token == config.VERIFY_TOKEN:
            logger.info("✅ Webhook verified successfully!")
            return challenge
        else:
            logger.warning("❌ Webhook verification failed - token mismatch")
            return 'Verification failed', 403

    except Exception as e:
        logger.error(f"❌ Webhook verification error: {e}")
        return 'Server error', 500


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming WhatsApp messages
    This endpoint receives all messages from users
    """
    try:
        data = request.get_json()
        logger.info("📨 Received webhook data")

        if not data:
            logger.warning("❌ Empty webhook data received")
            return 'OK', 200

        # Process the webhook data
        result = whatsapp_handler.process_webhook(data)

        if result.get('processed'):
            logger.info(f"✅ Webhook processed: {result.get('message_type')} from {result.get('sender')}")
        else:
            logger.info("ℹ️  Webhook received but no message to process")

        return 'OK', 200

    except Exception as e:
        logger.error(f"❌ Webhook processing error: {e}")
        return 'OK', 200  # Always return OK to prevent retries


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'WhatsApp Data Seller Bot',
        'version': '1.0.0'
    })


@app.route('/')
def home():
    """Home page with bot information"""
    return """
    <h1>🤖 Automatic Data Seller Bot</h1>
    <p>Your WhatsApp bot is running and ready to receive messages!</p>
    <p><strong>Status:</strong> ✅ Active</p>
    <p><strong>Webhook:</strong> /webhook</p>
    <p><strong>Health Check:</strong> <a href="/health">/health</a></p>
    <hr>
    <p>Next: Configure WhatsApp Business API webhook to point to this server.</p>
    """
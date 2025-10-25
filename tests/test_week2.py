# test_week2.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from layers.whatsapp_handler import WhatsAppHandler
from app import app
from config import config


def test_week2_setup():
    print("🧪 Testing Week 2 Setup...")
    print("=" * 50)

    # Test 1: Flask app initialization
    try:
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200
            print("✅ Flask app health check: PASSED")
    except Exception as e:
        print(f"❌ Flask app health check: FAILED - {e}")

    # Test 2: WhatsApp handler initialization
    try:
        whatsapp = WhatsAppHandler()
        print("✅ WhatsApp handler initialization: PASSED")
    except Exception as e:
        print(f"❌ WhatsApp handler initialization: FAILED - {e}")

    # Test 3: Configuration check
    try:
        if config.WHATSAPP_TOKEN and not config.WHATSAPP_TOKEN.startswith('your_'):
            print("✅ WhatsApp token: CONFIGURED")
        else:
            print("⚠️  WhatsApp token: NOT CONFIGURED (expected for now)")

        if config.VERIFY_TOKEN and config.VERIFY_TOKEN != 'your_webhook_verify_token_here':
            print("✅ Verify token: CONFIGURED")
        else:
            print("❌ Verify token: NOT CONFIGURED - please set in .env")

        print("✅ Configuration check: PASSED")
    except Exception as e:
        print(f"❌ Configuration check: FAILED - {e}")

    # Test 4: Webhook verification simulation
    try:
        with app.test_client() as client:
            response = client.get('/webhook?hub.mode=subscribe&hub.verify_token=wrong_token')
            assert response.status_code == 403
            print("✅ Webhook verification (wrong token): PASSED")
    except Exception as e:
        print(f"❌ Webhook verification test: FAILED - {e}")

    print("=" * 50)
    print("🎉 Week 2 foundation tests completed!")
    print("📍 Next: Run the server and configure webhooks")


if __name__ == "__main__":
    test_week2_setup()
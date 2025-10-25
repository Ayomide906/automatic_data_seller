# run_week2.py
import logging
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

from models.database_models import init_db
from config import config
from app import app


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOGS_DIR / 'data_seller_week2.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point for Week 2"""
    print("🚀 Starting Week 2: WhatsApp Integration...")

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        logger.info("✅ Database initialized successfully!")

        # Check WhatsApp configuration
        logger.info("Checking WhatsApp configuration...")

        if not config.WHATSAPP_TOKEN or config.WHATSAPP_TOKEN.startswith('your_'):
            logger.warning("❌ WhatsApp token not configured - bot cannot send messages")
            print("\n⚠️  IMPORTANT: Update your .env file with:")
            print("   - REAL WhatsApp token")
            print("   - Phone Number ID (when you get new SIM)")
        else:
            logger.info("✅ WhatsApp token loaded")

        if not config.WHATSAPP_PHONE_NUMBER_ID or config.WHATSAPP_PHONE_NUMBER_ID.startswith('your_'):
            logger.warning("⚠️  Phone Number ID not configured - waiting for SIM")
        else:
            logger.info("✅ Phone Number ID loaded")

        # Display startup information
        logger.info(f"🌐 Server will run on: {config.HOST}:{config.PORT}")
        logger.info(f"🔐 Webhook URL: http://your-server.com/webhook")
        logger.info(f"🔑 Verify Token: {config.VERIFY_TOKEN}")

        print("\n" + "=" * 60)
        print("✅ WEEK 2 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("📝 Next Steps:")
        print("   1. Get your Phone Number ID (when you have SIM)")
        print("   2. Use ngrok for local testing: ngrok http 5000")
        print("   3. Configure WhatsApp webhook with ngrok URL")
        print("   4. Test with real WhatsApp messages!")
        print("=" * 60)

        # Start Flask server
        print(f"\n🌐 Starting Flask server on {config.HOST}:{config.PORT}...")
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            use_reloader=False
        )

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
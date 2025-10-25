
import logging
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from models.database_models import init_db
from config import config


def setup_logging():
    """Setup application logging - Windows compatible"""

    # Remove emojis for Windows compatibility
    class NoEmojiFormatter(logging.Formatter):
        def format(self, record):
            # Remove emojis from log messages
            emoji_cleanup = {
                '✅': '[OK]',
                '⚠️': '[WARN]',
                '📊': '[DB]',
                '📁': '[DIR]',
                '📝': '[LOG]',
                '🐛': '[DEBUG]',
                '🌐': '[WEB]'
            }

            message = super().format(record)
            for emoji, replacement in emoji_cleanup.items():
                message = message.replace(emoji, replacement)
            return message

    # Create formatter without emojis
    formatter = NoEmojiFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler (can keep emojis)
    file_handler = logging.FileHandler(config.LOGS_DIR / 'data_seller.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Console handler (no emojis for Windows)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )


def main():
    """Main application entry point"""
    print("🚀 Starting Automatic Data Seller Agent Setup...")

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        logger.info("✅ Database initialized successfully!")

        # Check critical configuration
        logger.info("Checking configuration...")

        if not config.WHATSAPP_TOKEN or config.WHATSAPP_TOKEN.startswith('your_'):
            logger.warning("⚠️  WhatsApp token not configured - bot cannot send messages yet")
        else:
            logger.info("✅ WhatsApp token loaded")

        if not config.WHATSAPP_PHONE_NUMBER_ID or config.WHATSAPP_PHONE_NUMBER_ID.startswith('your_'):
            logger.warning("⚠️  Phone Number ID not configured - waiting for SIM")
        else:
            logger.info("✅ Phone Number ID loaded")

        # Display startup information
        logger.info(f"📊 Database path: {config.DATABASE_URL}")
        logger.info(f"📁 Receipts directory: {config.RECEIPTS_DIR}")
        logger.info(f"📝 Logs directory: {config.LOGS_DIR}")
        logger.info(f"🐛 Debug mode: {config.DEBUG}")

        print("\n" + "=" * 50)
        print("✅ SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("📝 Next Steps:")
        print("   1. Get Phone Number ID when you have new SIM")
        print("   2. Build WhatsApp webhook handler (Week 2)")
        print("   3. Create NLP conversation engine (Week 3)")
        print("   4. Test with real customers!")
        print("=" * 50)

        # Start basic Flask server (placeholder for now)
        start_basic_server()

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        print(f"❌ Setup failed: {e}")
        sys.exit(1)


def start_basic_server():
    """Start a basic server - will be enhanced in Week 2"""
    print("\n🌐 Starting basic server (Webhook functionality coming in Week 2)...")
    print("   Server will be ready for WhatsApp webhooks after SIM setup")
    print("   For now, this confirms your environment is working!")

    # Simple check - we'll build the actual server in Week 2
    try:
        import flask
        print("✅ Flask is ready for web development")
    except ImportError as e:
        print(f"❌ Flask issue: {e}")


if __name__ == "__main__":
    main()
from config import config

print("🔧 Testing Configuration...")
print(f"Project Directory: {config.BASE_DIR}")
print(f"Receipts Folder: {config.RECEIPTS_DIR}")
print(f"Logs Folder: {config.LOGS_DIR}")
print(f"Database Folder: {config.DATABASES_DIR}")
print(f"Debug Mode: {config.DEBUG}")
print(f"Tesseract Path: {config.TESSERACT_PATH}")

# Check if WhatsApp token is loaded
if config.WHATSAPP_TOKEN and not config.WHATSAPP_TOKEN.startswith('your_'):
    print("✅ WhatsApp Token: LOADED (secure)")
else:
    print("❌ WhatsApp Token: MISSING or using placeholder")

print("✅ Configuration test completed!")
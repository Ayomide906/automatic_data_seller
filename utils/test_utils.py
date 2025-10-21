
from utils.general_utils import extract_phone_number, format_currency
from utils.bank_api_utils import BankVerifier
from datetime import datetime
print("🧪 Testing Utility Functions...")

# Test phone number extraction
test_texts = [
    "Buy data for 08012345678",
    "My number is 07098765432",
    "Recharge 08123456789",
    "No phone here"
]

for text in test_texts:
    phone = extract_phone_number(text)
    print(f"📞 '{text}' → {phone}")

# Test currency formatting
amounts = [300, 500.50, 1000, 2500.75]
for amount in amounts:
    formatted = format_currency(amount)
    print(f"💰 {amount} → {formatted}")

# Test bank verification
bank_verifier = BankVerifier()
result = bank_verifier.verify_transaction('GTB', 500.0, 'TXN123', datetime.now())
if result['verified']:
    print('valid transact')
else:
    print('scam')
print(f"🏦 Bank verification: {result}")
print("✅ Utility functions tested successfully!")
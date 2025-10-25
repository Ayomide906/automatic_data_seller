# layers/basic_handler.py
class BasicMessageHandler:
    """Basic message handler for MTN, GLO, and Airtel data business"""

    def __init__(self):
        # Define your actual data bundles and prices
        self.data_plans = {
            'MTN': {
                '1GB': {'price': 300, 'validity': '7 days'},
                '2GB': {'price': 500, 'validity': '30 days'},
                '5GB': {'price': 1000, 'validity': '30 days'},
                '10GB': {'price': 2000, 'validity': '30 days'}
            },
            'GLO': {
                '1GB': {'price': 280, 'validity': '7 days'},
                '2.5GB': {'price': 500, 'validity': '30 days'},
                '5GB': {'price': 950, 'validity': '30 days'},
                '10GB': {'price': 1900, 'validity': '30 days'}
            },
            'AIRTEL': {
                '1GB': {'price': 320, 'validity': '7 days'},
                '2GB': {'price': 550, 'validity': '30 days'},
                '5GB': {'price': 1100, 'validity': '30 days'},
                '10GB': {'price': 2100, 'validity': '30 days'}
            }
        }

    def handle_message(self, message_text, customer_phone):
        """Handle incoming messages for real data business"""
        message_lower = message_text.lower()

        # Basic responses for your actual business
        if any(word in message_lower for word in ['hi', 'hello', 'hey']):
            return self._get_welcome_message()

        elif any(network in message_lower for network in ['mtn', 'glo', 'airtel']):
            return self._get_network_plans(message_lower)

        elif 'data' in message_lower or 'bundle' in message_lower:
            return self._get_all_networks()

        elif 'price' in message_lower or 'how much' in message_lower:
            return self._get_pricing_info()

        elif 'buy' in message_lower or 'purchase' in message_lower or 'order' in message_lower:
            return self._get_purchase_instructions()

        elif 'thank' in message_lower:
            return "You're welcome! 😊 Let me know if you need more data bundles."

        else:
            return self._get_help_message()

    def _get_welcome_message(self):
        """Welcome message for your business"""
        return """Hello! Welcome to our Automated Data Service! 📱

I can help you buy data bundles for:
• *MTN* 
• *GLO*
• *Airtel*

Just tell me which network you need, or type *'data'* to see all bundles!"""

    def _get_all_networks(self):
        """Show all available networks and popular bundles"""
        message = "📊 *AVAILABLE DATA BUNDLES*\n\n"

        for network, plans in self.data_plans.items():
            message += f"*{network}:*\n"
            for plan, details in list(plans.items())[:2]:  # Show first 2 plans per network
                message += f"• {plan} - ₦{details['price']} ({details['validity']})\n"
            message += "\n"

        message += "Type *'MTN'*, *'GLO'*, or *'AIRTEL'* to see full plans!\n"
        message += "Or type *'buy'* for purchase instructions."

        return message

    def _get_network_plans(self, message):
        """Show plans for a specific network"""
        if 'mtn' in message:
            network = 'MTN'
        elif 'glo' in message:
            network = 'GLO'
        elif 'airtel' in message:
            network = 'AIRTEL'
        else:
            return "Please specify: MTN, GLO, or Airtel?"

        plans = self.data_plans[network]

        message = f"📶 *{network} DATA PLANS*\n\n"
        for plan, details in plans.items():
            message += f"• *{plan}* - ₦{details['price']} ({details['validity']})\n"

        message += f"\nTo buy {network} data, send:\n"
        message += f"'Buy {network} [size] for [phone number]'\n"
        message += f"Example: 'Buy {network} 2GB for 08012345678'"

        return message

    def _get_pricing_info(self):
        """Provide pricing information"""
        return """💰 *QUICK PRICE LIST*

*MTN:*
1GB - ₦300 | 2GB - ₦500 | 5GB - ₦1000 | 10GB - ₦2000

*GLO:*
1GB - ₦280 | 2.5GB - ₦500 | 5GB - ₦950 | 10GB - ₦1900

*AIRTEL:*
1GB - ₦320 | 2GB - ₦550 | 5GB - ₦1100 | 10GB - ₦2100

Type the network name (MTN, GLO, AIRTEL) for full details!"""

    def _get_purchase_instructions(self):
        """Instructions for purchasing data"""
        return """🛒 *HOW TO BUY DATA*

1. *Choose your network*: MTN, GLO, or Airtel
2. *Select bundle size*: 1GB, 2GB, 5GB, 10GB, etc.
3. *Provide phone number* to recharge

*Format:* 
'Buy [Network] [Size] for [Phone Number]'

*Examples:*
• 'Buy MTN 2GB for 08012345678'
• 'Buy GLO 1GB for 07098765432' 
• 'Buy Airtel 5GB for 08123456789'

I'll then provide payment details! 💳"""

    def _get_help_message(self):
        """Default help message"""
        return """I'm here to help you buy data bundles! 📱

You can ask me about:
• *Data bundles* - Type 'data' or 'MTN', 'GLO', 'Airtel'
• *Prices* - Type 'price' or 'how much'
• *How to buy* - Type 'buy' or 'purchase'
• *Specific networks* - Just say 'MTN', 'GLO', or 'Airtel'

What would you like to know? 😊"""

    def extract_order_details(self, message):
        """Extract network, size, and phone number from order message"""
        message_upper = message.upper()

        # Detect network
        network = None
        if 'MTN' in message_upper:
            network = 'MTN'
        elif 'GLO' in message_upper:
            network = 'GLO'
        elif 'AIRTEL' in message_upper:
            network = 'AIRTEL'

        # Detect data size
        sizes = ['1GB', '2GB', '5GB', '10GB', '2.5GB']
        size = None
        for s in sizes:
            if s in message_upper:
                size = s
                break

        # Extract phone number (simple 11-digit pattern)
        import re
        phone_match = re.search(r'(\d{11})', message)
        phone = phone_match.group(1) if phone_match else None

        return {
            'network': network,
            'size': size,
            'phone_number': phone
        }

    def simulate_conversation(self):
        """Simulate realistic conversations for your business"""
        test_conversations = [
            # Conversation 1: New customer
            [
                "hi",
                "data",
                "mtn",
                "buy mtn 2gb for 08012345678"
            ],
            # Conversation 2: Price inquiry
            [
                "hello",
                "how much for glo data",
                "buy glo 1gb for 07098765432"
            ],
            # Conversation 3: Direct purchase
            [
                "I want to buy airtel 5gb for 08123456789"
            ]
        ]

        print("🤖 SIMULATING REAL BUSINESS CONVERSATIONS")
        print("=" * 50)

        for i, conversation in enumerate(test_conversations, 1):
            print(f"\n💬 CONVERSATION {i}:")
            print("-" * 30)

            for msg in conversation:
                print(f"Customer: {msg}")
                response = self.handle_message(msg, "+2348000000000")
                print(f"Bot: {response}")

                # Test order extraction for purchase messages
                if 'buy' in msg.lower():
                    order_details = self.extract_order_details(msg)
                    print(f"📦 Order extracted: {order_details}")

                print("-" * 30)
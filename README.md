# 🤖 Automatic Data Seller Agent

A sophisticated WhatsApp bot platform for automated data vending businesses. Built with Python, Flask, and WhatsApp Business API.

## 🎯 Project Vision

Transform WhatsApp into a 24/7 automated data store that processes orders, verifies payments, and delivers data bundles automatically.

## 📦 Current Status: Week 1 Complete ✅

### What's Built So Far:
- **✅ Foundation**: Project structure, virtual environment, dependencies
- **✅ Database**: SQLite with customers, products, orders, transactions
- **✅ Configuration**: Secure environment variable management
- **✅ Utilities**: Image processing, bank verification, web automation
- **✅ Testing**: Comprehensive test suite for all components
- **✅ Basic Bot**: Simple conversation handler (placeholder for NLP)

### Sample Data Included:
- 1GB Data Bundle - ₦300 (7 days)
- 2GB Data Bundle - ₦500 (30 days) 
- 5GB Data Bundle - ₦1000 (30 days)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (recommended)
- WhatsApp Business API account
- Tesseract OCR installed

### Installation
```bash
# 1. Clone and setup
git clone <your-repo>
cd automatic_data_seller
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your actual credentials

# 4. Initialize database
python run.py
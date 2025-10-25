# test_database.py
from models.database_models import init_db, SessionLocal, Product
print("🧪 Testing Database Setup...")
try:
    # Initialize the database
    init_db()
    print("✅ Database tables created successfully!")

    # Test if we can query products
    db = SessionLocal()
    products = db.query(Product).all()
    print(f"✅ Found {len(products)} sample products in database")

    # Show the products
    for product in products:
        print(f"   - {product.name}: ₦{product.price} ({product.data_size})")

    db.close()
    print("🎉 Database setup completed successfully!")

except Exception as e:
    print(f"❌ Database setup failed: {e}")
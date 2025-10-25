# models/database_models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship  # ← UPDATED IMPORT
from datetime import datetime
from config import config

# Create engine and session
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    name = Column(String(100), nullable=True)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    total_purchases = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    data_size = Column(String(20))  # e.g., "1GB", "2GB", "5GB"
    validity_period = Column(String(50))  # e.g., "7 days", "30 days"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    amount_paid = Column(Float)
    phone_to_recharge = Column(String(20))
    status = Column(String(50), default="pending")  # pending, paid, processing, completed, failed
    transaction_reference = Column(String(100), nullable=True)
    receipt_image_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    transactions = relationship("Transaction", back_populates="order")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    bank_reference = Column(String(100))
    amount = Column(Float)
    transaction_date = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))  # receipt_scan, bank_api, manual
    bank_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="transactions")


class ConversationState(Base):
    __tablename__ = "conversation_states"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), index=True)
    state = Column(String(100))  # greeting, product_inquiry, order_creation, payment_waiting, etc.
    context_data = Column(Text)  # JSON string storing conversation context
    last_updated = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database with sample data"""
    Base.metadata.create_all(bind=engine)

    # Create sample products
    db = SessionLocal()
    try:
        # Check if products already exist
        existing_products = db.query(Product).count()
        if existing_products == 0:
            sample_products = [
                Product(
                    name="1GB Data Bundle",
                    description="1GB data valid for 7 days",
                    price=300.0,
                    data_size="1GB",
                    validity_period="7 days",
                    stock_quantity=100
                ),
                Product(
                    name="2GB Data Bundle",
                    description="2GB data valid for 30 days",
                    price=500.0,
                    data_size="2GB",
                    validity_period="30 days",
                    stock_quantity=50
                ),
                Product(
                    name="5GB Data Bundle",
                    description="5GB data valid for 30 days",
                    price=1000.0,
                    data_size="5GB",
                    validity_period="30 days",
                    stock_quantity=25
                )
            ]
            db.add_all(sample_products)
            db.commit()
            print("Sample products added to database.")
        else:
            print("Products already exist in database.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


def get_db():
    """Database dependency for FastAPI style (can be adapted for Flask)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
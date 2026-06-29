from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship("Account", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    investments = relationship("Investment", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_name = Column(String(100))
    account_type = Column(String(50))  # savings, credit, wallet, etc.
    balance = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    raw_name = Column(String(255))
    normalized_name = Column(String(255), index=True)
    category = Column(String(100))

    transactions = relationship("Transaction", back_populates="merchant")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=True)

    date = Column(DateTime, nullable=False)
    description = Column(String(500))
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20))  # debit/credit
    category = Column(String(100))
    payment_method = Column(String(50))
    confidence_score = Column(Float, default=0.0)

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=False)
    month = Column(String(7))  # format: YYYY-MM
    planned_amount = Column(Float, nullable=False)
    actual_amount = Column(Float, default=0.0)

    user = relationship("User", back_populates="budgets")


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_name = Column(String(150))
    asset_type = Column(String(50))  # stock, mutual fund, crypto, etc.
    sector = Column(String(100))
    invested_amount = Column(Float)
    current_value = Column(Float)
    purchase_date = Column(DateTime)

    user = relationship("User", back_populates="investments")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String(150))
    billing_cycle = Column(String(20))  # monthly, yearly
    amount = Column(Float)
    last_billed_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    reasoning = Column(Text)
    impact_score = Column(Float)
    urgency = Column(String(20))  # low, medium, high
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(255))
    generated_at = Column(DateTime, default=datetime.utcnow)
    health_score = Column(Float)
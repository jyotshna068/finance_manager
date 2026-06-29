from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.models import User, Account
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, name: str, email: str, password: str) -> User:
    """Creates a new user with a securely hashed password."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("A user with this email already exists.")

    user = User(name=name, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Validates email/password combination. Returns None if invalid."""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_account(db: Session, user_id: int, account_name: str, account_type: str, currency: str = "INR") -> Account:
    """Creates a financial account (savings, credit, wallet, etc.) for a user."""
    account = Account(
        user_id=user_id,
        account_name=account_name,
        account_type=account_type,
        currency=currency,
        balance=0.0,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_user_accounts(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()
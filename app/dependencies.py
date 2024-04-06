from passlib.context import CryptContext


from app.db.database import SessionLocal


pwd_context = CryptContext(schemes=['bcrypt'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

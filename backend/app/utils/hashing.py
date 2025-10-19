from passlib.context import CryptContext # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Clean and truncate password to bcrypt's safe limit (72 bytes)
    clean_password = password.strip()
    encoded = clean_password.encode("utf-8")
    if len(encoded) > 72:
        encoded = encoded[:72]
        clean_password = encoded.decode("utf-8", errors="ignore")
    return pwd_context.hash(clean_password)

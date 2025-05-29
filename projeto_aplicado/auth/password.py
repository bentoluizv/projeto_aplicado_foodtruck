from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.

    Raises:
        ValueError: If password is not a string or is empty.
    """
    if not isinstance(password, str):
        raise ValueError('Password must be a string')
    if not password:
        raise ValueError('Password cannot be empty')
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password (str): The password to verify.
        hashed_password (str): The hash to verify against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    if not isinstance(plain_password, str) or not isinstance(
        hashed_password, str
    ):
        return False
    if not plain_password or not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

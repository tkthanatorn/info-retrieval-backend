import bcrypt


def generate_hash(s: str) -> str:
    bytes = s.encode("utf-8")
    salt = bcrypt.gensalt(10)
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode("utf-8")


def compare_hash(s: str, hash: str) -> bool:
    bytes = s.encode("utf-8")
    return bcrypt.checkpw(bytes, hash.encode("utf-8"))

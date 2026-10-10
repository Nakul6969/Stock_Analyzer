import bcrypt

def hash_password(password):
    # Always return string so MongoDB stores it consistently
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode("utf-8")   # ← store as string in MongoDB

def verify_password(password, hashed):
    # Handle both string and bytes from MongoDB
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")  # ← convert string back to bytes
    return bcrypt.checkpw(password.encode(), hashed)


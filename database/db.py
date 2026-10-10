import os
import dns.resolver
from dotenv import load_dotenv
from pymongo import MongoClient

# Configure dnspython to use public DNS servers (Google / Cloudflare)
# This prevents "The resolution lifetime expired: The DNS operation timed out"
# when local Wi-Fi / hotspot DNS resolvers (e.g. 10.x.x.x) drop or time out on SRV records.
try:
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
except Exception:
    pass

load_dotenv()

MONGO_URI = None
try:
    import streamlit as st
    MONGO_URI = st.secrets.get("MONGO_URI")
except Exception:
    pass

if not MONGO_URI:
    MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in environment or secrets.toml")

# Set sensible timeouts so unreachable DB never hangs the Streamlit app indefinitely
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000
)

db = client["apex_auth"]

users_col = db["users"]

def check_db_health():
    """Quick check if MongoDB Atlas is reachable."""
    try:
        client.admin.command("ping")
        return True, ""
    except Exception as e:
        return False, str(e)


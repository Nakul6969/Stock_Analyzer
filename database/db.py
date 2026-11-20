import os
import time
import logging
import dns.resolver
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo.errors

logger = logging.getLogger(__name__)

# Configure dnspython to use public DNS servers (Google / Cloudflare)
# while preserving any container/system resolvers when available.
try:
    resolver = dns.resolver.Resolver()
    for ns in ["8.8.8.8", "1.1.1.1", "8.8.4.4"]:
        if ns not in resolver.nameservers:
            resolver.nameservers.append(ns)
    resolver.lifetime = 3.0
    dns.resolver.default_resolver = resolver
except Exception:
    try:
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ["8.8.8.8", "1.1.1.1", "8.8.4.4"]
        dns.resolver.default_resolver.lifetime = 3.0
    except Exception:
        pass

load_dotenv()

def get_mongo_uri() -> str | None:
    uri = None
    try:
        import streamlit as st
        if "MONGO_URI" in st.secrets:
            uri = st.secrets["MONGO_URI"]
        elif "mongo" in st.secrets and isinstance(st.secrets["mongo"], dict):
            uri = st.secrets["mongo"].get("URI") or st.secrets["mongo"].get("MONGO_URI")
    except Exception:
        pass

    if not uri:
        uri = os.getenv("MONGO_URI")

    if uri:
        uri = str(uri).strip().strip("'\"")

    return uri

MONGO_URI = get_mongo_uri()

_client = None
_db = None
_users_col = None
_db_init_error = None
_last_attempt_time = 0.0

def init_db(force: bool = False):
    global _client, _db, _users_col, _db_init_error, _last_attempt_time
    if _client is not None and _users_col is not None:
        return True

    now = time.time()
    if not force and _db_init_error and (now - _last_attempt_time) < 30.0:
        return False
    _last_attempt_time = now

    uri = get_mongo_uri()
    if not uri or "your_mongodb_atlas_connection_string" in uri:
        _db_init_error = "MONGO_URI is missing or unconfigured in Streamlit Secrets / .env"
        return False

    try:
        _client = MongoClient(
            uri,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
            socketTimeoutMS=3000
        )
        _db = _client["apex_auth"]
        _users_col = _db["users"]
        _db_init_error = None
        return True
    except pymongo.errors.ConfigurationError as ce:
        _db_init_error = f"MongoDB Configuration/DNS Error: {ce}"
        logger.warning(_db_init_error)
        return False
    except Exception as e:
        _db_init_error = f"MongoDB Connection Error: {e}"
        logger.warning(_db_init_error)
        return False

# Attempt immediate initialization safely; does not crash module on error
init_db(force=True)

class _UsersColProxy:
    """Proxy object ensuring users_col behaves like a MongoDB collection,
    while safely raising ConnectionFailure if the database is unreachable."""
    def __getattr__(self, name):
        global _users_col
        if _users_col is None:
            init_db()
        if _users_col is not None:
            return getattr(_users_col, name)
        raise pymongo.errors.ConnectionFailure(
            f"Database connection unavailable: {_db_init_error or 'MONGO_URI invalid or unreachable'}."
        )

    def __getitem__(self, item):
        global _users_col
        if _users_col is None:
            init_db()
        if _users_col is not None:
            return _users_col[item]
        raise pymongo.errors.ConnectionFailure(
            f"Database connection unavailable: {_db_init_error or 'MONGO_URI invalid or unreachable'}."
        )

class _ClientProxy:
    """Proxy object ensuring client behaves like a MongoClient instance."""
    def __getattr__(self, name):
        global _client
        if _client is None:
            init_db()
        if _client is not None:
            return getattr(_client, name)
        raise pymongo.errors.ConnectionFailure(
            f"MongoDB Client unavailable: {_db_init_error or 'Client could not be initialized'}."
        )

    def __getitem__(self, item):
        global _client
        if _client is None:
            init_db()
        if _client is not None:
            return _client[item]
        raise pymongo.errors.ConnectionFailure(
            f"MongoDB Client unavailable: {_db_init_error or 'Client could not be initialized'}."
        )

users_col = _UsersColProxy()
client = _ClientProxy()
db = _client["apex_auth"] if _client else None

def check_db_health():
    """Quick check if MongoDB Atlas is reachable."""
    if _db_init_error or _client is None:
        if not init_db():
            return False, _db_init_error or "MongoDB Client could not be initialized."
    try:
        _client.admin.command("ping")
        return True, ""
    except Exception as e:
        return False, str(e)




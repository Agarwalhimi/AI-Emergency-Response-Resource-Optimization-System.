import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database.db import init_db, init_auth_db, authenticate_user

init_db()
init_auth_db()

user = authenticate_user("admin@emergency.ai", "admin123")
assert user is not None
assert user["email"] == "admin@emergency.ai"
print("Authentication smoke test passed.")

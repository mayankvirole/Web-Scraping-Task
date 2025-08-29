import os
from twikit import Client

client = Client()

COOKIE_FILE = "cookies.json"      # Needed if Twitter asks
PHONE = None                     # Optional, if your account requires it


def ensure_login():
    """Ensure cookies exist and are valid, else log in."""
    try:
        if os.path.exists(COOKIE_FILE):
            client.load_cookies(COOKIE_FILE)
            print("✅ Loaded cookies from file.")
            return
        else:
            raise FileNotFoundError

    except Exception as e:
        print(f"⚠️ Cookie load failed: {e}. Logging in fresh...")

        # Correct usage with keyword args
        client.login(
            auth_info_1=USERNAME,
            password=PASSWORD,
            email=EMAIL,
            phone=PHONE,
        )

        # Save cookies for future runs
        client.export_cookies(COOKIE_FILE)
        print("✅ Logged in and saved cookies.")


# Run on import
ensure_login()
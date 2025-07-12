import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id   = int(os.getenv("TG_API_ID", 0))
api_hash = os.getenv("TG_API_HASH", "")
session  = os.getenv("SESSION_NAME", "s16_session")

_client = None
def get_client():
    global _client
    if _client is None:
        _client = TelegramClient(session, api_id, api_hash)
        _client.start()          # asks SMS + 2FA only once
    return _client

if __name__ == "__main__":
    with get_client() as c:
        me = c.get_me()
        print(f"connected → id={me.id}, username={me.username}")

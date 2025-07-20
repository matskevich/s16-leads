import os
import asyncio
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from dotenv import load_dotenv
from telethon.tl.types import User
from .limiter import safe_call, get_rate_limiter

load_dotenv()

# Безопасные пути для хранения данных
DATA_DIR = Path("data/sessions")
DATA_DIR.mkdir(parents=True, exist_ok=True)

api_id   = int(os.getenv("TG_API_ID", 0))
api_hash = os.getenv("TG_API_HASH", "")
session_name = os.getenv("SESSION_NAME", "s16_session")
session_path = str(DATA_DIR / session_name)

# Проверка конфигурации
if not api_id or not api_hash:
    raise ValueError("❌ Необходимо указать TG_API_ID и TG_API_HASH в .env файле")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = TelegramClient(session_path, api_id, api_hash)
    return _client

async def test_connection():
    """Тестирует подключение к Telegram API с anti-spam защитой"""
    try:
        client = get_client()
        await client.start()
        
        # Используем safe_call для get_me()
        me = await safe_call(client.get_me, operation_type="api")
        print(f"✅ Подключение успешно: {me.username} (ID: {me.id})")
        
        # Показываем статистику anti-spam системы
        limiter = get_rate_limiter()
        stats = limiter.get_stats()
        print(f"🛡️  Anti-spam статус: API calls: {stats['api_calls']}, RPS: {stats['current_rps']}")
        
        await client.disconnect()
        return True
    except SessionPasswordNeededError:
        print("❌ Требуется двухфакторная аутентификация")
        return False
    except PhoneCodeInvalidError:
        print("❌ Неверный код подтверждения")
        return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())

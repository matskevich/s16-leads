import asyncio
from typing import List, Optional, Dict, Any
from telethon import TelegramClient
from telethon.tl.types import User, Channel, Chat
from telethon.errors import ChatAdminRequiredError, FloodWaitError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import logging
from src.infra.limiter import safe_call, smart_pause

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroupManager:
    """Менеджер для работы с группами Telegram"""
    
    def __init__(self, client: TelegramClient):
        self.client = client
    
    async def get_group_info(self, group_identifier: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о группе
        
        Args:
            group_identifier: username группы (без @) или ID группы
            
        Returns:
            Словарь с информацией о группе или None
        """
        try:
            # Проверяем тип идентификатора
            if isinstance(group_identifier, int):
                # Это числовой ID группы
                entity = await safe_call(self.client.get_entity, group_identifier, operation_type="api")
            elif isinstance(group_identifier, str) and (group_identifier.startswith('-') and group_identifier[1:].isdigit()):
                # Это строковый ID группы
                entity = await safe_call(self.client.get_entity, int(group_identifier), operation_type="api")
            else:
                # Это username, добавляем @ если нужно
                if not group_identifier.startswith('@'):
                    group_identifier = '@' + group_identifier
                entity = await safe_call(self.client.get_entity, group_identifier, operation_type="api")
            
            if isinstance(entity, (Channel, Chat)):
                return {
                    'id': entity.id,
                    'title': entity.title,
                    'username': getattr(entity, 'username', None),
                    'participants_count': getattr(entity, 'participants_count', 0),
                    'type': 'channel' if isinstance(entity, Channel) else 'group'
                }
            
        except Exception as e:
            logger.error(f"Ошибка при получении информации о группе {group_identifier}: {e}")
            return None
    
    async def get_participants(self, group_identifier: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Получает список участников группы
        
        Args:
            group_identifier: username группы (без @) или ID группы
            limit: максимальное количество участников для получения
            
        Returns:
            Список словарей с информацией об участниках
        """
        participants = []
        
        try:
            # Получаем информацию о группе
            group_info = await self.get_group_info(group_identifier)
            if not group_info:
                logger.error(f"Не удалось найти группу: {group_identifier}")
                return []
            
            logger.info(f"Получаем участников группы: {group_info['title']}")
            
            # Определяем идентификатор для iter_participants
            if isinstance(group_identifier, int):
                group_id = group_identifier
            elif isinstance(group_identifier, str) and (group_identifier.startswith('-') and group_identifier[1:].isdigit()):
                group_id = int(group_identifier)
            else:
                group_id = group_identifier if group_identifier.startswith('@') else '@' + group_identifier
            
            # Получаем участников с anti-spam защитой
            count = 0
            async for user in self.client.iter_participants(group_id, limit=limit):
                if isinstance(user, User) and not user.bot:  # Исключаем ботов
                    participant_info = {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone': user.phone,
                        'is_bot': user.bot,
                        'is_verified': user.verified,
                        'is_premium': getattr(user, 'premium', False),
                        'status': str(user.status) if user.status else None
                    }
                    participants.append(participant_info)
                    count += 1
                    
                    # Smart pause каждые 1000 участников для предотвращения FLOOD_WAIT
                    if count % 1000 == 0:
                        await smart_pause("participants", count)
            
            logger.info(f"Получено {len(participants)} участников из группы {group_info['title']}")
            return participants
            
        except ChatAdminRequiredError:
            logger.error(f"Нет прав администратора для получения участников группы: {group_identifier}")
            return []
        except FloodWaitError as e:
            logger.error(f"Превышен лимит запросов. Ожидание {e.seconds} секунд")
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении участников группы {group_identifier}: {e}")
            return []
    
    async def search_participants(self, group_identifier: str, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Ищет участников в группе по запросу
        
        Args:
            group_identifier: username группы (без @) или ID группы
            query: поисковый запрос
            limit: максимальное количество результатов
            
        Returns:
            Список найденных участников
        """
        participants = []
        
        try:
            logger.info(f"Поиск участников в группе {group_identifier} по запросу: {query}")
            
            # Определяем идентификатор для iter_participants
            if isinstance(group_identifier, int):
                group_id = group_identifier
            elif isinstance(group_identifier, str) and (group_identifier.startswith('-') and group_identifier[1:].isdigit()):
                group_id = int(group_identifier)
            else:
                group_id = group_identifier if group_identifier.startswith('@') else '@' + group_identifier
            
            async for user in self.client.iter_participants(
                group_id, 
                search=query, 
                limit=limit
            ):
                if isinstance(user, User) and not user.bot:
                    participant_info = {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone': user.phone,
                        'is_bot': user.bot,
                        'is_verified': user.verified,
                        'is_premium': getattr(user, 'premium', False),
                        'status': str(user.status) if user.status else None
                    }
                    participants.append(participant_info)
            
            logger.info(f"Найдено {len(participants)} участников по запросу '{query}'")
            return participants
            
        except Exception as e:
            logger.error(f"Ошибка при поиске участников: {e}")
            return []
    
    async def export_participants_to_csv(self, group_identifier: str, filename: str, limit: int = 1000) -> bool:
        """
        Экспортирует список участников в CSV файл
        
        Args:
            group_identifier: username группы (без @) или ID группы
            filename: имя файла для сохранения
            limit: максимальное количество участников
            
        Returns:
            True если экспорт успешен, False в противном случае
        """
        import csv
        
        try:
            participants = await self.get_participants(group_identifier, limit)
            
            if not participants:
                logger.warning("Нет участников для экспорта")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'username', 'first_name', 'last_name', 'phone', 'is_verified', 'is_premium', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for participant in participants:
                    # Очищаем данные для CSV
                    clean_participant = {k: v for k, v in participant.items() if k in fieldnames}
                    writer.writerow(clean_participant)
            
            logger.info(f"Экспортировано {len(participants)} участников в файл {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при экспорте в CSV: {e}")
            return False 
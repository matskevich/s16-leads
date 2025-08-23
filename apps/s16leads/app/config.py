#!/usr/bin/env python3
"""
S16 Project Configuration Manager

Управляет конфигурацией специфичной для проекта S16,
включая настройки ключевых групп и логики сверки участников.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class S16Config:
    """Конфигурация для проекта S16-Leads"""
    
    def __init__(self):
        """Инициализация конфигурации S16 из переменных окружения"""
        
        # Основная группа s16 space (референсная)
        self.space_group_id: int = int(os.getenv('S16_SPACE_GROUP_ID', '-1002188344480'))
        self.space_group_name: str = os.getenv('S16_SPACE_GROUP_NAME', 's16 space')
        
        # Настройки сверки участников
        self.enable_cross_check: bool = self._get_bool('S16_ENABLE_CROSS_CHECK', True)
        self.mark_existing_members: bool = self._get_bool('S16_MARK_EXISTING_MEMBERS', True)
        self.export_comparison: bool = self._get_bool('S16_EXPORT_COMPARISON', True)
    
    def _get_bool(self, env_var: str, default: bool = False) -> bool:
        """Безопасное получение boolean значения из переменной окружения"""
        value = os.getenv(env_var, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_space_group_id(self) -> int:
        """Возвращает ID основной группы s16 space"""
        return self.space_group_id
    
    def get_space_group_name(self) -> str:
        """Возвращает название основной группы s16 space"""
        return self.space_group_name
    
    def is_cross_check_enabled(self) -> bool:
        """Проверяет включена ли сверка участников с s16 space"""
        return self.enable_cross_check
    
    def should_mark_existing_members(self) -> bool:
        """Проверяет нужно ли помечать существующих участников"""
        return self.mark_existing_members
    
    def should_export_comparison(self) -> bool:
        """Проверяет нужно ли экспортировать результаты сравнения"""
        return self.export_comparison
    
    def __str__(self) -> str:
        """Строковое представление конфигурации"""
        return f"""S16 Configuration:
- Space Group: {self.space_group_name} (ID: {self.space_group_id})
- Cross Check: {self.enable_cross_check}
- Mark Existing: {self.mark_existing_members}
- Export Comparison: {self.export_comparison}"""


# Глобальный экземпляр конфигурации
s16_config = S16Config()


def get_s16_config() -> S16Config:
    """Возвращает экземпляр конфигурации S16"""
    return s16_config


# Удобные функции для быстрого доступа
def get_space_group_id() -> int:
    """Быстрый доступ к ID группы s16 space"""
    return s16_config.get_space_group_id()


def get_space_group_name() -> str:
    """Быстрый доступ к названию группы s16 space"""
    return s16_config.get_space_group_name()


def is_cross_check_enabled() -> bool:
    """Быстрая проверка включена ли сверка участников"""
    return s16_config.is_cross_check_enabled() 
#!/usr/bin/env python3
"""
Скрипт синхронизации .env файла
==============================

Добавляет в .env недостающие ключи из env.sample
"""

import os
import sys


def sync_env():
    """Синхронизировать .env с env.sample"""
    
    env_sample = {}
    env_current = {}
    
    # Читаем .env.sample
    try:
        with open('.env.sample', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    env_sample[key] = line
    except FileNotFoundError:
        print('❌ .env.sample not found!')
        sys.exit(1)
    
    # Читаем текущий .env
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    env_current[key] = True
    except FileNotFoundError:
        # .env не существует - это нормально, он будет создан
        pass
    
    # Ищем недостающие ключи
    missing_keys = []
    for key in env_sample:
        if key not in env_current:
            missing_keys.append((key, env_sample[key]))
    
    # Добавляем недостающие ключи
    if missing_keys:
        print(f'📋 Found {len(missing_keys)} missing keys:')
        with open('.env', 'a') as f:
            f.write('\n# Added by make sync-env\n')
            for key, line in missing_keys:
                print(f'  + {key}')
                f.write(line + '\n')
        print('✅ Missing keys added to .env')
    else:
        print('✅ .env is up to date with .env.sample')


if __name__ == '__main__':
    sync_env() 
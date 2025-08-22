#!/usr/bin/env python3
"""
Gender Analysis Module for Telegram Users

Детерминированный скоринговый алгоритм для анализа пола пользователей Telegram.
Правила → Скоринг → Вывод. Без магии и угадайки.
"""

import re
import logging
from typing import Literal, Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

GenderType = Literal['male', 'female', 'unknown']

class GenderScorer:
    """Детерминированный скорер пола пользователей Telegram"""
    
    # Порог для принятия решения
    THRESHOLD = 40
    
    def __init__(self):
        """Инициализация словарей и правил"""
        
        # Русские женские имена
        self.ru_female_names = {
            'анна', 'аня', 'оля', 'ольга', 'софья', 'соня', 'алла', 'дарья', 'даша',
            'елизавета', 'лиза', 'алёна', 'катя', 'катерина', 'мария', 'марго',
            'василиса', 'надежда', 'тоня', 'катрин', 'дина', 'ирина', 'ира',
            'наталья', 'наташа', 'светлана', 'света', 'татьяна', 'таня',
            'екатерина', 'полина', 'юлия', 'юля', 'ксения', 'ксюша',
            'валерия', 'лера', 'виктория', 'вика', 'диана', 'кристина',
            'маргарита', 'рита', 'алина', 'вероника', 'милана', 'арина',
            # Добавлено из ручной классификации тантрических групп
            'салома', 'елизавета', 'саша', 'надежда', 'виктория',
            # Добавлено из второй партии классификации
            'дария', 'кили', 'юрга',
            # Добавлено из третьей партии (тантра)
            'u', 'ksenii', 'be_magica'
        }
        
        # Русские мужские имена
        self.ru_male_names = {
            'дима', 'дмитрий', 'илья', 'коля', 'николай', 'даниил', 'даня',
            'антон', 'андрей', 'леонид', 'руслан', 'виталий', 'михаил',
            'ростислав', 'павел', 'роман', 'макс', 'гриша', 'пётр', 'иван',
            'александр', 'саша', 'алексей', 'леша', 'евгений', 'женя',
            'артем', 'владимир', 'олег', 'сергей', 'юрий', 'ярослав',
            'денис', 'игорь', 'станислав', 'богдан', 'вадим', 'никита',
            'глеб', 'тимур', 'егор', 'артур', 'матвей', 'арсений',
            'тимофей', 'федор', 'семен', 'григорий', 'георгий', 'константин',
            'степан', 'эдуард', 'валерий', 'анатолий', 'борис', 'виктор',
            # Добавлено из ручной классификации тантрических групп
            'морис', 'руслан', 'андрей', 'ник', 'артем', 'коля',
            # Добавлено из второй партии классификации
            'михаил', 'морис', 'ник',
            # Добавлено из третьей партии (тантра)
            'matskevich', 'матскевич'
        }
        
        # Международные мужские имена
        self.en_male_names = {
            'mike', 'daniel', 'simon', 'jannik', 'pedro', 'max', 'nikolay',
            'ilya', 'arjun', 'wissam', 'leonid', 'rost', 'vitaly', 'alex',
            'alexander', 'andrew', 'anton', 'dmitry', 'eugene', 'ivan',
            'kirill', 'maxim', 'michael', 'oleg', 'pavel', 'roman',
            'sergey', 'vladimir', 'yuri', 'alexey', 'igor', 'stanislav',
            'bogdan', 'vadim', 'denis', 'nikita', 'gleb', 'timur', 'dima',
            'egor', 'arthur', 'john', 'james', 'robert', 'william',
            'david', 'richard', 'charles', 'joseph', 'thomas', 'christopher',
            'matthew', 'anthony', 'mark', 'donald', 'steven', 'paul',
            'joshua', 'kenneth', 'kevin', 'brian', 'george', 'timothy',
            # Добавлено из ручной классификации тантрических групп
            'ruslan', 'andrey', 'artem',
            # Добавлено из второй партии классификации
            'mikhail', 'morris', 'nik', 'moris'
        }
        
        # Международные женские имена
        self.en_female_names = {
            'anna', 'olga', 'alla', 'darya', 'sofya', 'elizaveta', 'alyona',
            'maria', 'katrin', 'margo', 'dina', 'katia', 'vasilisa', 'anya',
            'sonya', 'tania', 'liza', 'nastya', 'dasha', 'natasha', 'tanya',
            'ira', 'julia', 'lena', 'masha', 'vika', 'lera', 'kristina',
            'diana', 'alina', 'veronika', 'milana', 'anastasia', 'valeria',
            'victoria', 'ekaterina', 'elena', 'irina', 'ksenia', 'polina',
            'svetlana', 'tatiana', 'alexandra', 'margarita', 'mary',
            'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara',
            'susan', 'jessica', 'sarah', 'karen', 'nancy', 'lisa',
            # Добавлено из ручной классификации тантрических групп
            'oly', 'salome', 'elisaveta', 'sasha', 'nadezhda', 'tonya', 
            'viktoriya', 'olly', 'katya',
            # Добавлено из второй партии классификации
            'daria', 'kili', 'jurga',
            # Добавлено из третьей партии (тантра) 
            'u', 'ksenii', 'be_magica', 'ah_less', 'леся'
        }
        
        # Критические исключения - НЕ классифицировать по окончанию
        self.critical_exceptions = {
            'илья', 'даня', 'никита', 'женя', 'саша'
        }
    
    def analyze_gender(self, first_name: Optional[str] = None, 
                      last_name: Optional[str] = None,
                      username: Optional[str] = None,
                      display_name: Optional[str] = None,
                      bio: Optional[str] = None) -> Tuple[GenderType, List[str]]:
        """
        Анализирует пол пользователя по скоринговому алгоритму
        
        Returns:
            Tuple[GenderType, List[str]]: пол и список срабатываний
        """
        s_f = 0  # Female score
        s_m = 0  # Male score
        rationale = []  # Список срабатываний
        
        # Объединяем все текстовые данные для поиска явных меток
        all_text = ' '.join(filter(None, [first_name, last_name, username, display_name, bio]))
        
        # 1. ЯВНЫЕ МЕТКИ
        s_f, s_m, rationale = self._check_explicit_markers(all_text, s_f, s_m, rationale)
        
        # 2. РУССКАЯ ФАМИЛИЯ
        if last_name:
            s_f, s_m, rationale = self._check_russian_surname(last_name, s_f, s_m, rationale)
        
        # 3. ИМЯ (словарь + исключения)
        if first_name:
            s_f, s_m, rationale = self._check_name_dictionary(first_name, s_f, s_m, rationale)
        
        # 4. ЛОКАЛЬНЫЕ ХИНТЫ
        if first_name and last_name:
            s_f, s_m, rationale = self._check_local_hints(first_name, last_name, s_f, s_m, rationale)
        
        # 5. ПРИНЯТИЕ РЕШЕНИЯ
        decision, final_rationale = self._make_decision(s_f, s_m, rationale)
        
        logger.debug(f"Gender analysis: S_f={s_f}, S_m={s_m}, decision={decision}")
        logger.debug(f"Rationale: {final_rationale}")
        
        return decision, final_rationale
    
    def _normalize_name(self, name: Optional[str]) -> str:
        """Универсальная нормализация имен для кроссязыкового распознавания"""
        if not name:
            return ''
        
        # Убираем эмодзи (включая сердечки, флаги и т.д.)
        name_clean = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F900-\U0001F9FF]+', '', name)
        
        # Убираем остальные специальные символы, кроме букв и пробелов  
        name_clean = re.sub(r'[^\w\s]', '', name_clean)
        
        # Убираем лишние пробелы
        name_clean = re.sub(r'\s+', ' ', name_clean.strip()).lower()
        
        # Универсальная транслитерация русских имен
        cyrillic_to_latin = {
            # Основные соответствия
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 
            'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 
            'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        
        # Создаем варианты имени для поиска
        variants = [name_clean]
        
        # Если это кириллица, добавляем латинский вариант
        if any(ord(c) >= 1024 and ord(c) <= 1279 for c in name_clean):
            latin_variant = ''
            for char in name_clean:
                if char in cyrillic_to_latin:
                    latin_variant += cyrillic_to_latin[char]
                else:
                    latin_variant += char
            variants.append(latin_variant)
        
        # Специальные случаи транслитерации
        special_transliterations = {
            'мoris': 'морис',  # смешанные символы
            'мoрис': 'морис',
            'мöрис': 'морис',
            'ksenii': 'ксения',  # обратная транслитерация
            'ksenia': 'ксения',
            'dmitry': 'дмитрий',
            'dmitri': 'дмитрий',
            'dima': 'дима',
            'matskevich': 'матскевич',
        }
        
        # Проверяем специальные случаи
        for original, corrected in special_transliterations.items():
            if name_clean == original:
                variants.append(corrected)
        
        # Возвращаем первый вариант (основной нормализованный)
        return variants[0]
    
    def _get_name_variants(self, name: Optional[str]) -> List[str]:
        """Получает все возможные варианты имени для поиска"""
        if not name:
            return []
        
        # Базовая нормализация
        normalized = self._normalize_name(name)
        variants = [normalized]
        
        # Транслитерация кириллица <-> латиница
        cyrillic_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        
        latin_to_cyrillic = {v: k for k, v in cyrillic_to_latin.items() if v}
        
        # Если кириллица -> добавляем латиницу
        if any(ord(c) >= 1024 and ord(c) <= 1279 for c in normalized):
            latin_variant = ''
            for char in normalized:
                latin_variant += cyrillic_to_latin.get(char, char)
            variants.append(latin_variant)
        
        # Если латиница -> пробуем найти кириллический эквивалент
        else:
            # Простая обратная транслитерация для коротких имен
            if len(normalized) <= 8:  # только для коротких имен
                cyrillic_variant = ''
                i = 0
                while i < len(normalized):
                    # Проверяем двухбуквенные комбинации
                    if i < len(normalized) - 1:
                        two_char = normalized[i:i+2]
                        if two_char in latin_to_cyrillic:
                            cyrillic_variant += latin_to_cyrillic[two_char]
                            i += 2
                            continue
                    
                    # Однобуквенные
                    char = normalized[i]
                    cyrillic_variant += latin_to_cyrillic.get(char, char)
                    i += 1
                
                if cyrillic_variant != normalized:
                    variants.append(cyrillic_variant)
        
        # Добавляем известные варианты
        known_variants = {
            'dima': ['дима', 'dmitry', 'dmitri', 'дмитрий'],
            'дима': ['dima', 'dmitry', 'dmitri'],
            'ksenii': ['ксения', 'ksenia'],
            'ксения': ['ksenii', 'ksenia'],
            'ah_less': ['леся', 'олеся', 'лесь'],
            'леся': ['ah_less', 'олеся', 'lesia'],
        }
        
        for variant in variants[:]:  # копия списка для итерации
            if variant in known_variants:
                variants.extend(known_variants[variant])
        
        # Убираем дубликаты, сохраняем порядок
        seen = set()
        unique_variants = []
        for variant in variants:
            if variant and variant not in seen:
                seen.add(variant)
                unique_variants.append(variant)
        
        return unique_variants
    
    def _check_explicit_markers(self, text: str, s_f: int, s_m: int, rationale: List[str]) -> Tuple[int, int, List[str]]:
        """Проверка явных меток"""
        text_lower = text.lower()
        
        # Эмодзи
        if '♀️' in text:
            s_f += 100
            rationale.append("♀️ emoji (+100 female)")
        
        if '♂️' in text:
            s_m += 100
            rationale.append("♂️ emoji (+100 male)")
        
        # Прононсы
        female_pronouns = ['she/her', 'она', 'her/she']
        male_pronouns = ['he/him', 'он', 'him/he']
        neutral_pronouns = ['they/them', 'они']
        
        for pronoun in female_pronouns:
            if pronoun in text_lower:
                s_f += 100
                rationale.append(f"Pronoun '{pronoun}' (+100 female)")
        
        for pronoun in male_pronouns:
            if pronoun in text_lower:
                s_m += 100
                rationale.append(f"Pronoun '{pronoun}' (+100 male)")
        
        for pronoun in neutral_pronouns:
            if pronoun in text_lower:
                rationale.append(f"Neutral pronoun '{pronoun}' (no classification)")
        
        return s_f, s_m, rationale
    
    def _check_russian_surname(self, last_name: str, s_f: int, s_m: int, rationale: List[str]) -> Tuple[int, int, List[str]]:
        """Проверка русской фамилии"""
        surname_clean = re.sub(r'[^\w]', '', last_name.lower().strip())
        
        # Женские окончания
        female_endings = ['-ова', '-ёва', '-ева', '-ина', '-ына', '-ская']
        for ending in female_endings:
            suffix = ending[1:]  # убираем дефис
            if surname_clean.endswith(suffix) and len(surname_clean) > len(suffix):
                s_f += 70
                rationale.append(f"Russian female surname '{ending}' (+70 female)")
                return s_f, s_m, rationale
        
        # Мужские окончания
        male_endings = ['-ов', '-ев', '-ин', '-ын', '-ский']
        for ending in male_endings:
            suffix = ending[1:]  # убираем дефис
            if surname_clean.endswith(suffix) and len(surname_clean) > len(suffix):
                s_m += 50
                rationale.append(f"Russian male surname '{ending}' (+50 male)")
                return s_f, s_m, rationale
        
        return s_f, s_m, rationale
    
    def _check_name_dictionary(self, first_name: str, s_f: int, s_m: int, rationale: List[str]) -> Tuple[int, int, List[str]]:
        """Проверка имени по словарям с поддержкой вариантов"""
        # Получаем все варианты имени
        name_variants = self._get_name_variants(first_name)
        
        for variant in name_variants:
            # Берем первое слово для составных имен
            first_word = variant.split()[0] if variant else ''
            
            if not first_word:
                continue
            
            # Русские женские имена
            if first_word in self.ru_female_names:
                s_f += 80
                rationale.append(f"Russian female name '{first_word}' (+80 female)")
                return s_f, s_m, rationale
            
            # Русские мужские имена
            if first_word in self.ru_male_names:
                s_m += 80
                rationale.append(f"Russian male name '{first_word}' (+80 male)")
                return s_f, s_m, rationale
            
            # Международные мужские имена
            if first_word in self.en_male_names:
                s_m += 80
                rationale.append(f"International male name '{first_word}' (+80 male)")
                return s_f, s_m, rationale
            
            # Международные женские имена
            if first_word in self.en_female_names:
                s_f += 80
                rationale.append(f"International female name '{first_word}' (+80 female)")
                return s_f, s_m, rationale
        
        return s_f, s_m, rationale
    
    def _check_local_hints(self, first_name: str, last_name: str, s_f: int, s_m: int, rationale: List[str]) -> Tuple[int, int, List[str]]:
        """Проверка локальных хинтов"""
        name_clean = self._normalize_name(first_name)
        surname_clean = re.sub(r'[^\w]', '', last_name.lower().strip())
        
        first_word = name_clean.split()[0] if name_clean else ''
        
        # Критические исключения - НЕ классифицировать по окончанию
        if first_word in self.critical_exceptions:
            rationale.append(f"Critical exception '{first_word}' - no ending classification")
            return s_f, s_m, rationale
        
        # Если нет в словаре, но есть женская фамилия и имя на -а/-я
        if (first_word.endswith(('а', 'я')) and 
            len(first_word) > 2 and
            surname_clean.endswith(('ова', 'ева', 'ина', 'ына', 'ская'))):
            s_f += 30
            rationale.append(f"Russian name ending + female surname (+30 female)")
        
        # Испано-/португальские хинты (низкий вес)
        if first_word.endswith('o') and len(first_word) > 2:
            s_m += 20
            rationale.append(f"Spanish/Portuguese male ending '-o' (+20 male)")
        elif first_word.endswith('a') and len(first_word) > 2 and not first_word.endswith('ова'):
            s_f += 20
            rationale.append(f"Spanish/Portuguese female ending '-a' (+20 female)")
        
        return s_f, s_m, rationale
    
    def _make_decision(self, s_f: int, s_m: int, rationale: List[str]) -> Tuple[GenderType, List[str]]:
        """Принятие финального решения"""
        diff = abs(s_f - s_m)
        
        final_rationale = rationale.copy()
        final_rationale.append(f"Final scores: S_f={s_f}, S_m={s_m}, diff={diff}")
        
        if diff < self.THRESHOLD:
            final_rationale.append(f"Difference {diff} < threshold {self.THRESHOLD} → unknown")
            return 'unknown', final_rationale
        
        if s_f - s_m >= self.THRESHOLD:
            final_rationale.append(f"S_f - S_m = {s_f - s_m} ≥ {self.THRESHOLD} → female")
            return 'female', final_rationale
        
        if s_m - s_f >= self.THRESHOLD:
            final_rationale.append(f"S_m - S_f = {s_m - s_f} ≥ {self.THRESHOLD} → male")
            return 'male', final_rationale
        
        # Не должно достигаться
        final_rationale.append("Fallback → unknown")
        return 'unknown', final_rationale


# Глобальный экземпляр скорера
gender_scorer = GenderScorer()

def analyze_telegram_user_gender(first_name: Optional[str] = None, 
                                last_name: Optional[str] = None,
                                username: Optional[str] = None,
                                display_name: Optional[str] = None,
                                bio: Optional[str] = None) -> GenderType:
    """
    Удобная функция для анализа пола пользователя Telegram
    
    Returns:
        'male', 'female' или 'unknown'
    """
    result, _ = gender_scorer.analyze_gender(first_name, last_name, username, display_name, bio)
    return result

def analyze_telegram_user_gender_detailed(first_name: Optional[str] = None, 
                                         last_name: Optional[str] = None,
                                         username: Optional[str] = None,
                                         display_name: Optional[str] = None,
                                         bio: Optional[str] = None) -> Tuple[GenderType, List[str]]:
    """
    Детальный анализ пола пользователя с обоснованием
    
    Returns:
        Tuple[GenderType, List[str]]: пол и список срабатываний
    """
    return gender_scorer.analyze_gender(first_name, last_name, username, display_name, bio)

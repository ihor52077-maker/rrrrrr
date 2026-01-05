"""
Валидаторы для классификации и фильтрации данных
Функции для валидации, классификации и определения возраста данных
"""

импорт ре
from datetime import datetime, timedelta
из шаблонов импортировать (
    get_pattern_by_name, get_fake_patterns, REMOVED_EXTENSIONS, get_boilerplate_patterns
)

класс DataValidator:
    «Основной класс валидатора»
    
    def __init__(self):
        self.patterns = get_pattern_by_name(None)
        self.fake_patterns = get_fake_patterns()
        self.boilerplate_patterns = get_boilerplate_patterns()
        self.stats = {
            'total_input': 0,
            'after_dedup': 0,
            'removed_by_extension': 0,
            'removed_as_trash': 0,
            'removed_as_fake': 0,
            'removed_as_dead': 0,
            'critical_count': 0,
            'useful_count': 0,
            'weak_count': 0,
            'trash_count': 0,
            'tokens_count': 0,
            'crypto_count': 0,
            'email_pass_count': 0,
            'login_pass_count': 0,
            'configs_count': 0,
            'cookies_count': 0,
            'unknown_count': 0,
            'fresh_count': 0,
            'stale_count': 0,
            'old_count': 0,
            'unknown_age_count': 0,
            'dead_count': 0,
        }
    
    def validate_token(self, value):
        """Проверка формата токена"""
        если значение отсутствует:
            вернуть False
        если len(value) < 20:
            вернуть False
        если значение равно ' ':
            вернуть False
        вернуть True
    
    def validate_crypto(self, value):
        """Проверка формата криптографического ключа"""
        если значение отсутствует:
            вернуть False
        # Приватный ключ Ethereum (64 шестнадцатеричных символа)
        if re.match(r'^[a-fA-F0-9]{64}$', value):
            вернуть True
        # Формат PEM
        if value.startswith('-----BEGIN'):
            вернуть True
        return len(value) >= 32
    
    def validate_email_password(self, email, password):
        """Проверьте пару "email:password"""
        Если не адрес электронной почты или не пароль:
            вернуть False
        
        # Проверка формата электронной почты
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.strip()):
            вернуть False
        
        # Проверка пароля
        если len(password.strip()) < 8:
            вернуть False
        
        return not self.is_fake_value(password)
    
    def validate_login_password(self, login, password):
        """Проверьте пару логин:пароль"""
        Если нет логина или пароля:
            вернуть False
        
        если len(login.strip()) < 3:
            вернуть False
        
        если len(password.strip()) < 8:
            вернуть False
        
        return not self.is_fake_value(login) and not self.is_fake_value(password)
    
    def is_fake_value(self, value):
        """Проверка на наличие поддельного/тестового/демо-значения"""
        если значение отсутствует:
            вернуть True
        
        for pattern in self.fake_patterns:
            if pattern.search(value):
                вернуть True
        
        вернуть False
    
    def is_boilerplate(self, value):
        «Проверьте, является ли значение стандартным HTML/JS/CSS-кодом»
        если значение отсутствует:
            вернуть False
        
        for pattern in self.boilerplate_patterns:
            if pattern.search(value):
                вернуть True
        
        вернуть False
    
    def has_invalid_extension(self, value):
        «Проверьте, удалено ли расширение файла в значении»
        for ext in REMOVED_EXTENSIONS:
            if value.endswith(ext):
                вернуть True
        вернуть False
    
    def is_binary_garbage(self, value):
        «Проверка на наличие двоичного мусора»
        если значение отсутствует:
            вернуть False
        
        # Подсчет непечатаемых символов
        non_printable = sum(1 for c in value if ord(c) < 32 and c not in '\n\t\r')
        if non_printable > len(value) * 0.1: # Более 10% непечатаемых данных
            вернуть True
        
        вернуть False
    
    def classify_importance(self, data):
        Классифицируйте важность данных: КРИТИЧЕСКИЕ, ПОЛЕЗНЫЕ, СЛАБЫЕ, НЕНУЖНЫЕ"
        если это не данные:
            вернуть 'МУСОР'
        
        текст = str(data).lower()
        
        # Проверка на наличие КРИТИЧЕСКИХ шаблонов
        if any(pattern.search(text) for pattern in self.patterns.get('TOKENS', [])):
            self.stats['tokens_count'] += 1
            вернуть 'CRITICAL'
        
        if any(pattern.search(text) for pattern in self.patterns.get('CRYPTO', [])):
            self.stats['crypto_count'] += 1
            вернуть 'CRITICAL'
        
        # Проверка адреса электронной почты и пароля (КРИТИЧНО, если пароль действителен)
        email_pass_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}):([a-zA-Z0-9!@#$%^&*]{8,})'
        email_pass_match = re.search(email_pass_pattern, text)
        если email_pass_match:
            email, password = email_pass_match.groups()
            if self.validate_email_password(email, password):
                self.stats['email_pass_count'] += 1
                вернуть 'CRITICAL'
        
        # Проверка на наличие полезных шаблонов (логин:пароль, cookie, configs)
        if any(pattern.search(text) for pattern in self.patterns.get('COOKIES', [])):
            self.stats['cookies_count'] += 1
            вернуть 'ПОЛЕЗНО'
        
        if any(pattern.search(text) for pattern in self.patterns.get('CONFIGS', [])):
            self.stats['configs_count'] += 1
            вернуть 'ПОЛЕЗНО'
        
        login_pass_pattern = r'([a-zA-Z0-9._]+):([a-zA-Z0-9!@#$%^&*]{8,})'
        login_pass_match = re.search(login_pass_pattern, text)
        если login_pass_match:
            логин, пароль = login_pass_match.groups()
            if self.validate_login_password(login, password):
                self.stats['login_pass_count'] += 1
                вернуть 'ПОЛЕЗНО'
        
        # Проверьте наличие слабых закономерностей (электронные письма, имена пользователей)
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            вернуть 'СЛАБЫЙ'
        
        if re.search(r'https?://', ​​text):
            вернуть 'СЛАБЫЙ'
        
        self.stats['unknown_count'] += 1
        вернуть 'МУСОР'
    
    def determine_age(self, data):
        «Определите возраст данных: свежие, устаревшие, старые, неизвестные, неактуальные»
        если это не данные:
            вернуть 'неизвестно'
        
        текст = str(data)
        
        # Попытка извлечения даты
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})', # YYYY-MM-DD
            r'(\d{2})/(\d{2})/(\d{4})', # MM/DD/YYYY
            r'(\d{4})(\d{2})(\d{2})', # ГГГГММДД
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            если совпадение:
                пытаться:
                    if len(match.groups()[0]) == 4: # Формат ГГГГ
                        год, месяц, день = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    еще:
                        день, месяц, год = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    
                    дата = дата и время (год, месяц, день)
                    now = datetime.now()
                    days_old = (now - date).days
                    
                    если days_old < 30:
                        вернуть 'свежий'
                    elif days_old < 365:
                        вернуть 'устаревший'
                    еще:
                        вернуть 'старый'
                за исключением (ValueError, AttributeError):
                    продолжать
        
        # Проверка на наличие неработающих индикаторов
        if any(word in text.lower() for word in ['404', 'not found', 'removed', 'deleted', 'dead']):
            вернуть 'мертвый'
        
        вернуть 'неизвестно'
    
    def has_context(self, data, surrounding_data=None):
        «Проверьте, есть ли у секрета какой-либо контекст».
        если это не данные:
            вернуть False
        
        текст = str(data).lower()
        
        # Контекстные индикаторы
        context_indicators = [
            r'(имя пользователя|логин|пользователь|учетная запись)',
            r'(email|mail|@)',
            r'(url|link|http|domain)',
            r'(config|configuration|settings)',
            r'(база данных|db|mysql|postgres)',
        ]
        
        has_context = any(re.search(indicator, text) for indicator in context_indicators)
        возвращает has_context или surrounding_data не None

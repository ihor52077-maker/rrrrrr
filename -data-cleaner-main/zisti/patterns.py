"""
Регулярные выражения для классификации и обнаружения
Шаблоны для классификации секретов, токенов, криптографии и т.д.
"""

импорт ре

# Регулярные выражения для классификации
ШАБЛОНЫ = {
    'ТОКЕНЫ': [
        r'(?i)(token|auth|bearer|authorization)[\s=:]+([a-zA-Z0-9._\-]{20,})',
        r'(?i)(api.?key|apikey|api_key)[\s=:]+([a-zA-Z0-9\-_]{20,})',
        r'(?i)(access.?token|accesstoken)[\s=:]+([a-zA-Z0-9\-_.]{20,})',
        r'(?i)(github_token|github.?token)[\s=:]+([a-zA-Z0-9_]{20,})',
        r'(?i)(refresh.?token)[\s=:]+([a-zA-Z0-9\-_.]{20,})',
    ],
    
    'КРИПТО': [
        r'(?i)(privatekey|private_key|privkey|priv_key)[\s=:]+([a-fA-F0-9]{64})',
        r'^[a-fA-F0-9]{64}$',
        r'^-----BEGIN.*PRIVATE KEY-----',
        r'(?i)(0x)?[a-fA-F0-9]{40}$', # Адрес Ethereum
    ],
    
    'EMAIL_PASSWORD': [
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}):([a-zA-Z0-9!@#$%^&*(){}\[\]:;"\'<>,.?/\-_+=~`]{8,})',
    ],
    
    'LOGIN_PASSWORD': [
        r'(?i)(login|user|username)[\s=:]+([a-zA-Z0-9._]+)\s+(password|pass|pwd)[\s=:]+(.+)',
        r'([a-zA-Z0-9._]+):([a-zA-Z0-9!@#$%^&*(){}\[\]:;"\'<>,.?/\-_+=~`]{8,})',
    ],
    
    «ПЕЧЕНЬЕ»: [
        r'(?i)(phpsessid|sessionid|session.?id|cookie)[\s=:]+([a-zA-Z0-9\-_]{10,})',
        r'(?i)(jwt|jwttoken)[\s=:]+([a-zA-Z0-9\-_.]+)',
    ],
    
    'КОНФИГУРАЦИИ': [
        r'(?i)(db_password|database_password|mysql_password)[\s=:]+(.+)',
        r'(?i)(aws_access_key_id|aws_secret_access_key)[\s=:]+(.+)',
        r'(?i)(api_secret|secret_key|secret)[\s=:]+(.+)',
        r'(?i)(connection_string|connstr)[\s=:]+(.+)',
    ],
}

# Поддельные/проверочные значения для удаления
FAKE_VALUES = [
    r'(?i)(demo|test|example|sample|changeme|asdfghjk|notreal|dummy|fake|placeholder)',
    r'(?i)^(admin|root|guest|user|test|demo)$',
    r'^(password|123456|12345678|qwerty|abc123|password123|admin123|000000)$',
    r'^([a-z0-9]+@(example|test|localhost|sample)\.com)$',
]

# Расширения файлов для удаления
УДАЛЕННЫЕ_РАСШИРЕНИЯ = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', # Изображения
    '.mp4', '.avi', '.mkv', '.mov', '.webm', # Видео
    '.mp3', '.wav', '.aac', '.flac', '.m4a', # Аудио
    '.ttf', '.otf', '.woff', '.woff2', # Шрифты
}

# Шаблоны для удаления
BOILERPLATE_PATTERNS = [
    r'<!DOCTYPE',
    р'<html',
    р'<тело',
    р'<script',
    r'<style',
    r'function\s+\w+\s*\(',
    r'var\s+\w+\s*=',
    r'console\.log',
]

def get_pattern_by_name(pattern_name):
    """Получить скомпилированные шаблоны регулярных выражений по имени"""
    скомпилировано = {}
    для категории, шаблоны в PATTERNS.items():
        compiled[category] = [re.compile(p, re.MULTILINE) for p in patterns]
    возврат скомпилированный

def get_fake_patterns():
    """Получить собранные шаблоны фиктивных значений"""
    return [re.compile(p, re.MULTILINE | re.IGNORECASE) for p in FAKE_VALUES]

def get_boilerplate_patterns():
    """Получите скомпилированные шаблоны шаблонов"""
    return [re.compile(p, re.IGNORECASE) for p in BOILERPLATE_PATTERNS]

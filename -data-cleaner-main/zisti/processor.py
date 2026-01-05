Основной механизм обработки данных
11-этапный конвейер обработки данных
"""

импорт json
импорт ре
импорт zip-файла
импорт os
импорт csv
from datetime import datetime
импорт потоков
from validators import DataValidator

класс DataProcessor:
    «Главный процессор данных с 11-ступенчатым конвейером»
    
    def __init__(self):
        self.validator = DataValidator()
        self.stats = self.validator.stats.copy()
        self.current_stage = 0
        self.lock = threading.Lock()
    
    def load_file(self, filepath):
        """Загрузка данных из ZIP, JSON, TXT или CSV файла"""
        данные = []
        
        пытаться:
            if filepath.endswith('.zip'):
                with zipfile.ZipFile(filepath, 'r') as zf:
                    for file_info in zf.filelist:
                        if file_info.filename.endswith('.json'):
                            with zf.open(file_info as f:
                                content = json.load(f)
                                если isinstance(content, list):
                                    data.extend(content)
                                elif isinstance(content, dict):
                                    data.append(content)
                        elif file_info.filename.endswith(('.txt', '.csv')):
                            with zf.open(file_info as f:
                                для строки в f:
                                    line_str = line.decode('utf-8', errors='ignore').strip()
                                    если line_str:
                                        data.append({'match': line_str})
            
            elif filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = json.load(f)
                    если isinstance(content, list):
                        data.extend(content)
                    elif isinstance(content, dict):
                        data.append(content)
            
            elif filepath.endswith(('.txt', '.log')):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    для строки в f:
                        line_str = line.strip()
                        если line_str:
                            data.append({'match': line_str})
            
            elif filepath.endswith('.csv'):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    для строки в читателе:
                        data.append(row)
        
        за исключением исключения как e:
            print(f"Ошибка загрузки файла: {e}")
        
        возвращаемые данные
    
    def process(self, data, callbacks=None):
        """Выполнить 11-этапный конвейер"""
        callbacks = callbacks or {'log': print, 'progress': lambda x, y: None}
        
        self.stats['total_input'] = len(data)
        callbacks['log'](f"Загружено записей: {len(data)}")
        
        # Этап 1: Дедупликация
        self.current_stage = 1
        callbacks['log']("Этап 1: Дедупликация...")
        data = self.step_1_deduplication(data)
        self.stats['after_dedup'] = len(data)
        callbacks['progress'](1, 11)
        
        # Этап 2: Первичная очистка
        self.current_stage = 2
        callbacks['log']("Этап 2: Первичная очистка...")
        data = self.step_2_primary_cleanup(data)
        callbacks['progress'](2, 11)
        
        # Этап 3: Фильтр расширения
        self.current_stage = 3
        callbacks['log']("Этап 3: Фильтрация расширений...")
        data = self.step_3_extension_filter(data)
        callbacks['progress'](3, 11)
        
        Этап 4: Определение возраста
        self.current_stage = 4
        callbacks['log']("Этап 4: Определение возраста...")
        data = self.step_4_determine_age(data)
        callbacks['progress'](4, 11)
        
        Этап 5: Классификация
        self.current_stage = 5
        callbacks['log']("Этап 5: Классификация по важности...")
        classified = self.step_5_classify_importance(data)
        callbacks['progress'](5, 11)
        
        Этап 6: Валидация
        self.current_stage = 6
        callbacks['log']("Этап 6: Проверка...")
        classified = self.step_6_validate(classified)
        callbacks['progress'](6, 11)
        
        Этап 7: Удаление подделок
        self.current_stage = 7
        callbacks['log']("Этап 7: Удаление фейков...")
        classified = self.step_7_remove_fakes(classified)
        callbacks['progress'](7, 11)
        
        # Этап 8: Проверка контекста
        self.current_stage = 8
        callbacks['log']("Этап 8: Контекстная проверка...")
        classified = self.step_8_context_check(classified)
        callbacks['progress'](8, 11)
        
        Этап 9: Нормализация
        self.current_stage = 9
        callbacks['log']("Этап 9: Нормализация...")
        classified = self.step_9_normalize(classified)
        callbacks['progress'](9, 11)
        
        # Этап 10: Вторичная дедупликация
        self.current_stage = 10
        callbacks['log']("Этап 10: Вторичная дедупликация...")
        classified = self.step_10_secondary_dedup(classified)
        callbacks['progress'](10, 11)
        
        Этап 11: Финальная сортировка
        self.current_stage = 11
        callbacks['log']("Этап 11: Финальная сортировка...")
        classified = self.step_11_final_sort(classified)
        callbacks['progress'](11, 11)
        
        callbacks['log']("Обработка завершена!")
        
        # Обновить статистику
        for category in ['critical', 'useful', 'weak', 'trash']:
            self.stats[f'{category}_count'] = len(classified.get(category, []))
        
        возврат объявлений
    
    def step_1_deduplication(self, data):
        """Удалить точные и нормализованные дубликаты"""
        seen = set()
        результат = []
        
        для элемента в данных:
            match = str(item.get('match', '')).strip()
            normalized = match.lower().strip()
            
            если нормализованное значение не обнаружено и найдено:
                seen.add(normalized)
                result.append(item)
        
        удалено = len(данные) - len(результат)
        self.stats['removed_as_trash'] += removed
        вернуть результат
    
    def step_2_primary_cleanup(self, data):
        «Удалите короткие строки, двоичный мусор и шаблонный код»
        результат = []
        
        для элемента в данных:
            match = str(item.get('match', '')).strip()
            
            # Проверьте минимальную длину
            если длина совпадения < 8:
                self.stats['removed_as_trash'] += 1
                продолжать
            
            # Проверка на наличие двоичного мусора
            if self.validator.is_binary_garbage(match):
                self.stats['removed_as_trash'] += 1
                продолжать
            
            # Проверка на наличие шаблонного текста
            if self.validator.is_boilerplate(match):
                self.stats['removed_as_trash'] += 1
                продолжать
            
            # Проверка на наличие base64 без секретных индикаторов
            if re.match(r'^[A-Za-z0-9+/]*={0,2}$', match) and len(match) > 50:
                # Base64, проверьте, не выглядит ли это как секрет
                if not any(keyword in match.lower() for keyword in ['token', 'key', 'secret', 'password']):
                    self.stats['removed_as_trash'] += 1
                    продолжать
            
            result.append(item)
        
        вернуть результат
    
    def step_3_extension_filter(self, data):
        «Удаление файлов с нежелательными расширениями»
        результат = []
        
        для элемента в данных:
            match = str(item.get('match', ''))
            
            if self.validator.has_invalid_extension(match):
                self.stats['removed_by_extension'] += 1
                продолжать
            
            result.append(item)
        
        вернуть результат
    
    def step_4_determine_age(self, data):
        ""Определить возраст данных""
        для элемента в данных:
            возраст = self.validator.determine_age(item.get('match', ''))
            item['age'] = age
            self.stats[f'{age}_count'] += 1
        
        возвращаемые данные
    
    def step_5_classify_importance(self, data):
        «Классифицируйте по важности»
        classified = {'critical': [], 'useful': [], 'weak': [], 'trash': []}
        
        для элемента в данных:
            важность = self.validator.classify_importance(item.get('match', ''))
            ключ = важность.нижняя()
            Если ключ не относится к категории "секретно":
                key = 'trash'
            classified[key].append(item)
        
        возврат объявлений
    
    def step_6_validate(self, classified):
        """Проверка данных"""
        # Проверка выполняется в функции classify_importance
        возврат объявлений
    
    def step_7_remove_fakes(self, classified):
        """Удалить фиктивные/тестовые/демонстрационные значения"""
        результат = {}
        
        для категории, элементы в classified.items():
            результат[категория] = []
            для элемента в элементах:
                match = str(item.get('match', ''))
                if not self.validator.is_fake_value(match):
                    result[category].append(item)
                еще:
                    self.stats['removed_as_fake'] += 1
        
        вернуть результат
    
    def step_8_context_check(self, classified):
        «Проверка контекста — удаление секретов без контекста»
        результат = {}
        
        для категории, элементы в classified.items():
            результат[категория] = []
            для элемента в элементах:
                если category == 'critical' или category == 'useful':
                    # Чтобы узнать секреты, проверьте контекст
                    if self.validator.has_context(item.get('match', '')):
                        result[category].append(item)
                    еще:
                        если в результате отсутствует слово 'trash':
                            result['trash'] = []
                        result['trash'].append(item)
                еще:
                    result[category].append(item)
        
        если в результате отсутствует слово 'trash':
            result['trash'] = []
        
        вернуть результат
    
    def step_9_normalize(self, classified):
        «Нормализация формата данных»
        результат = {}
        
        для категории, элементы в classified.items():
            результат[категория] = []
            для элемента в элементах:
                match = str(item.get('match', ''))
                
                # Нормализация email:password
                если в match присутствует ':' и '@':
                    parts = match.split(':')
                    если len(parts) == 2:
                        match = f"{parts[0]}:{parts[1]}"
                
                item['match'] = match
                result[category].append(item)
        
        вернуть результат
    
    def step_10_secondary_dedup(self, classified):
        «Удалить дубликаты после нормализации»
        результат = {}
        
        для категории, элементы в classified.items():
            seen = set()
            результат[категория] = []
            
            для элемента в элементах:
                match = str(item.get('match', ''))
                Если совпадение не обнаружено:
                    seen.add(match)
                    result[category].append(item)
        
        вернуть результат
    
    def step_11_final_sort(self, classified):
        «Заключительная сортировка и вывод»
        возврат объявлений
    
    def save_results(self, classified, output_dir):
        «Сохранение результатов в файлы»
        os.makedirs(output_dir, exist_ok=True)
        
        start_time = datetime.now()
        
        # Сохранить в файлы
        for category in ['critical', 'useful', 'weak', 'trash']:
            filepath = os.path.join(output_dir, f'{category}.txt')
            items = classified.get(category, [])
            
            with open(filepath, 'w', encoding='utf-8') as f:
                для элемента в элементах:
                    match = item.get('match', '')
                    f.write(f"{match}\n")
        
        # Сохранение статистики
        processing_time = (datetime.now() - start_time).total_seconds()
        
        статистика = {
            'timestamp': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'общий': {
                'total_input': self.stats['total_input'],
                'after_dedup': self.stats['after_dedup'],
            },
            'удаления': {
                'removed_by_extension': self.stats['removed_by_extension'],
                'removed_as_trash': self.stats['removed_as_trash'],
                'removed_as_fake': self.stats['removed_as_fake'],
                'removed_as_dead': self.stats['removed_as_dead'],
            },
            'by_importance': {
                'critical_count': len(classified.get('critical', [])),
                'useful_count': len(classified.get('useful', [])),
                'weak_count': len(classified.get('weak', [])),
                'trash_count': len(classified.get('trash', [])),
            },
            'by_type': {
                'tokens_count': self.stats['tokens_count'],
                'crypto_count': self.stats['crypto_count'],
                'email_pass_count': self.stats['email_pass_count'],
                'login_pass_count': self.stats['login_pass_count'],
                'configs_count': self.stats['configs_count'],
                'cookies_count': self.stats['cookies_count'],
                'unknown_count': self.stats['unknown_count'],
            },
            'by_age': {
                'fresh_count': self.stats['fresh_count'],
                'stale_count': self.stats['stale_count'],
                'old_count': self.stats['old_count'],
                'unknown_age_count': self.stats['unknown_age_count'],
                'dead_count': self.stats['dead_count'],
            },
        }
        
        stats_path = os.path.join(output_dir, 'stats.json')
        
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        возвращаться {
            'critical': os.path.join(output_dir, 'critical.txt'),
            'useful': os.path.join(output_dir, 'useful.txt'),
            'weak': os.path.join(output_dir, 'weak.txt'),
            'trash': os.path.join(output_dir, 'trash.txt'),
            'stats': stats_path,
        }
    
    def get_statistics(self):
        """Получить актуальную статистику"""
        return self.stats.copy()

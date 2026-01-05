import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
импорт потоков
импорт os
импорт json
from datetime import datetime
from processor import DataProcessor

ПЕРЕВОДЫ = {
    'start_scan': 'Начать обработку',
    'stop_scan': 'Остановить',
    'save_results': 'Сохранить',
    'open_results': 'Открыть пятна',
    'select_file': 'Выбрать файл',
    'обработано': 'Обработано:',
    'критический': 'КРИТИЧЕСКИ:',
    'useful': 'USEFUL:',
    'слабый': 'СЛАБЫЙ:',
    'мусор': 'МУСОРЫ:',
    'loading': 'Загрузка...',
}

класс DataCleanerUI:
    def __init__(self, root, input_file=None, output_dir=None):
        self.root = root
        self.processor = DataProcessor()
        self.input_file = input_file
        self.output_dir = output_dir or os.path.expanduser("~/Desktop/data-cleaner-output")
        self.results = None
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        «Настройка компонентов пользовательского интерфейса»
        # Главный экран
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Панель 1: Выбор файла
        file_frame = ttk.LabelFrame(main_frame, text="1. Загрузка файла", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_frame, text="Выбрать ZIP/JSON/TXT", command=self.load_file).pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(file_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        # Панель 2: Параметры
        param_frame = ttk.LabelFrame(main_frame, text="2. Параметры", дополнение="10")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(param_frame, text="Минимальная длина:").pack(side=tk.LEFT,padx=5)
        self.min_length = tk.IntVar(value=8)
        ttk.Scale(param_frame, from_=4, to=32, variable=self.min_length, orient=tk.HORIZONTAL).pack(side=tk.LEFT, padx=5)
        
        # Панель 3: Статистика
        stats_frame = ttk.LabelFrame(main_frame, text="3. Статистика", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_var = tk.StringVar(value="Статистика...")
        ttk.Label(stats_frame, textvariable=self.stats_var, font=("Arial", 9)).pack()
        
        # Панель 4: Журнал
        log_frame = ttk.LabelFrame(main_frame, text="4. Лог обработки", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=100)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Начать", command=self.start_processing).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Открыть вывод", command=self.open_output_folder).pack(side=tk.LEFT, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_file(self):
        """Загрузить входной файл"""
        file_path = filedialog.askopenfilename(
            filetypes=[("ZIP-файлы", "*.zip"), ("JSON-файлы", "*.json"), ("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        если file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.log_text.insert(tk.END, f"Файл загружен: {file_path}\n")
            self.log_text.see(tk.END)
    
    def start_processing(self):
        """Начать обработку в фоновом потоке"""
        if not self.input_file:
            messagebox.showwarning("Внимание", "Выберите файл!")
            возвращаться
        
        self.processing = True
        thread = threading.Thread(target=self.process_data)
        thread.start()
    
    def process_data(self):
        «Данные процесса»»
        пытаться:
            self.log_callback("Загрузка файла...")
            data = self.processor.load_file(self.input_file)
            
            self.log_callback(f"Загружено {len(data)} записи")
            
            # Обработка с помощью обратных вызовов
            обратные вызовы = {
                'log': self.log_callback,
                'прогресс': lambda x, y: self.update_progress(x, y),
            }
            
            self.results = self.processor.process(data, callbacks)
            
            self.log_callback("Сохранение результатов...")
            self.processor.save_results(self.results, self.output_dir)
            
            self.log_callback("✓ Обработка завершена!")
            self.log_callback(f"Результаты сохранены в: {self.output_dir}")
            
            # Обновить статистику
            self.update_stats()
            
        за исключением исключения как e:
            self.log_callback(f"✗ Ошибка: {e}")
            трассировка импорта
            self.log_callback(traceback.format_exc())
        окончательно:
            self.processing = False
    
    def log_callback(self, message):
        """Добавить сообщение в журнал"""
        self.root.after(0, lambda: self._add_log(message))
    
    def _add_log(self, message):
        """Фактически добавить в журнал"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def update_progress(self, current, total):
        «Обновить информацию о ходе выполнения»
        проходить
    
    def update_stats(self):
        """Обновить отображение статистики""
        если self.results:
            stats_text = (
                f"CRITICAL: {len(self.results.get('critical', []))} | "
                f"ПОЛЕЗНО: {len(self.results.get('useful', []))} | "
                f"СЛАБЫЙ: {len(self.results.get('weak', []))} | "
                f"МУСОР: {len(self.results.get('trash', []))}"
            )
            self.stats_var.set(stats_text)
    
    def open_output_folder(self):
        """Открыть папку с выходными файлами"""
        os.makedirs(self.output_dir, exist_ok=True)
        если os.name == 'nt':
            os.startfile(self.output_dir)
        еще:
            os.system(f"xdg-open '{self.output_dir}' 2>/dev/null || open '{self.output_dir}'")

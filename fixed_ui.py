import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import json
from datetime import datetime
from processor import DataProcessor

TRANSLATIONS = {
    'start_scan': 'Начать обработку',
    'stop_scan': 'Остановить',
    'save_results': 'Сохранить',
    'open_results': 'Открыть папку',
    'select_file': 'Выбрать файл',
    'processed': 'Обработано:',
    'critical': 'КРИТИЧЕСКИ:',
    'useful': 'USEFUL:',
    'weak': 'СЛАБЫЙ:',
    'trash': 'МУСОР:',
    'loading': 'Загрузка...',
}

class DataCleanerUI:
    def __init__(self, root, input_file=None, output_dir=None):
        self.root = root
        self.processor = DataProcessor()
        self.input_file = input_file
        self.output_dir = output_dir or os.path.expanduser("~/Desktop/data-cleaner-output")
        self.results = None
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка компонентов пользовательского интерфейса"""
        
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Панель 1: Выбор файла
        file_frame = ttk.LabelFrame(main_frame, text="1. Загрузка файла", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_frame, text="Выбрать ZIP/JSON/TXT", command=self.load_file).pack(side=tk.LEFT, padx=5)
        self.file_label = ttk.Label(file_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        # Панель 2: Параметры
        param_frame = ttk.LabelFrame(main_frame, text="2. Параметры", padding="10")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(param_frame, text="Минимальная длина:").pack(side=tk.LEFT, padx=5)
        self.min_length = tk.IntVar(value=8)
        ttk.Scale(param_frame, from_=4, to=32, variable=self.min_length, orient=tk.HORIZONTAL).pack(side=tk.LEFT, padx=5)
        
        # Панель 3: Статистика
        stats_frame = ttk.LabelFrame(main_frame, text="3. Статистика", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stats_var = tk.StringVar(value="Статистика...")
        ttk.Label(stats_frame, textvariable=self.stats_var, font=("Arial", 9)).pack()
        
        # Панель 4: Лог
        log_frame = ttk.LabelFrame(main_frame, text="4. Лог обработки", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=100)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Панель 5: Предварительный просмотр результатов
        preview_frame = ttk.LabelFrame(main_frame, text="5. Результаты предварительного просмотра", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=6, width=100)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Начать обработку", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Остановить", command=self.stop_processing, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Открыть вывод", command=self.open_output_folder).pack(side=tk.LEFT, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_file(self):
        """Загрузить входной файл"""
        file_path = filedialog.askopenfilename(
            filetypes=[("ZIP-файлы", "*.zip"), ("JSON-файлы", "*.json"), ("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.log_text.insert(tk.END, f"Файл загружен: {file_path}\n")
            self.log_text.see(tk.END)
    
    def start_processing(self):
        """Начать обработку в фоновом потоке"""
        if not self.input_file:
            messagebox.showwarning("Внимание", "Выберите файл!")
            return
        
        self.processing = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=self.process_data)
        thread.daemon = True
        thread.start()
    
    def stop_processing(self):
        """Остановить обработку"""
        self.processing = False
        self.log_callback("Обработка остановлена пользователем")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def process_data(self):
        """Обработать данные"""
        try:
            self.log_callback("Загрузка файла...")
            data = self.processor.load_file(self.input_file)
            
            self.log_callback(f"Загружено {len(data)} записей")
            
            # Обработка с обратными вызовами
            callbacks = {
                'log': self.log_callback,
                'progress': lambda x, y: self.update_progress(x, y),
            }
            
            self.results = self.processor.process(data, callbacks)
            
            self.log_callback("Сохранение результатов...")
            self.processor.save_results(self.results, self.output_dir)
            
            self.log_callback("УСПЕХ: Обработка завершена!")
            self.log_callback(f"Результаты сохранены в: {self.output_dir}")
            
            # Обновить статистику
            self.update_stats()
            self.update_preview()
            
        except Exception as e:
            self.log_callback(f"ERROR: {e}")
            import traceback
            self.log_callback(traceback.format_exc())
        finally:
            self.processing = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def log_callback(self, message):
        """Добавить сообщение в лог"""
        self.root.after(0, lambda: self._add_log(message))
    
    def _add_log(self, message):
        """Действительно добавить в журнал"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def update_progress(self, current, total):
        """Обновить прогресс"""
        pass
    
    def update_stats(self):
        """Обновить данные статистики"""
        if self.results:
            stats_text = (
                f"CRITICAL: {len(self.results.get('critical', []))} | "
                f"USEFUL: {len(self.results.get('useful', []))} | "
                f"WEAK: {len(self.results.get('weak', []))} | "
                f"TRASH: {len(self.results.get('trash', []))}"
            )
            self.stats_var.set(stats_text)
    
    def update_preview(self):
        """Обновить предварительный просмотр результатов"""
        if self.results:
            preview = ""
            for category in ['critical', 'useful', 'weak', 'trash']:
                items = self.results.get(category, [])[:5]
                preview += f"\n=== {category.upper()} ({len(self.results.get(category, []))} total) ===\n"
                for item in items:
                    preview += f"{item.get('match', '')}\n"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, preview)
    
    def open_output_folder(self):
        """Открыть папку с результатом"""
        os.makedirs(self.output_dir, exist_ok=True)
        if os.name == 'nt':
            os.startfile(self.output_dir)
        else:
            os.system(f"xdg-open '{self.output_dir}' 2>/dev/null || open '{self.output_dir}'")

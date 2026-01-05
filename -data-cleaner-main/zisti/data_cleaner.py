#!/usr/bin/env python3
"""
Очиститель данных — продвинутый инструмент обработки данных
Обработка результатов DorkStrike PRO с классификацией и очисткой

Автор: Команда по очистке данных
Версия: 1.0.0
"""

импорт sys
импорт os
импорт argparse
import tkinter as tk

# Убедитесь, что скрипт может найти свои модули
script_dir = os.path.dirname(os.path.abspath(__file__))
если script_dir не находится в sys.path:
    sys.path.insert(0, script_dir)

from ui import DataCleanerUI

def main():
    «Основная точка входа для Data Cleaner»
    parser = argparse.ArgumentParser(description="Data Cleaner - Advanced Data Processing Tool")
    parser.add_argument('--input', help='Путь к входному файлу')
    parser.add_argument('--output', help='Путь к выходному каталогу')
    
    args = parser.parse_args()
    
    # Режим графического интерфейса (основной)
    пытаться:
        root = tk.Tk()
        root.title("Очистка данных - Обработка данных")
        root.geometry("1200x800")
        
        app = DataCleanerUI(root, input_file=args.input, output_dir=args.output)
        root.mainloop()
    за исключением исключения как e:
        print(f"Ошибка при запуске графического интерфейса: {e}")
        трассировка импорта
        traceback.print_exc()
        sys.exit(1)

если __name__ == "__main__":
    основной()

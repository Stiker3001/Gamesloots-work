import os
import re

def fix_header_panel(file_path):
    """Исправляет структуру header__panel в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Проверяем, есть ли вообще header__panel в файле
        if 'header__panel' not in content:
            return False
        
        # Паттерн для поиска неправильной структуры header__panel
        # Ищем случай, когда wrapper закрывается сразу после открытия, а header__nav и header__controls находятся вне wrapper
        # Структура: <div class="header__panel"><div class="wrapper"></div><ul>...</ul><div class="header__controls">...</div></div></div>
        # Нужно: <div class="header__panel"><div class="wrapper"><ul>...</ul><div class="header__controls">...</div></div></div>
        
        # Паттерн 1: точный паттерн с учетом всех возможных пробелов и переносов
        # Ищем: <div class="header__panel">...<div class="wrapper">...</div>...<ul class="list-reset header__nav">...</ul>...<div class="header__controls">...</div>...</div>...</div>
        # Используем более гибкий паттерн, который найдет структуру с любыми пробелами и переносами
        # Учитываем отступы (пробелы и табы) перед закрывающим тегом wrapper
        # Паттерн должен найти структуру где wrapper закрывается сразу после открытия
        # Используем более точный паттерн, который учитывает отступы и пробелы
        pattern1 = r'(<div class="header__panel">\s*<div class="wrapper">)\s*\n\s*</div>\s*\n\s*(<ul class="list-reset header__nav">.*?</ul>)\s*\n\s*(<div class="header__controls">.*?</div>)\s*\n\s*</div>\s*\n\s*</div>'
        
        replacement1 = r'\1\n\2\n\3\n</div>\n</div>'
        
        # Проверяем, есть ли неправильная структура и исправляем
        if re.search(pattern1, content, re.MULTILINE | re.DOTALL):
            content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE | re.DOTALL)
        
        # Паттерн 2: вариант без переносов строк (компактный)
        pattern2 = r'(<div class="header__panel">\s*<div class="wrapper">)\s+</div>\s+(<ul class="list-reset header__nav">.*?</ul>)\s+(<div class="header__controls">.*?</div>)\s+</div>\s+</div>'
        
        replacement2 = r'\1\n\2\n\3\n</div>\n</div>'
        
        if re.search(pattern2, content, re.MULTILINE | re.DOTALL):
            content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE | re.DOTALL)
        
        # Паттерн 3: вариант с отступами (пробелы и табы) - более точный
        # Ищем структуру с отступами перед закрывающим тегом wrapper
        # Учитываем возможные пробелы и табы в разных комбинациях
        pattern3 = r'(<div class="header__panel">\s*<div class="wrapper">)\s*\n?\s*</div>\s*\n?\s*(<ul class="list-reset header__nav">.*?</ul>)\s*\n?\s*(<div class="header__controls">.*?</div>)\s*\n?\s*</div>\s*\n?\s*</div>'
        
        replacement3 = r'\1\n\2\n\3\n</div>\n</div>'
        
        if re.search(pattern3, content, re.MULTILINE | re.DOTALL):
            content = re.sub(pattern3, replacement3, content, flags=re.MULTILINE | re.DOTALL)
        
        # Если содержимое изменилось, сохраняем файл
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Исправлено: {file_path}")
            return True
        else:
            print(f"[SKIP] Структура уже правильная: {file_path}")
            return False
                
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {file_path}")
        return False
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке {file_path}: {e}")
        return False

def main():
    """Основная функция"""
    processed = 0
    skipped = 0
    errors = 0
    
    # Список HTML файлов для обработки
    html_files = []
    
    # Добавляем все HTML файлы из goods/info/
    goods_info_dir = 'goods/info'
    if os.path.exists(goods_info_dir):
        for file in os.listdir(goods_info_dir):
            if file.endswith('.html') and not file.endswith('-1.html'):
                html_files.append(os.path.join(goods_info_dir, file))
    
    # Добавляем все HTML файлы из en/goods/info/
    en_goods_info_dir = 'en/goods/info'
    if os.path.exists(en_goods_info_dir):
        for file in os.listdir(en_goods_info_dir):
            if file.endswith('.html') and not file.endswith('-1.html'):
                html_files.append(os.path.join(en_goods_info_dir, file))
    
    # Добавляем другие HTML файлы только из текущей директории проекта
    # Исключаем системные папки
    exclude_dirs = {'.git', 'node_modules', 'AppData', '__pycache__', '.vscode', '.idea'}
    
    for root, dirs, files in os.walk('.'):
        # Пропускаем системные папки
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        # Пропускаем папки вне проекта
        if any(excluded in root for excluded in ['AppData', 'Gamesloots-work-2']):
            continue
        
        for file in files:
            if file.endswith(('.html', '.htm')):
                file_path = os.path.join(root, file)
                # Пропускаем дубликаты (-1.html)
                if not file.endswith('-1.html') and not file.endswith('-1.htm'):
                    # Пропускаем файлы из системных папок
                    if not any(excluded in file_path for excluded in ['AppData', 'Gamesloots-work-2']):
                        html_files.append(file_path)
    
    print(f"Найдено {len(html_files)} HTML файлов для обработки\n")
    
    for filename in html_files:
        try:
            if fix_header_panel(filename):
                processed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"[ERROR] Ошибка при обработке {filename}: {e}")
            errors += 1
    
    print(f"\nИтого:")
    print(f"  - Исправлено: {processed} файлов")
    print(f"  - Пропущено: {skipped} файлов")
    print(f"  - Ошибок: {errors}")

if __name__ == '__main__':
    main()


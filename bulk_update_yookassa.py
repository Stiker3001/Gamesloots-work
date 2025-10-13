#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Массовое добавление кнопки YooKassa во все файлы товаров
"""

import os
import glob

# Шаблон старого кода (без YooKassa)
OLD_CODE = '''                           <div btps="" title-fees="Комиссия 0 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="11">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/cryptonator.png"></span>
                        <span class="payment__btn-label">Bitcoin (Plisio.net)</span>
                     </button>
                  </div>
            
               </div>'''

# Вариант с -1.png
OLD_CODE_1 = '''                           <div btps="" title-fees="Комиссия 0 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="11">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/cryptonator-1.png"></span>
                        <span class="payment__btn-label">Bitcoin (Plisio.net)</span>
                     </button>
                  </div>
            
               </div>'''

# Новый код (с YooKassa)
NEW_CODE = '''                           <div btps="" title-fees="Комиссия 0 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="11">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/cryptonator.png"></span>
                        <span class="payment__btn-label">Bitcoin (Plisio.net)</span>
                     </button>
                  </div>
                           <div btps="" title-minprice="Минимальная сумма к оплате: 10" title-fees="Комиссия 2.8 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="30">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/yookassa.svg"></span>
                        <span class="payment__btn-label">YooKassa</span>
                     </button>
                  </div>
            
               </div>'''

NEW_CODE_1 = '''                           <div btps="" title-fees="Комиссия 0 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="11">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/cryptonator-1.png"></span>
                        <span class="payment__btn-label">Bitcoin (Plisio.net)</span>
                     </button>
                  </div>
                           <div btps="" title-minprice="Минимальная сумма к оплате: 10" title-fees="Комиссия 2.8 %" class="payment__item item--cryptocurrency">
                     <button type="button" class="payment__btn" pay="30">
                        <span class="payment__btn-icon"><img alt="" src="../../source/custom/css/imperiumkey/img/icons/payments/yookassa.svg"></span>
                        <span class="payment__btn-label">YooKassa</span>
                     </button>
                  </div>
            
               </div>'''

def update_file(filepath):
    """Обновить один файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли уже YooKassa
        if 'pay="30"' in content:
            return 'skipped'
        
        # Заменяем код
        if OLD_CODE in content:
            new_content = content.replace(OLD_CODE, NEW_CODE)
        elif OLD_CODE_1 in content:
            new_content = content.replace(OLD_CODE_1, NEW_CODE_1)
        else:
            return 'not_found'
        
        # Сохраняем
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 'updated'
    except Exception as e:
        return f'error: {e}'

def main():
    print("=" * 60)
    print("Массовое обновление файлов - добавление кнопки YooKassa")
    print("=" * 60)
    print()
    
    # Папки для обновления
    directories = [
        'goods/info/*.html',
        'en/goods/info/*.html'
    ]
    
    total_files = 0
    updated = 0
    skipped = 0
    not_found = 0
    errors = 0
    
    for pattern in directories:
        files = glob.glob(pattern)
        print(f"Обработка: {pattern} ({len(files)} файлов)")
        
        for filepath in files:
            total_files += 1
            result = update_file(filepath)
            
            if result == 'updated':
                updated += 1
                print(f"  ✓ {os.path.basename(filepath)}")
            elif result == 'skipped':
                skipped += 1
            elif result == 'not_found':
                not_found += 1
                print(f"  ⚠ Не найден код: {os.path.basename(filepath)}")
            else:
                errors += 1
                print(f"  ✗ Ошибка: {os.path.basename(filepath)} - {result}")
    
    print()
    print("=" * 60)
    print("РЕЗУЛЬТАТЫ:")
    print(f"  Всего файлов: {total_files}")
    print(f"  Обновлено: {updated}")
    print(f"  Пропущено (уже обновлено): {skipped}")
    print(f"  Не найден код: {not_found}")
    print(f"  Ошибок: {errors}")
    print("=" * 60)
    print()
    print("✅ Обновление завершено!")

if __name__ == '__main__':
    main()


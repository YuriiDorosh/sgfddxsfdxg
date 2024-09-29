import pandas as pd

def parse_excel_with_pandas(file_path, sheet_name='Sheet2'):
    # Завантажуємо дані з Excel у pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Створюємо список для зберігання головних продуктів та їх складових
    main_products = []
    current_product = None
    current_level = {i: None for i in range(1, 9)}  # Зберігаємо поточні елементи для рівнів від 1 до 8
    
    # Ітеруємо по рядках DataFrame
    for idx, row in df.iterrows():
        # Аналізуємо ширину злитих клітинок (порожні клітинки між ними)
        filled_cells = row.notnull()  # Перевіряємо, які комірки не порожні
        
        # Ширина продукту (скільки колонок не пусті)
        width = sum(filled_cells.iloc[7:15])  # Колонки з H по O
        
        # Визначаємо рівні продуктів
        if width == 8:  # 1 рівень (найширша комірка)
            if current_product:
                main_products.append(current_product)
            current_product = {
                'Main Product': row.iloc[7],  # Продукт з колонки H
                'Components': []
            }
            current_level[1] = current_product
        elif width == 7:  # 2 рівень
            component = {
                'Level': 2,
                'Main Component': row.iloc[8],  # Компонент з колонки I
                'Sub-components': []
            }
            current_product['Components'].append(component)
            current_level[2] = component
        elif width == 6:  # 3 рівень
            sub_component = {
                'Level': 3,
                'Main Component': row.iloc[9],  # Підкомпонент з колонки J
                'Sub-components': []
            }
            current_level[2]['Sub-components'].append(sub_component)
            current_level[3] = sub_component
        elif width == 5:  # 4 рівень
            part = {
                'Level': 4,
                'Component': row.iloc[10]  # Частина з колонки K
            }
            current_level[3]['Sub-components'].append(part)
            current_level[4] = part
        # Додайте логіку для рівнів 5-8 за аналогією
    
    # Додаємо останній продукт після завершення циклу
    if current_product:
        main_products.append(current_product)

    return main_products

# Використання функції
file_path = 'test.xlsx'  # Вкажіть шлях до вашого файлу Excel
products_data = parse_excel_with_pandas(file_path)

# Виведення результату
for product in products_data:
    print(f"Main Product: {product['Main Product']}")
    for component in product['Components']:
        print(f"  Main Component (Level 2): {component['Main Component']}")
        for sub_component in component['Sub-components']:
            print(f"    Main Component (Level 3): {sub_component['Main Component']}")
            for part in sub_component.get('Sub-components', []):
                print(f"      Component (Level 4): {part['Component']}")

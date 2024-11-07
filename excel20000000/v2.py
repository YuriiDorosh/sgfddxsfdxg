import pandas as pd
import json

# Читання даних
df = pd.read_excel('tree_structure.xlsx', header=None)

# Визначення рівня вкладеності
def get_level(row):
    for i, cell in enumerate(row):
        if pd.notnull(cell):
            return i
    return None

df['Level'] = df.apply(get_level, axis=1)

# Отримання назв елементів
def get_name(row):
    for cell in row:
        if pd.notnull(cell):
            return str(cell).strip()
    return None

df['Name'] = df.apply(get_name, axis=1)

# Побудова дерева
tree = []
stack = []

for index, row in df.iterrows():
    level = row['Level']
    name = row['Name']
    node = {'name': name, 'children': []}

    if level == 0:
        tree.append(node)
        stack = [node]
    else:
        while len(stack) > level:
            stack.pop()
        parent = stack[-1]
        parent['children'].append(node)
        stack.append(node)

# Виведення дерева
print(json.dumps(tree, ensure_ascii=False, indent=4))

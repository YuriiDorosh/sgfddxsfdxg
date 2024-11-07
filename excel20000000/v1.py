from ninja_extra import NinjaExtraAPI, File
from ninja.files import UploadedFile
import pandas as pd
from io import BytesIO

api = NinjaExtraAPI()

@api.post("/parse-excel")
async def parse_excel(file: UploadedFile = File(...)):
    # Завантаження файлу Excel
    file_data = BytesIO(file.read())
    
    # Читання аркуша 'data_base'
    try:
        data = pd.read_excel(file_data, sheet_name='data_base')
    except Exception as e:
        return {"error": f"Failed to read Excel file: {str(e)}"}
    
    # Попередня очистка даних, видалення пустих рядків
    data = data.dropna(how="all").reset_index(drop=True)
    
    # Список заголовків (груп), за якими потрібно групувати
    groups = ['ліжка', 'матраци', 'станки']  # додайте сюди інші назви груп, якщо необхідно
    
    parsed_data = {}
    current_group = None
    
    for _, row in data.iterrows():
        name = str(row['name']).strip() if 'name' in row else None
        
        # Перевірка, чи є рядок заголовком групи
        if name in groups:
            current_group = name
            parsed_data[current_group] = []  # Створюємо новий список для даних цієї групи
            continue
        
        # Додавання рядка до поточної групи, якщо група визначена
        if current_group:
            item = {
                "full_name": row.get("full name"),
                "info": row.get("info"),
                "comment": row.get("comment"),
                "quantity": row.get("quantity")
            }
            parsed_data[current_group].append(item)
    
    return {"data": parsed_data}

# Додайте маршрут до головного проекту
urlpatterns = [
    path("api/", api.urls),
]

#!/bin/bash

PROJECT_PATH="/var/www/project"
LAST_MODIFIED_FILE="$PROJECT_PATH/last_modified.txt"
MAKE_CMD="make all"

# Отримуємо дату останньої модифікації файлів, ігноруючи певні директорії
LATEST_MODIFICATION=$(find $PROJECT_PATH -type f \
  -not -path "$PROJECT_PATH/.git/*" \
  -not -name ".env" \
  -not -path "$PROJECT_PATH/backend/logs/*" \  # Ігноруємо лог-файли
  -not -path "$PROJECT_PATH/frontend/uploads/*" \  # Ігноруємо зміни в папці uploads
  -exec stat -c %Y {} + | sort -nr | head -n 1)

# Читаємо попередню дату модифікації
if [ -f "$LAST_MODIFIED_FILE" ]; then
  PREVIOUS_MODIFICATION=$(cat $LAST_MODIFIED_FILE)
else
  PREVIOUS_MODIFICATION=0
fi

# Якщо є зміни, перезапускаємо Docker-контейнери
if [ "$LATEST_MODIFICATION" -gt "$PREVIOUS_MODIFICATION" ]; then
  echo "Changes detected, restarting services..."
  cd $PROJECT_PATH
  $MAKE_CMD
  echo $LATEST_MODIFICATION > $LAST_MODIFIED_FILE
else
  echo "No changes detected."
fi

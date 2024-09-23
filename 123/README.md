```bash
crontab -e
```

```bash
*/5 * * * * /path/on/vps/project/check_changes.sh >> /path/on/vps/project/deploy.log 2>&1
```

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

```bash
ssh-copy-id your_vps_user@your_vps_ip
```

```bash
chmod +x deploy.sh
```

vps
```bash
chmod 700 ~/.ssh
```

vps
```bash
chmod 600 ~/.ssh/authorized_keys
```

local
```bash
chmod 600 ~/.ssh/id_rsa
```

local
```bash
chmod 644 ~/.ssh/id_rsa.pub
```

```bash
sudo apt update
sudo apt install rsync
```

```bash
sudo yum install rsync
```

```bash
grep CRON /var/log/syslog
```

```bash
grep CRON /var/log/cron
```


```bash
#!/bin/bash

PROJECT_PATH="/root/test/123"
LAST_MODIFIED_FILE="$PROJECT_PATH/last_modified.txt"
MAKE_CMD="make all"

# Отримуємо дату останньої модифікації файлів, ігноруючи певні директорії
LATEST_MODIFICATION=$(find $PROJECT_PATH -type f \
  -not -path "$PROJECT_PATH/.git/*" \
  -not -name ".env" \
  -not -path "$PROJECT_PATH/backend/logs/*" \
  -not -path "$PROJECT_PATH/frontend/uploads/*" \
  -exec stat -c %Y {} + | sort -nr | head -n 1)

# Читаємо попередню дату модифікації
if [ -f "$LAST_MODIFIED_FILE" ]; then
  PREVIOUS_MODIFICATION=$(cat $LAST_MODIFIED_FILE)
else
  PREVIOUS_MODIFICATION=0
fi

# Перевіряємо, чи є значення для LATEST_MODIFICATION
if [ -z "$LATEST_MODIFICATION" ]; then
  echo "No files found for modification checking."
  exit 1
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

```


*/5 * * * * /root/check_changes.sh >> /root/deploy.log 2>&1
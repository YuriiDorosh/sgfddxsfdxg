#!/bin/bash

# Налаштування
REMOTE_USER="your_vps_user"
REMOTE_HOST="your_vps_ip"
REMOTE_PATH="/path/on/vps/project"
LOCAL_PATH="/path/on/local/project"

rsync -avz --exclude-from='.rsyncignore' $LOCAL_PATH $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH


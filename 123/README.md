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


*/5 * * * * /root/check_changes.sh >> /root/deploy.log 2>&1
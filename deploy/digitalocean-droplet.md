# DigitalOcean deployment

SQLite needs a persistent filesystem. Vercel and most serverless platforms do not provide durable local SQLite storage, so the safest simple deployment is a small DigitalOcean Droplet running Docker Compose.

## Droplet setup

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo mkdir -p /opt/todo-sqlite-multiuser
sudo chown $USER:$USER /opt/todo-sqlite-multiuser
cd /opt/todo-sqlite-multiuser
git clone https://github.com/enoteware/todo-sqlite-multiuser.git .
cp .env.example .env
# edit TODO_SECRET_KEY
sudo docker compose up -d --build
```

The SQLite DB lives in the named Docker volume `todo-sqlite-multiuser_todo_data`.

## Optional production front door

Put Caddy or Nginx in front for HTTPS and a custom domain.

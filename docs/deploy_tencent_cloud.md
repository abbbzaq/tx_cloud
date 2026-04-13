# 腾讯云 Linux 部署指南

## 1. 服务器准备

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip nginx git
```

## 2. 拉取代码

```bash
sudo mkdir -p /srv/query_ali_clb
sudo chown -R $USER:$USER /srv/query_ali_clb
cd /srv/query_ali_clb
git clone https://github.com/abbbzaq/tx_cloud.git .
```

## 3. 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. 配置环境变量

```bash
cp .env.example .env
nano .env
```

## 5. 初始化数据库

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py check
```

## 6. 配置 systemd

```bash
sudo cp deploy/systemd/query_ali_clb.service /etc/systemd/system/query_ali_clb.service
sudo sed -i 's#User=www#User=ubuntu#g' /etc/systemd/system/query_ali_clb.service
sudo sed -i 's#Group=www#Group=ubuntu#g' /etc/systemd/system/query_ali_clb.service
sudo systemctl daemon-reload
sudo systemctl enable query_ali_clb
sudo systemctl start query_ali_clb
sudo systemctl status query_ali_clb --no-pager
```

## 7. 配置 Nginx

```bash
sudo cp deploy/nginx/query_ali_clb.conf /etc/nginx/sites-available/query_ali_clb
sudo ln -sf /etc/nginx/sites-available/query_ali_clb /etc/nginx/sites-enabled/query_ali_clb
sudo nginx -t
sudo systemctl restart nginx
```

## 8. 开放安全组端口

在腾讯云控制台安全组放行：
- TCP 80（HTTP）
- TCP 443（如果后续上 HTTPS）

## 9. 验证接口

```bash
curl http://127.0.0.1/ali/
curl http://127.0.0.1/tx/
curl http://127.0.0.1/ucloud/
```

## 10. 常用排障命令

```bash
sudo journalctl -u query_ali_clb -n 200 --no-pager
sudo systemctl restart query_ali_clb
sudo systemctl restart nginx
```

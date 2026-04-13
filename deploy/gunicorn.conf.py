# Gunicorn configuration for production
bind = "127.0.0.1:8000"
workers = 2
threads = 2
timeout = 120
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"

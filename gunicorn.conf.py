import os

PORT = os.getenv("PORT", "8080")
bind = "0.0.0.0:" + PORT
workers = 1
log_level = "info"
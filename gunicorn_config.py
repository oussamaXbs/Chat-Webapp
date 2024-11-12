# gunicorn_config.py
import os

# Bind to Azure’s assigned port
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = 4  # Adjust this based on your expected traffic

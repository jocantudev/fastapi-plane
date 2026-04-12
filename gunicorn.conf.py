# Gunicorn configuration file
import multiprocessing
import os

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = 4

worker_class = "uvicorn.workers.UvicornWorker"

# On Azure App Service, cpu_count() can be much higher than actual quota.
# Cap workers to avoid memory pressure and startup crashes on small SKUs.
default_workers = min(4, (multiprocessing.cpu_count() * 2) + 1)
workers = int(os.getenv("WEB_CONCURRENCY", default_workers))
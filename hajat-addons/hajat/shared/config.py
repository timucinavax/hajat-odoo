from box import Box
from decouple import config

config = Box({
    "backend_webhook_url": config("BACKEND_WEBHOOK_URL", default="http://localhost:5000"),
    "backend_api_key": config("BACKEND_API_KEY", default=""),
},frozen_box=True)
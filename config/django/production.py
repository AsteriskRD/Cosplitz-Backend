# from .base import *
from config.env import env

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# CORS_ALLOWED_ORIGINS = [
#     "https://cosplitz.vercel.app/",
#     "http://127.0.0.1:5500",
# ]
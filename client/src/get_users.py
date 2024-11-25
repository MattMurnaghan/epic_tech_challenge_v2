import requests
import os
from client.src.utils import load_env_vars, load_urls

load_env_vars()

load_urls(["BASE_URL", "USERS", "USERS_ID"])





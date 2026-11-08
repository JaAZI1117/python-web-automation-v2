import os

# 关闭 Selenium Manager 联网解析（你机器访问 raw.githubusercontent / storage.googleapis 很慢）
os.environ.setdefault("SE_OFFLINE", "true")

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))

STANDARD_USER = {"username": "standard_user", "password": "secret_sauce"}

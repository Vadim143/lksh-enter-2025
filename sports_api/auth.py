import json
import requests
import logging
from sports_api.config import get_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = "https://lksh-enter.ru"
settings = get_settings()
token = settings.token
headers = {"Authorization": token}

logger.info("Чтение файла reason.json")
with open("../data/reason.json", encoding="utf-8") as f:
    reason = json.load(f)

logger.info(f"Отправка POST-запроса на {base_url}/login")
response = requests.post(base_url + "/login", headers=headers, json=reason)

logger.info(f"Ответ от сервера: статус {response.status_code}, тело: {response.text}")

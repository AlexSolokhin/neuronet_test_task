import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены: проверьте файл .env')
else:
    load_dotenv()

ASR_TOKEN = os.getenv('ASR_TOKEN')
TTS_TOKEN = os.getenv('TTS_TOKEN')

db = "some db object"

media_params = nv.media_params({
    "asr": "google",
    "tts": "google",
    "lang": "ru_RU",
    "authentication_data": {"asr": ASR_TOKEN, "tts": TTS_TOKEN}
})

default_env = nn.env({
    "flag": "some_flag",
    "lang": "ru_RU",
})

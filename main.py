import telebot
import requests
import os

# Токен Telegram-бота от BotFather
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Для безопасности используем переменные окружения
# API-ключ от Hugging Face
HF_API_KEY = os.getenv("HF_API_KEY")
# URL модели на Hugging Face (например, GPT-2, можно заменить на другую, например, "facebook/blenderbot-400M-distill")
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция для запроса к Hugging Face API
def get_hf_response(user_input):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input, "parameters": {"max_length": 100, "num_return_sequences": 1}}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return "Извини, что-то пошло не так с API."

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, "Думаю...")
    reply = get_hf_response(user_text)
    bot.send_message(message.chat.id, reply)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)

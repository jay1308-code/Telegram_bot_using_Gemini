from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai



load_dotenv()
TOKEN = os.getenv("TOKEN")
GEMINI_TOKEN = os.getenv("GOOGLE_API_KEY")




# Connect with Gemini
genai.configure(api_key=GEMINI_TOKEN)

generation_config = {
  "temperature": 0.6,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

MODEL_NAME = "gemini-1.0-pro"


model = genai.GenerativeModel(model_name=MODEL_NAME,
                             generation_config=generation_config,
                             safety_settings=safety_settings)



#Initialization of bot
bot =Bot(token=TOKEN)
dispatcher = Dispatcher(bot)



class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()


def clear_past():
    reference.response = ""




@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")




@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Bappy. How can i assist you?")




@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)




@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    response = model.start_chat(history=[
        {"role": "user", "parts": [reference.response]},  # Provide previous conversation context (optional)
        {"role": "model", "parts": [message.text]}  # Initial greeting (optional)
    ])

    response.send_message(message.text)
    reference.response = response.last.text

    print(f">>> Gemini: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)
    
    





if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)




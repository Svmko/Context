# Context; a bot for simple task management

from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_reponse

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents probably were not enabled.)')
        return
    
#    if is_private := user_message[0] == '?':
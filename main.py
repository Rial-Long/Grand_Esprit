import discord
from discord.ext import commands
from tools import *
from bot_command import *
import os
from dotenv import load_dotenv

def main():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = "GE!", intents = intents)

    @bot.event                  #if the bot ready to start
    async def on_ready():
        print("Ready !")
    great_spirit_command(bot, intents)
    load_dotenv()
    bot.run(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    main()
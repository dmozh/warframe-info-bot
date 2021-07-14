import discord
from discord.ext import commands
from bot.settings import Settings
from bot.bot_commands import cmds

bot = commands.Bot(command_prefix=Settings.prefix)

for f in cmds:
    bot.add_command(f)

bot.run(Settings.token)

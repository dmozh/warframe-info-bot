import discord
from discord.ext import commands
from bot.settings import Settings
from bot.bot_commands import cogs

bot = commands.Bot(command_prefix=Settings.prefix)

for cog in cogs:
    bot.add_cog(cog(bot))

bot.run(Settings.token)

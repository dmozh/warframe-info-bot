import discord
from discord.ext import commands
from bot.settings import settings
from bot.bot_commands import cogs

bot = commands.Bot(command_prefix=settings.prefix)

for cog in cogs:
    bot.add_cog(cog(bot))

bot.run(settings.token)

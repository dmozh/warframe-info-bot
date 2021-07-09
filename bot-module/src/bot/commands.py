from discord.ext import commands
from bot.settings import Settings
from logger import log

bot = commands.Bot(command_prefix=Settings.prefix)


# @log('command hello', 'execute command hello')
# async def h(ctx):
#     await ctx.send(f'Hello')
#
#
# custom = commands.Command(h)
#
# bot.add_command(custom)


@bot.command()
@log('command hello', 'execute command hello')
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')

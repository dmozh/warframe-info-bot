from logger import log
from ..services import general
from discord.ext import commands


@commands.command()
@log('command hello', 'execute command hello', log_coro=True)
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@commands.command()
async def pic(ctx):

    await ctx.send(f'hi :100:')#, embed=embed)  # Отправляем Embed
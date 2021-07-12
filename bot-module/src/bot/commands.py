import discord

from discord.ext import commands
from bot.settings import Settings
from logger import log
from requests import get
import json


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
@log('command hello', 'execute command hello', log_coro=True)
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@bot.command()
async def pic(ctx):
    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = 'https://warframe.market/static/assets/icons/en/thumbs/Catalyzer_Link.8ffa520e67c52e10b51ccc1cec6b7f88.128x128.png') # Устанавливаем картинку Embed'a
    await ctx.send('hi', embed = embed) # Отправляем Embed
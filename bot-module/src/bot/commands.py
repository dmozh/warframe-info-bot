import discord

from discord.ext import commands
from bot.settings import Settings
from logger import log
from requests import get
from json import loads
from .services import trade_service

bot = commands.Bot(command_prefix=Settings.prefix)

dialogs = {}


@bot.command()
@log('command hello', 'execute command hello', log_coro=True)
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@bot.command()
async def pic(ctx):
    embed = discord.Embed(color=0xff9900, title='Random Fox')  # Создание Embed'a
    embed.set_image(
        url='https://warframe.market/static/assets/icons/en/thumbs/Catalyzer_Link.8ffa520e67c52e10b51ccc1cec6b7f88.128x128.png')  # Устанавливаем картинку Embed'a
    await ctx.send(f'hi :100:', embed=embed)  # Отправляем Embed


@bot.command()
@log(f"{__name__}", "find items", log_coro=True)
async def find(ctx):
    msg = trade_service.TradeService.gen_msg(ctx.message.content.lower())
    await ctx.send(msg)

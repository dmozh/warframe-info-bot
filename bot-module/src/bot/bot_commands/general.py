from logger import log
from ..services import general
from discord.ext import commands


class General(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @log('command hello', 'execute command hello', log_coro=True)
    async def hello(self, ctx):
        author = ctx.message.author

        await ctx.send(f'Hello, {author.mention}!')

    @commands.command()
    async def pic(self, ctx):
        await ctx.send(f'hi :100:')  # , embed=embed)  # Отправляем Embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            print(type(user))
            print(user.bot)
            print(user, reaction, str(__name__))

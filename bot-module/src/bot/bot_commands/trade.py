from logger import log
from ..services.trade import TradeService
from discord.ext import commands
from discord.member import Member


# from ..dialogs import Dialog, DIALOGS

services = {}


class Trade(commands.Cog, name="Trade"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @log(f"{__name__}", "find items", log_coro=True)
    async def find(self, ctx, *items):
        """
        Find items
        enter command with one or more items separated by a space
        Example: $find парные a1 Мираж
        :param items: tuple
        """
        # print(items)
        if not str(ctx.message.author) in services:
            service = TradeService(ctx)
            services[str(ctx.message.author)] = service
        else:
            service = services[str(ctx.message.author)]
        msg = await ctx.send(f"{service.gen_msg(items=items)}")
        await service.add_reactions(msg)
        # print(type(msg))
        # await msg.add_reaction("🔒")

    @commands.Cog.listener()
    @log(f"{__name__}", "find items set emoji", log_coro=True)
    async def on_reaction_add(self, reaction, user: Member):
        if not user.bot:
            print(type(user))
            print(user.bot)
            service = services[str(user)]
            ctx = service.return_ctx()
            msg = await ctx.send(f"{service.select_page(reaction, user)}")
            await service.add_reactions(msg)
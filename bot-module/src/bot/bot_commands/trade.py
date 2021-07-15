from logger import log
from ..services.trade import TradeService
from discord.ext import commands

# from ..dialogs import Dialog, DIALOGS

services = {}


class Trade(commands.Cog, name="Trade"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @log(f"{__name__}", "find items", log_coro=True)
    async def find(self, ctx, item):
        """
        Find items
        :param item:
        :param ctx:
        :return:
        """
        service = TradeService(ctx)

        msg = service.gen_msg(item.lower())
        o = await ctx.send(f"{msg}")
        await o.add_reaction("🔒")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(user, reaction, str(__name__))

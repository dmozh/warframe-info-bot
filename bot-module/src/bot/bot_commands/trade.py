from logger import log

from ..services.trade import TradeService
from ..services.base import services

from discord.ext import commands
from discord.member import Member


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
        :param ctx:
        :param items: tuple
        """
        service = TradeService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_msg(items=items)

    @commands.Cog.listener()
    async def on_message(self, msg):
        pass

    @commands.Cog.listener()
    # @log(f"{__name__}", "find items set emoji", log_coro=True)
    async def on_reaction_add(self, reaction, user: Member):
        if not user.bot:
            service = list(filter(lambda x: x is not None,
                                  map(lambda x: x if x.ctx.message.author == user and
                                                     x.msg.id == reaction.message.id else None,
                                      services)))[0]
            await service.action_on_reaction(reaction, user)

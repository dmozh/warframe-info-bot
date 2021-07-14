from logger import log
from ..services import trade
from discord.ext import commands


@commands.command()
@log(f"{__name__}", "find items", log_coro=True)
async def find(ctx, msg):
    # msg = trade.TradeService.gen_msg(ctx.message.content.lower())
    await ctx.send(f"{msg}")

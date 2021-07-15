from logger import log
from ..services.trade import TradeService
from discord.ext import commands

# from ..dialogs import Dialog, DIALOGS

services = {}


@commands.command()
@log(f"{__name__}", "find items", log_coro=True)
async def find(ctx, msg):
    if not services[ctx.message.author]:
        services[ctx.message.author] = TradeService(ctx)

    msg = services[ctx.message.author].gen_msg(msg.lower())
    await ctx.send(f"{msg}")
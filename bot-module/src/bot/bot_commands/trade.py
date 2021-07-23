from logger import log
from ..services.trade import TradeService, services
from discord.ext import commands
from discord.member import Member
from collections import namedtuple


# from ..dialogs import Dialog, DIALOGS

# services = {}


# "<author>": {"service": service, "msg": msg}

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
        # print(items)
        # if str(ctx.message.author) in services:
        #     await services[str(ctx.message.author)].clear_reactions()
        service = TradeService(ctx.message.author, services, ctx)
        await services.add_service(ctx.message.author, service)
        # print(service)
        # print(services)
        # services[str(ctx.message.author)] = service
        # if not str(ctx.message.author) in services:
        #     service = TradeService(ctx)
        #     services[str(ctx.message.author)] = service
        # else:
        #     service = services[str(ctx.message.author)]
        await service.action_on_msg(items=items)
        # await ctx.message.reply(content='fff')
        # msg = await ctx.send(f"{service.general_msg(items=items)}")
        # service.msg = msg
        # services[str(ctx.message.author)] = msg
        # await service.add_reactions(msg)
        # print(type(msg))
        # await msg.add_reaction("🔒")

    @commands.Cog.listener()
    async def on_message(self, msg):
        pass#print(msg)

    @commands.Cog.listener()
    # @log(f"{__name__}", "find items set emoji", log_coro=True)
    async def on_reaction_add(self, reaction, user: Member):
        if not user.bot:
            # print(type(reaction), reaction.message.reference)
            # print(type(user))
            # print(user.bot)
            # print(services)
            service = list(filter(lambda x: x is not None,
                                  map(lambda x: x if x.ctx.message.author == user and
                                                    x.ctx.message.id == reaction.message.reference.message_id else None,
                                      services)))[0]
            await service.action_on_reaction(reaction, user)
            # msg = services[str(user)]['msg']
            # ctx = service.return_ctx()
            # await service.delete_msg()
            # await msg.delete()
            # del services[str(user)]['msg']
            # text = service.action_on_reaction(reaction, user)
            # msg = await ctx.send(text)
            # services[str(ctx.message.author)]['msg'] = msg
            # service.msg = msg
            # await service.add_reactions(msg)

from .trade import *
from .worldstate import *

cogs = [obj for (name, obj) in vars().items()
        if hasattr(obj, "__class__") and obj.__class__.__name__ == "CogMeta"]

# class Events(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print('Ready!')
#         print('Logged in as ---->', self.bot.user)
#         print('ID:', self.bot.user.id)
#
#     @commands.Cog.listener()
#     async def on_message(self, message):
#         print(message)
#
#     @commands.command()
#     async def find1(self, _ctx, msg):
#         print(_ctx)
#
#     @commands.Cog.listener()
#     async def on_message_edit(self, after, before):
#         print(type(after), before.reactions)

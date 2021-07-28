from discord import Embed
from discord import Message
from discord.ext.commands import Context
from logger import log
from ..services import general
from discord.ext import commands
from ..settings import settings
from requests import post


class General(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @log('command hello', 'execute command hello', log_coro=True)
    async def hello(self, ctx):
        author = ctx.message.author
        print(ctx.message.channel.id)
        base_url = f"https://discord.com/api"

        headers = {"Authorization": f"Bot {settings.token}",
                   'Content-Type': 'application/json'}
        json = {
            "content": "Hello",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Click me!",
                            "style": 1,
                            "custom_id": "click_one"
                        }
                    ]

                }
            ]
        }
        r = post(base_url + f"/v9/channels/{str(ctx.message.channel.id)}/messages", headers=headers, json=json)
        print(r.status_code)
        await ctx.send(f'Hello, {author.mention}!')

    @commands.command()
    async def pic(self, ctx):
        embed = Embed(color=0xff9900, title='Random Fox')  # Создание Embed'a
        embed.set_image(
            url='https://warframe.market/static/assets/icons/en/thumbs/Catalyzer_Link.8ffa520e67c52e10b51ccc1cec6b7f88.128x128.png')  # Устанавливаем картинку Embed'a
        await ctx.send(f'hi :100:', embed=embed)  # Отправляем Embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            # print(type(user))
            # print(user.bot)
            # print(reaction.message.reference.message_id)
            # print(user, reaction, str(__name__))
            pass

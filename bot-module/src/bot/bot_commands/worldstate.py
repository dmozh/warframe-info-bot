from ..services.worldstate import WorldStateService
from ..services.base import services
from ..settings import settings

from discord import Embed
from discord import Message
from discord.ext.commands import Context
from discord.ext import commands

from typing import Optional
from logger import log
from requests import post


class WorldState(commands.Cog, name="General"):
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

    @commands.command()
    async def sortie(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current sortie
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def fissures(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current fissures
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def invasions(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current events
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def nightwave(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current nightwave
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def void_trader(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current void_trader
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def events(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current events
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def alerts(self, ctx: Context, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current alerts
        :param ctx:
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            await service.action_on_command(str(ctx.message.content), platform, language)

    @commands.command()
    async def location_cycle(self, ctx: Context, location: str, platform: Optional[str] = 'pc', language: Optional[str] = 'ru'):
        """
        Get info for current cetus_cycle
        :param ctx:
        :param location:
        Must have argument, choose location
        Possible options [earth, cambion, cetus]
        :param platform: str
        Choose game platform
        Possible options [pc, ps4, xb1, swi]
        :param language: str
        Choose game language
        Possible options [de, es, fr, it, ko, pl, pt, ru, zh, en]
        :return:
        """
        service = WorldStateService(ctx.message.author, services, ctx)
        added = await services.add_service(ctx.message.author, service)
        if added:
            _ = str(ctx.message.content).replace("location_", f"{location.lower()}_")
            await service.action_on_command(_, platform, language)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            pass

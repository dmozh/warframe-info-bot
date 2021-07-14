from discord import Embed


class GeneralService:
    def __int__(self, ctx):
        self.ctx = ctx

    def gen_embed(self):
        embed = Embed(color=0xff9900, title='Random Fox')  # Создание Embed'a
        embed.set_image(
            url='https://warframe.market/static/assets/icons/en/thumbs/Catalyzer_Link.8ffa520e67c52e10b51ccc1cec6b7f88.128x128.png')  # Устанавливаем картинку Embed'a
        return embed

    def gen_msg(self):
        msg = self.ctx.message.author
        return msg

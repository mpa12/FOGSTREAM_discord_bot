import discord
from discord.ext import commands
from config import settings
from fact_pars import parse
from log import log_command


class MyBot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        # Bot initialization
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            self_bot=self_bot
        )
        self.remove_command("help")
        self.add_commands()

    async def on_ready(self):
        # Bot readiness
        print("[INFO]: Bot now online")

    def add_commands(self):
        @self.command()
        # Outputs a random fact
        async def random_fact_text(ctx):
            text = parse()[0]
            embed = discord.Embed(
                color=0x2f3236,
                title='Случайный факт',
                description=text)
            await ctx.send(embed=embed)

            log_command(
                'random_fact_text',
                ctx.author,
                'successfully'
            )

        @self.command()
        # Outputs a random image
        async def random_fact_img(ctx):
            img = parse()[1]
            embed = discord.Embed(
                color=0x2f3236,
                title='Случайная картинка с фактом',
            )
            embed.set_image(url=img)
            await ctx.send(embed=embed)

            log_command(
                'random_fact_img',
                ctx.author,
                'successfully'
            )

        @self.command()
        # Lists all commands
        async def help(ctx):
            embed = discord.Embed(
                color=0x2f3236,
                title='Все доступные команды',
                description="""```Основные команды:```
                !help - Все доступные команды
                !random_fact_text - Случайный факт в виде текста
                !random_fact_img - Бот отправляет рандомную аниме картинку"""
            )
            embed.set_author(
                name="FOGSTREAM",
                icon_url=(
                    "https://sun9-65.userapi.com/impf/c6364"
                    "26/v636426078/3270e/nMDuecW59rE.jpg?size=447"
                    "x408&quality=96&sign=5ac6b9e015b8e1369f3975a"
                    "e6f36303f&type=album"
                )
            )
            await ctx.send(embed=embed)

            log_command(
                'help',
                ctx.author,
                'successfully'
            )

        @self.event
        async def on_command_error(ctx, error):
            # Errors logging
            comand_name = ctx.command
            if comand_name is None:
                comand_name = str(error).split(' ')[1][1:-1]
            log_command(
                comand_name,
                ctx.author,
                'unsuccessfully'
            )

bot = MyBot(
    command_prefix=settings['prefix'],
    self_bot=False
)
bot.run(settings['token'])

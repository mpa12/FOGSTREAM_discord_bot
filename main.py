import discord
from discord.ext import commands
import asyncio
import json
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
                !random_fact_img - Бот отправляет рандомную аниме картинку
                !clear [количество сообщений] - Чистит чат
                !lvl - узнать количество сообщений"""
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

        @self.command()
        @commands.has_permissions(administrator=True)
        # clear chat
        async def clear(ctx, count):
            await ctx.channel.purge(limit=int(count)+1)
            await ctx.channel.send('Сообщения успешно удалены')
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=1)

            log_command(
                f'clear {count}',
                ctx.author,
                'successfully'
            )

        @self.command()
        # see lvl
        async def lvl(ctx):
            with open("lvls.json", "r") as f:
                id_us = str(ctx.author.id)
                data = dict(json.load(f))
                if id_us not in data:
                    await ctx.channel.send(
                        f'{ctx.author.mention}, количество сообщений - 0'
                    )
                else:
                    await ctx.channel.send(
                        f'{ctx.author.mention}, количество сообщений - {data[id_us]}'
                    )
            log_command(
                'lvl',
                ctx.author,
                'unsuccessfully'
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

        @self.event
        async def on_message(message):
            if self.user == message.author:
                return

            commands = [
                '!help',
                '!random_fact_text',
                '!random_fact_img',
                '!clear',
                '!lvl'
                ]
            if message.content.split(' ')[0] not in commands:
                await message.channel.send(
                    'Я тебя не понимаю - отправь  мне команду'
                    )
                log_command(
                    'on_message',
                    message.author,
                    'successfully'
                )
            else:
                await self.process_commands(message)

            with open("lvls.json", "r") as f:
                id_us = str(message.author.id)
                data = dict(json.load(f))
                if id_us not in data:
                    data[id_us] = 1
                else:
                    data[id_us] += 1
            with open('lvls.json', 'w') as f:
                json.dump(data, f)

bot = MyBot(
    command_prefix=settings['prefix'],
    self_bot=False
)
bot.run(settings['token'])

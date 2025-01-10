import discord
from discord.ext import commands
import random
from bot_logic import *

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='?', description=description, intents=intents)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.content.startswith('?deleteme'):
            msg = await message.channel.send('I will delete myself now...')
            await msg.delete()

            # this also works
            await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

    async def on_message_delete(self, message):
        msg = f'{message.author} has deleted the message: {message.content}'
        await message.channel.send(msg)

client = MyClient(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Junta dos numeros."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Lanzar un dado."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('El formato necesita ser NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='Elegir una de tus opciones de otra manera.')
async def choose(ctx, *choices: str):
    """Elige entre multiples opciones."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repitiendo...'):
    """Repite un mensajes multiples veces."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Dice cuando un miembro se unio."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Dice si un usuario es genial.

    En realidad solo revisa si un subcomando esta siendo invocado.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} no es genial')


@cool.command(name='bot')
async def _bot(ctx):
    """El bot es genial?"""
    await ctx.send('Si, el bot es genial.')

bot.run('TOKEN')
import discord
from discord.ext import commands
import os
import aiohttp
import io
from datetime import datetime
import asyncio
import random
import pyfiglet
import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config('config.json')

TOKEN = config['token']
PREFIX = config['prefix']
OWNER = config['owner_id']

bot = discord.Client()
bot = commands.Bot(command_prefix=PREFIX, self_bot=True,
                   intents=discord.Intents.all())
bot.remove_command("help")

bot.uptime = datetime.now()

@bot.command(aliases=['uinfo', 'ui'], description='Shows user info')
async def userinfo(ctx, *, user: discord.User = None):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    if user is None:
        await ctx.send('You need to mention a user or provide their ID!')
        return

    user_info = f'——————   User Info  ——————\nUser | {user.name}\nID | {user.id}\nCreated at | {user.created_at}'
    
    # Check if the command is used in a guild
    if ctx.guild:
        member = ctx.guild.get_member(user.id)
        if member:
            server_info = (
                f'——————   Server Info  ——————\n'
                f'Nickname | {member.nick}\n'
                f'Joined at | {member.joined_at}\n'
                f'Roles | {", ".join([role.name for role in member.roles if role.name != "@everyone"])}'
            )
            user_info += f"\n{server_info}"
    await ctx.send(user_info)

@bot.command(aliases=['sinfo', 'si'], description='Displays information about the server')
async def serverinfo(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    server = ctx.guild
    if not server:
        await ctx.send('This command must be used in a server!')
        return

    server_info = (
        f'——————   {server.name}  ——————\n'
        f'Creation Date | {server.created_at}\n'
        f'Owner | {server.owner} (ID: {server.owner_id})\n'
        f'Server ID | {server.id}\n'
        f'Region | {server.region}\n'
        f'Member Count | {server.member_count}\n'
        f'Channel Count | {len(server.channels)}\n'
        f'Emoji Count | {len(server.emojis)}\n'
        f'Role Count | {len(server.roles)}\n'
    )
    bot_count = sum(1 for member in server.members if member.bot)
    server_info += f'Bot Count | {bot_count}\n'
    await ctx.send(server_info)

@bot.command(aliases=['ss'], description='Takes a screenshot of the specified webpage.')
async def screenshot(ctx, url: str):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    access_key = 'KkYgqylu-i6R0g'
    screenshot_url = f'https://api.screenshotone.com/take?url={url}&access_key={access_key}'
    await ctx.send(screenshot_url)

@bot.command(aliases=['badtr'], description='Badly translates words into other words.')
async def badtranslate(ctx, *, text: str = None):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    if text is None:
        raise discord.ext.commands.errors.MissingRequiredArgument(param=inspect.Parameter('text', inspect.Parameter.POSITIONAL_OR_KEYWORD))

    def bad_translate(input_text):
        translation_table = str.maketrans("aeiou", "12345")
        translated = input_text.translate(translation_table)
        return ''.join(''.join(s)[:2] for s in translated.split())

    translated_text = bad_translate(text)
    await ctx.send(f'Original: {text}\nBadly Translated: {translated_text}')

@bot.command(aliases=['h'], description='WawaSB help')
async def help(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()
    
    uptime_duration = datetime.now() - bot.uptime
    hours, remainder = divmod(int(uptime_duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f'{hours}h {minutes}m {seconds}s'
    
    help_text = (
        f'——————   WawaSB Help  ——————\n'
        f'Uptime | {uptime_str}\n'
        f'Server  Count | {len(bot.guilds)}\n'
        f'Command Count | {len(bot.commands)}\n'
        f'——————   WawaSB CMDS  ——————\n'
        + ''.join(f'**{command.name}** | {command.description or "No description"}\n' for command in bot.commands)
    )

    await ctx.send(help_text)

@bot.command(aliases=["clear", "cl", "c"], description="Purges messages")
async def purge(ctx, amount: int):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == ctx.bot.user):
        try:
            await message.delete()
        except Exception:
            pass

@bot.command(aliases=["av"], description="Shows the avatar of the specified user")
async def avatar(ctx, *, user: discord.User = None):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    if user is None:
        await ctx.send('You need to mention a user or provide their ID!')
        return

    avatar_url = str(user.avatar_url)
    if avatar_url:
        await ctx.send(avatar_url)
    else:
        await ctx.send('This user has no avatar.')

@bot.command(aliases=["banr"], description="Shows the banner of the specified user")
async def banner(ctx, *, user: discord.User = None):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    if user is None:
        await ctx.send('You need to mention a user or provide their ID!')
        return

    banner_url = str(user.banner_url)
    if banner_url:
        await ctx.send(banner_url)
    else:
        await ctx.send('This user has no banner.')

@bot.command(aliases=["sicon"], description="Shows the server icon")
async def servericon(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    server = ctx.guild
    if not server:
        await ctx.send('This command must be used in a server!')
        return

    server_icon_url = str(server.icon_url)
    if server_icon_url:
        await ctx.send(server_icon_url)
    else:
        await ctx.send('This server has no icon.')

@bot.command(aliases=["sbanner"], description="Shows the server banner")
async def serverbanner(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    server = ctx.guild
    if not server:
        await ctx.send('This command must be used in a server!')
        return

    server_banner_url = str(server.banner_url)
    if server_banner_url:
        await ctx.send(server_banner_url)
    else:
        await ctx.send('This server has no banner.')

@bot.command(name="ascii", description="Converts text to ascii")
async def ascii(ctx, *, text):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    ascii_art = pyfiglet.figlet_format(text)
    await ctx.send(f'```{ascii_art}```')    

@bot.command(name="streaming", description="Sets a streaming status")
async def streaming(ctx, *, name):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await bot.change_presence(activity=discord.Streaming(name=name, url="https://www.twitch.tv/settings"))

@bot.command(name="playing", description="Sets a playing status")
async def playing(ctx, *, name):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await bot.change_presence(activity=discord.Game(name=name))

@bot.command(name="watching", description="Sets a watching status")
async def watching(ctx, *, name):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))

@bot.command(name="listening", description="Sets a listening status")
async def listening(ctx, *, name):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))

@bot.command(name="stop", description="Stops the self bots status")
async def stop(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await bot.change_presence(activity=None)

@bot.command(name="ping", description="Shows the bots latency")
async def ping(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name="uptime", description="Shows the bots uptime")
async def uptime(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    uptime_duration = datetime.now() - bot.uptime
    hours, remainder = divmod(int(uptime_duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f'{hours}h {minutes}m {seconds}s'

    await ctx.send(f'{uptime_str}')

@bot.command(name="massreact", description="Reacts to messagesthe channel")
async def massreact(ctx, emote):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()


    messages = await ctx.message.channel.history(limit=15).flatten()
    for message in messages:
        await message.add_reaction(emote)

@bot.command(name="reactuser", description="Keep reacting to a user's messages")
async def reactuser(ctx, member: discord.Member, emote):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    def check(message):
        return message.author == member

    try:
        while True:
            message = await bot.wait_for('message', check=check)
            await message.add_reaction(emote)
    except asyncio.CancelledError:
        pass

@bot.command(name="stopreact", description="Stops reacting to a user's messages")
async def stopreact(ctx):
    if ctx.author.id != OWNER:
        return

    await ctx.message.delete()

    def check(message):
        return message.author == member

    try:
        while True:
            message = await bot.wait_for('message', check=check)
            await message.remove_reaction(emote)
    except asyncio.CancelledError:
        pass

@bot.event
async def on_ready():
    print('Bot is ready!')
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(TOKEN, bot=False)

import asyncio
from os import getenv

import discord
from discord.ext import commands

from utility import fetch_target_user
from utility import quit_hex_role
from utility import get_color_from_pallet
from utility import fetch_hex_role

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';', intents=intents)


@bot.event
async def on_ready():
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game(name=str(len(bot.guilds)) + ' servers'))


@bot.event
async def on_guild_join(guild):
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game(name=str(len(bot.guilds)) + ' servers'))


@bot.event
async def on_guild_remove(guild):
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game(name=str(len(bot.guilds)) + ' servers'))


@bot.command(aliases=['p'])
async def pallet(ctx, target: str = ''):
    target_user: discord.Member = ctx.author
    if ctx.author.guild_permissions.administrator:
        if target != '':
            user = await fetch_target_user(ctx.guild, target)
            if user is not None:
                target_user = user

    await quit_hex_role(target_user)

    hex_str = get_color_from_pallet()
    role = await fetch_hex_role(ctx.guild, hex_str)
    await target_user.add_roles(role)


@bot.command(aliases=['c'])
async def color(ctx, hex_str: str, target: str = ''):
    target_user: discord.Member = ctx.author
    if ctx.author.guild_permissions.administrator:
        if target != '':
            user = await fetch_target_user(ctx.guild, target)
            if user is not None:
                target_user = user

    await quit_hex_role(target_user)

    if '#' not in hex_str:
        return
    role = await fetch_hex_role(ctx.guild, hex_str)
    await target_user.add_roles(role)


@bot.command()
async def reset(ctx, target: str = ''):
    target_user: discord.Member = ctx.author
    if ctx.author.guild_permissions.administrator:
        if target != '':
            user = await fetch_target_user(ctx.guild, target)
            if user is not None:
                target_user = user

    await quit_hex_role(target_user)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

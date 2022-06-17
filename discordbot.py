import asyncio
from os import getenv
from typing import Union

import discord
from discord.ext import commands

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


@bot.command(aliases=['r'])
async def reset(ctx, target: str = ''):
    target_user: discord.Member = ctx.author
    if ctx.author.guild_permissions.administrator:
        if target != '':
            user = await fetch_target_user(ctx.guild, target)
            if user is not None:
                target_user = user

    await quit_hex_role(target_user)


async def fetch_target_user(guild: discord.Guild, text: str) -> Union[discord.Member, None]:
    if text.isdigit():
        return await guild.fetch_member(int(text))
    else:
        if '@' in text:
            id_str = ((text.replace('<', '')).replace('@', '')).replace('>', '')
            return await guild.fetch_member(int(id_str))
    return None


async def fetch_hex_role(guild: discord.Guild, hex_str: str) -> discord.Role:
    sixteen_integer_hex = int(hex_str.replace('#', ''), 16)
    readable_hex = int(hex(sixteen_integer_hex), 0)

    for role in guild.roles:
        if role.name == hex_str:
            return role

    return await guild.create_role(name=hex_str, colour=readable_hex)


async def quit_hex_role(target: discord.Member):
    for role in target.roles:
        if '#' in role.name:
            if len(role.members) == 1:
                await role.delete()

            await target.remove_roles(role)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

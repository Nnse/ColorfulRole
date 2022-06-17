import tkinter
from tkinter import colorchooser
from typing import Union

import discord


def get_color_from_pallet() -> str:
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    c = colorchooser.askcolor(parent=root)
    if c is not None:
        root.destroy()
    root.mainloop()

    return str(c[1])


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

# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar


def make_sugg_embed(msg: discord.Message, args: list, token: str):
    sugg_embed = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
    sugg_embed.description = " ".join(args)
    author_name = f'{msg.author.name} [{msg.author.id}]'
    footer_content = f'[{token}]'
    sugg_embed.set_author(name=author_name, icon_url=user_avatar(msg.author))
    sugg_embed.set_footer(icon_url=msg.guild.icon_url, text=footer_content)
    return sugg_embed


async def serversuggestion(cmd: SigmaCommand, pld: CommandPayload):
    sugg_channel = await cmd.db.get_guild_settings(pld.msg.guild.id, 'suggestion_channel')
    if pld.args:
        if sugg_channel:
            channel = pld.msg.guild.get_channel(int(sugg_channel))
            if channel:
                sugg_token = secrets.token_hex(4)
                sugg_msg = await channel.send(embed=make_sugg_embed(pld.msg, pld.args, sugg_token))
                [await sugg_msg.add_reaction(r) for r in ['⬆', '⬇']]
                response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {sugg_token} submitted.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Cannot find suggestion channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Suggestion channel not set.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await pld.msg.channel.send(embed=response)
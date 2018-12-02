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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def suggestionchannel(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_channels:
        if pld.msg.channel_mentions:
            target = pld.msg.channel_mentions[0]
        else:
            if pld.args:
                if pld.args[0].lower() == 'disable':
                    await cmd.db.set_guild_settings(pld.msg.guild.id, 'suggestion_channel', None)
                    response = discord.Embed(color=0x66CC66, title=f'✅ Suggestion Channel disabled.')
                    await pld.msg.channel.send(embed=response)
                return
            else:
                target = pld.msg.channel
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'suggestion_channel', target.id)
        response = discord.Embed(color=0x66CC66, title=f'✅ Suggestion Channel set to #{target.name}.')
    else:
        response = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Manage Channels needed.')
    await pld.msg.channel.send(embed=response)
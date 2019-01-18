﻿# Apex Sigma: The Database Giant Discord Bot.
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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, ok, error, not_found


async def removecommand(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            trigger = pld.args[0].lower()
            custom_commands = pld.settings.get('custom_commands') or {}
            if trigger in custom_commands:
                del custom_commands[trigger]
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'custom_commands', custom_commands)
                response = ok(f'{trigger} has been removed.')
            else:
                response = not_found('Command not found.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)

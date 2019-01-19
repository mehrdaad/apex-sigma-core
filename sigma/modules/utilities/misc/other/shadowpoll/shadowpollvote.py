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
from sigma.core.utilities.generic_responses import ok, error, not_found


def origin(x, poll_file):
    return x.id == poll_file["origin"]["server"]


def check_roles(allowed_roles, all_users, user):
    members = []
    for member in all_users:
        if member.id == user.id:
            members.append(member)
    authorized = False
    for member_item in members:
        for allowed_role in allowed_roles:
            role = discord.utils.find(lambda x: x.id == allowed_role, member_item.roles)
            if role:
                authorized = True
                break
        if authorized:
            break
    return authorized


async def shadowpollvote(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        if len(pld.args) == 2:
            poll_id = pld.args[0].lower()
            try:
                choice_num = int(pld.args[1])
            except ValueError:
                choice_num = None
            if choice_num:
                poll_file = await cmd.db[cmd.db.db_nam].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    choice_count = len(poll_file['poll']['answers'])
                    if 0 > choice_num or choice_num > choice_count:
                        bad_choice = True
                    else:
                        bad_choice = False
                    if not bad_choice:
                        active = poll_file['settings']['active']
                        if active:
                            perms = poll_file['permissions']
                            chn_p = perms['channels']
                            rol_p = perms['roles']
                            usr_p = perms['users']
                            if not chn_p and not rol_p and not usr_p:
                                authorized = True
                            else:
                                rol_auth = check_roles(rol_p, cmd.bot.get_all_members(), pld.msg.author)
                                if pld.msg.channel:
                                    chn_auth = pld.msg.channel.id in chn_p
                                else:
                                    chn_auth = False
                                usr_auth = pld.msg.author.id in usr_p
                                if rol_auth or usr_auth or chn_auth:
                                    authorized = True
                                else:
                                    authorized = False
                            if authorized:
                                if str(pld.msg.author.id) in poll_file['votes']:
                                    ender = 'updated'
                                else:
                                    ender = 'recorded'
                                poll_file['votes'].update({str(pld.msg.author.id): choice_num})
                                poll_coll = cmd.db[cmd.db.db_nam].ShadowPolls
                                await poll_coll.update_one({'id': poll_id}, {'$set': poll_file})
                                response = ok(f'Your choice has been {ender}.')
                            else:
                                response = discord.Embed(color=0xFFCC4D, title='🔒 Not authorized to vote.')
                        else:
                            response = discord.Embed(color=0xFFCC4D, title='🔒 That poll is not active.')
                    else:
                        response = error('Choice number out of range.')
                else:
                    response = not_found('Poll not found.')
            else:
                response = error('Not a valid choice number.')
        else:
            response = error('Missing the choice number.')
    else:
        response = error('Missing poll ID and choice.')
    await pld.msg.channel.send(embed=response)

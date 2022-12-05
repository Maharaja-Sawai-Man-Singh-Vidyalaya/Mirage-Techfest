"""
Licensed under GNU General Public License v3.0


Permissions of this strong copyleft license are 
conditioned on making available complete source 
code of licensed works and modifications, which 
include larger works using a licensed work, 
under the same license. Copyright and license 
notices must be preserved. Contributors provide
an express grant of patent rights.

Permissions:
    Commercial use
    Modification
    Distribution
    Patent use
    Private use

Limitations:
    Liability
    Warranty

Conditions:
    License and copyright notice
    State changes
    Disclose source
    Same license

Kindly check out ../LICENSE
"""

import contextlib
import datetime
import traceback

import discord
from discord import app_commands
from discord.ext import commands


class JLHandlers(commands.Cog):
    """Welcome and Goodbye message handlers with events"""

    def __init__(self, bot):
        self.bot = bot
        self.category = [None]

    def _format_text(self, text, member):
        """
        VARIABLES:
        {$mention} -> mention user
        {$username} -> username (name without discriminator)
        {$discriminator} -> discriminator
        {$user} -> username with discriminator
        {$userid} -> user identifier
        {$pfp} -> user profile picture
        {$servericon} -> server icon
        {$botpfp} -> bot profile picture
        {$servername} -> server name
        {$serverid} -> server identifier
        """
        text = str(text)

        variables = {
            "{$mention}": member.mention,
            "{$username}": member.name,
            "{$discriminator}": member.discriminator,
            "{$user}": str(member),
            "{$userid}": member.id,
            "{$pfp}": self.bot.tools._get_mem_avatar(member),
            "{$servericon}": self.bot.tools._get_guild_icon(member),
            "{$botpfp}": self.bot.tools._get_mem_avatar(self.bot.user),
            "{$servername}": member.guild.name,
            "{$serverid}": member.guild.id,
        }

        for var, val in variables.items():
            text = text.replace(var, str(val))

        return text

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member or not member.guild:
            return

        embed = discord.Embed(
            color=self.bot._gen_colors(),
            timestamp=member.joined_at,
        )
        embed.set_author(
            name=self._format_text(
                self.bot.config["welcome_config"]["embed_author_title"], member
            ),
            icon_url=self._format_text(
                self.bot.config["welcome_config"]["embed_author_icon"], member
            ),
        )

        title = self._format_text(
            self.bot.config["welcome_config"]["embed_title"], member
        )
        description = self._format_text(
            self.bot.config["welcome_config"]["embed_description"], member
        )

        if title != "":
            embed.title = title
        if description != "":
            embed.description = description

        embed.set_footer(
            text=self._format_text(
                self.bot.config["welcome_config"]["embed_footer_text"], member
            ),
            icon_url=self._format_text(
                self.bot.config["welcome_config"]["embed_footer_icon"], member
            ),
        )

        _text = self._format_text(
            self.bot.config["welcome_config"]["embed_footer_icon"], member
        )
        channel = member.guild.get_channel(
            self.bot.config["welcome_config"]["msg_channel_id"]
        )

        if _text == "":
            return await channel.send(embed=embed)
        else:
            return await channel.send(
                content=self._format_text(
                    self.bot.config["welcome_config"]["text"], member
                ),
                embed=embed,
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member or not member.guild:
            return

        embed = discord.Embed(
            color=self.bot._gen_colors(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(
            name=self._format_text(
                self.bot.config["goodbye_config"]["embed_author_title"], member
            ),
            icon_url=self._format_text(
                self.bot.config["goodbye_config"]["embed_author_icon"], member
            ),
        )

        title = self._format_text(
            self.bot.config["goodbye_config"]["embed_title"], member
        )
        description = self._format_text(
            self.bot.config["goodbye_config"]["embed_description"], member
        )

        if title != "":
            embed.title = title
        if description != "":
            embed.description = description

        embed.set_footer(
            text=self._format_text(
                self.bot.config["goodbye_config"]["embed_footer_text"], member
            ),
            icon_url=self._format_text(
                self.bot.config["goodbye_config"]["embed_footer_icon"], member
            ),
        )

        _text = self._format_text(
            self.bot.config["goodbye_config"]["embed_footer_icon"], member
        )
        channel = member.guild.get_channel(
            self.bot.config["goodbye_config"]["msg_channel_id"]
        )

        if _text == "":
            return await channel.send(embed=embed)
        else:
            return await channel.send(
                content=self._format_text(
                    self.bot.config["goodbye_config"]["text"], member
                ),
                embed=embed,
            )


async def setup(bot):
    """Setup function for cog"""
    await bot.add_cog(JLHandlers(bot))

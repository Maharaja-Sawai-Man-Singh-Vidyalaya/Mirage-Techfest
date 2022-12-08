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


import asyncio
import random
import re
from typing import List
from urllib import parse

import discord
from discord import app_commands
from discord.ext import commands


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):

        global player1
        global player2

        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        content = None

        if view.current_player == view.X:
            if interaction.user != player1:
                await interaction.response.send_message(
                    "Its not your Turn!", ephemeral=True
                )
            else:
                self.style = discord.ButtonStyle.danger
                self.label = "X"
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                content = "It is now O's turn"

        else:
            if interaction.user != player2:
                await interaction.response.send_message(
                    "Its not your Turn!", ephemeral=True
                )
            else:
                self.style = discord.ButtonStyle.success
                self.label = "O"
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Fun(commands.Cog):
    """Cog full of commands to entertain your community."""

    def __init__(self, bot) -> None:
        self.bot = bot
        self.sra = self.bot.SRA(self.bot)
        self.category = ["fun"]

    # ---------------------------- General Fun cmds go below ------------------------------------

    @app_commands.command(name="pokedex", description="The official pokedex.")
    @app_commands.checks.cooldown(2, 5, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(pokemon="The pokemon whose data to show.")
    async def _pokedex(self, interaction: discord.Interaction, pokemon: str) -> None:
        """
        **Description:**
        Gets the info the given pokemon from the pokedex.

        **Args:**
        • `<pokemon>` - The pokemon name

        **Syntax:**
        ```
        /pokedex <pokemon>
        ```
        """
        results = await self.sra.get_data_for(
            f"pokemon/pokedex?pokemon={pokemon}", name="pokemon"
        )
        if results:
            if results.get("error") is not None:
                await interaction.response.send_message(results.get("error"))
                return
            else:
                # data
                name = results.get("name")
                desc = results.get("description")
                poke_type = results.get("type")  # list
                ht = results.get("height")
                weight = results.get("weight")
                _id = results.get("id")
                ability = results.get("abilities")
                eggs = results.get("egg_groups")
                stats = results.get("stats")
                url = (
                    f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{_id}.png"
                )

                # embed
                embed = discord.Embed(color=discord.Color.random())
                embed.title = str(name).title()
                embed.description = str(desc)

                embed.add_field(name="Weight", value=str(weight), inline=True)
                embed.add_field(name="Height", value=str(ht), inline=True)
                embed.add_field(
                    name="Ability" if len(ability) == 1 else "Abilities",
                    value=", ".join(ability),
                    inline=True,
                )
                embed.add_field(
                    name="Stats",
                    value=f"Hp: {stats['hp']}\nAttack: {stats['attack']}\nDefense: {stats['defense']}",
                    inline=True,
                )
                embed.add_field(name="Type", value=", ".join(poke_type), inline=True)
                embed.add_field(
                    name="Egg" if len(eggs) == 1 else "Eggs",
                    value=", ".join(eggs),
                    inline=True,
                )

                embed.set_thumbnail(url=url)
                embed.set_footer(text=f"ID: {str(_id)}")

                await interaction.response.send_message(embed=embed)
                return

        else:
            await interaction.response.send_message(
                f"Could not fetch the results for `{pokemon}`, try again later."
            )

    @app_commands.command(
        name="animal-facts",
        description="Shows facts about animals with an image as well.",
    )
    @app_commands.choices(
        animal=[
            app_commands.Choice(name="panda", value="panda"),
            app_commands.Choice(name="fox", value="fox"),
            app_commands.Choice(name="cat", value="cat"),
            app_commands.Choice(name="bird", value="bird"),
            app_commands.Choice(name="koala", value="koala"),
        ]
    )
    @app_commands.describe(animal="The animal to view facts about")
    @app_commands.checks.cooldown(2, 5, key=lambda i: (i.guild_id, i.user.id))
    async def _fact(self, interaction: discord.Interaction, animal: str) -> None:
        """
        **Description:**
        Shows facts about animals with an image as well.

        **Args:**
        • `<animal>` - The animal [panda|fox|cat|bird|koala]

        **Syntax:**
        ```
        /animal-fact <animal panda|fox|cat|bird|koala>
        ```
        """
        _paths = {"panda": "red_panda", "bird": "birb"}

        name = f"{animal.title()} facts"
        results = await self.sra.get_data_for(
            f"animal/{_paths.get(animal) or animal}",
            name=name,
        )

        if results:
            if results.get("error") is not None:
                return await interaction.response.send_message(results.get("error"))
            else:
                fact = results.get("fact")
                img_url = results.get("image")

                embed = discord.Embed(color=discord.Color.random())
                embed.title = name.title()
                embed.description = fact

                embed.set_image(url=img_url)

                return await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"Could not fetch the results for `{name}`, try again later."
            )

    @app_commands.command(name="embed", description="Generate an embed.")
    @app_commands.describe(
        title="Title of the embed",
        description="Description of the embed",
        color="Color in hex or defaults eg. '#FFFFFF' or 'white'",
        footer="Footer for the embed.",
        image_url="URL for a thumbnail.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
    async def _embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        color: str = None,
        footer: str = None,
        image_url: str = None,
    ):
        """
        **Description:**
        Generate an embed.

        **Args:**
        • `<title>` - Title of the embed
        • `<description>` - Description of the embed
        • `[color]` - Color in hex or defaults eg. '#FFFFFF' or 'white'
        • `[footer]` - Footer for the embed.
        • `[image_url]` - URL for a thumbnail.

        **Syntax:**
        ```
        /embed <title> <description> [color] [footer] [image_url]
        ```
        """
        embed = discord.Embed(title=title, description=description)
        if footer:
            embed.set_footer(text=footer)
        if image_url:
            embed.set_thumbnail(url=image_url)
        if color:
            if color[0] == "#":
                color = color.replace("#", "0x")
            try:
                color = int(color, 16)
            except ValueError as e:
                basic_colors = {
                    "blue": 0x0000FF,
                    "pink": 0xFFB6C1,
                    "purple": 0x800080,
                    "green": 0x00FF00,
                    "white": 0xFFFFFF,
                    "black": 0x000000,
                    "grey": 0x797373,
                    "red": 0xFF0000,
                }

                _color = basic_colors.get(color)
                if _color:
                    color = _color
                else:
                    return await interaction.response.send_message(
                        (
                            f"Your color `{color}` is not a valid hex code or a basic color.\n"
                            "Example of a valid hex code: `#FFFFFF`, `#000000`\n"
                            "Basic colors:\n`blue`, `pink`\n`purple`, `green`\n`white`, `black`\n`grey`, `red`"
                        )
                    )

        embed.color = color or self.bot._gen_colors()
        try:
            await interaction.response.send_message("Creating!")
            await interaction.delete_original_message()
            await interaction.channel.send(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    title=" ".join(
                        re.compile(r"[A-Z][a-z]*").findall(e.__class__.__name__)
                    ),
                    description=str(e),
                )
            )

    @app_commands.command(
        name="reply", description="Reply to a specific message using me."
    )
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(
        message_id="The message ID to reply to.", message="The reply"
    )
    async def _reply(
        self, interaction: discord.Interaction, message_id: str, message: str
    ):
        """
        **Description:**
        Reply to a specific message using me.

        **Args:**
        • `<message_id>` - The message ID to reply to.
        • `<message>` - The Reply

        **Syntax:**
        ```
        /reply <message_id> <message>
        ```
        """
        try:
            msg = await interaction.channel.fetch_message(int(message_id))
        except (discord.errors.NotFound, ValueError):
            return await interaction.response.send_message(
                "Can't find your referenced message, use a correct ID."
            )

        await interaction.response.send_message("Okay!")
        await interaction.delete_original_message()
        await msg.reply(
            message, allowed_mentions=discord.AllowedMentions(replied_user=False)
        )

    # ----------------------------- GAMES -----------------------------------

    @app_commands.command(
        name="tictactoe", description="Play tictactoe, you can play with yourself too."
    )
    @app_commands.describe(enemy="Your opponent")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def tictactoe(self, interaction: discord.Interaction, enemy: discord.Member):
        """
        **Description:**
        Play tictactoe, you can play with yourself too.

        **Args:**
        • <enemy>

        **Syntax:**
        ```
        /tictactoe <enemy>
        ```
        """
        await interaction.response.defer(thinking=True)

        if enemy.bot:
            return await interaction.followup.send(
                f"You can't play with a bot, you can play with yourself though.\nTry `/tictactoe enemy:{interaction.user}`"
            )
        await interaction.followup.send("Tic Tac Toe: X goes first", view=TicTacToe())

        global player1
        global player2

        player1 = interaction.user
        player2 = enemy

    @app_commands.command(
        name="8ball", description="Ask a question and get a random answer"
    )
    @app_commands.describe(question="The question to be answered.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
    async def _ball(self, interaction: discord.Interaction, question: str):
        """
        **Description:**
        Ask a question and get a random answer

        **Args:**
        • `[question]` - The question to be answered.

        **Syntax:**
        ```
        /8ball <question>
        ```
        """
        await interaction.response.defer(thinking=True)
        res = await self.bot.http._HTTPClient__session.get(
            f"https://eightballapi.com/api?{parse.quote(question)}&lucky=false"
        )
        res = await res.json()

        embed = discord.Embed(
            timestamp=interaction.created_at, color=self.bot._gen_colors()
        )
        embed.set_author(
            name="8ball...", icon_url=self.bot.tools._get_mem_avatar(interaction.user)
        )

        embed.add_field(name="Question: ", value=question, inline=False)
        embed.add_field(name="Answer: ", value=res["reading"], inline=False)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="dice", description="Roll a dice.")
    @app_commands.checks.cooldown(1, 2, key=lambda i: (i.guild_id, i.user.id))
    async def dice(self, interaction: discord.Interaction):
        """
        **Description:**
        Roll a dice.

        **Args:**
        • None

        **Syntax:**
        ```
        /dice
        ```
        """

        outputs = [
            "https://cdn.discordapp.com/emojis/755891608859443290.webp?size=96&quality=lossless",
            "https://cdn.discordapp.com/emojis/755891608741740635.webp?size=96&quality=lossless",
            "https://cdn.discordapp.com/emojis/755891608251138158.webp?size=96&quality=lossless",
            "https://cdn.discordapp.com/emojis/755891607882039327.webp?size=96&quality=lossless",
            "https://cdn.discordapp.com/emojis/755891608091885627.webp?size=96&quality=lossless",
            "https://cdn.discordapp.com/emojis/755891607680843838.webp?size=96&quality=lossless",
        ]

        await interaction.response.send_message(random.choice(outputs))

    @app_commands.command(name="coinflip", description="Flip a coin.")
    @app_commands.checks.cooldown(1, 2, key=lambda i: (i.guild_id, i.user.id))
    async def flip(self, interaction: discord.Interaction):
        """
        **Description:**
        Flip a coin.

        **Args:**
        • None

        **Syntax:**
        ```
        /coinflip
        ```
        """

        outputs = [
            "https://i.ibb.co/pwgPZBY/image.png",
            "https://i.ibb.co/gvd5M5y/image.png",
        ]

        await interaction.response.send_message(random.choice(outputs))

    @app_commands.command(
        name="number-guessing",
        description="Guess a random number from a given range, you get 7 chances.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(
        start="The start number of the range (inclusive)",
        end="The end number of the range (inclusive)",
    )
    async def guess_the_num(
        self, interaction: discord.Interaction, start: int, end: int
    ):
        """
        **Description:**
        Guess a random number from a given range, you get 7 chances.

        **Args:**
        • <start>: The start number of the range
        • <end>: The end number of the range

        **Syntax:**
        ```
        /number-guessing <start> <ending>
        ```
        """

        if start < 0 or end < 0:
            return await interaction.response.send_message(
                "numbers cannot be negative."
            )

        if (end - start) < 10 or (end - start) > 1000:
            return await interaction.response.send_message(
                "The range should at least differ by 10 and max by 1000."
            )

        num = random.randrange(start, end + 1)

        msg = await interaction.response.send_message("Guess the number")

        def check(m):
            try:
                content = int(m.content)
            except:
                return False
            else:
                if m.author == interaction.user and content <= end and content >= start:
                    return True
                else:
                    return False

        attempts = 0

        while 1:
            try:
                message = await self.bot.wait_for("message", timeout=30, check=check)
            except asyncio.TimeoutError:
                return await interaction.edit_original_response(
                    content="You did not respond on time :|"
                )
            else:
                if int(message.content) == num:
                    await interaction.edit_original_response(
                        content="You guessed it Right 🎉!",
                        attachments=[discord.File("./assets/stickman/happy.png")],
                    )
                    break
                else:
                    attempts += 1
                    if attempts == 7:
                        await interaction.edit_original_response(
                            content=f"You could not guess the number, it was `{num}`",
                            attachments=[
                                discord.File(f"./assets/stickman/{attempts}.png")
                            ],
                        )
                        break
                    else:
                        await interaction.edit_original_response(
                            content="Wrong!",
                            attachments=[
                                discord.File(f"./assets/stickman/{attempts}.png")
                            ],
                        )

    @app_commands.command(name="meme", description="Get a meme from r/memes.")
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def _meme(self, interaction: discord.Interaction):
        """
        **Description:**
        Get a meme from r/memes.

        **Args:**
        • None

        **Syntax:**
        ```
        /meme
        ```
        """

        await interaction.response.defer(thinking=True)

        res = await self.bot.http._HTTPClient__session.get(
            f"https://www.reddit.com/r/memes/random/.json"
        )
        res = await res.json()
        parent = res[0]["data"]["children"][0]["data"]

        embed = discord.Embed(
            color=self.bot._gen_colors(), timestamp=interaction.created_at
        )
        embed.title = parent["title"]
        embed.description = parent["selftext"]
        embed.set_image(url=parent["url"])
        embed.set_footer(
            text=f"👍 {parent['ups']} | 💬 {parent['num_comments']} • by {parent['author']}",
            icon_url=self.bot.tools._get_mem_avatar(interaction.user),
        )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    """Setup function for cog"""
    await bot.add_cog(
        Fun(bot), guild=discord.Object(id=bot.config["bot_config"]["guild_id"])
    )

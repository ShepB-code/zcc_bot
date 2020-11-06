#Settings cog for the ZCC Events Bot
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get

class Settings(commands.Cog):
    prefix = "+"
    """Cog for the Settings Command"""
    def __init__(self, bot):
        self.bot = bot
        self.settings_embed = None
        self.settings_dict = {"KillSetting": 0, 1: 0}
        self.bot_id = 757700872791654500
        prefix = self.bot.command_prefix

    @commands.group(
        help="A command to access and update calculation settings.\n`{prefix}settings` to view current settings"
    )
    @commands.has_guild_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            if not self.settings_dict:
                await ctx.send("You don't have any current settings. You can add settings or update settings by using the `?settings update` command.")
            else:
                await ctx.send(embed=self.create_embed())
    
    @settings.command(
        help="`{prefix}settings update` to update settings"
    )
    async def update(self, ctx):

        channel = ctx.channel
        author = ctx.message.author

        def msg_check(m):
            return m.author == author and m.channel == channel

        await ctx.send("How many points should each kill give?")
        while True:
            try:
                kill_setting_msg = await self.bot.wait_for('message', check=msg_check)
                kill_setting = int(kill_setting_msg.content)
                break
            except ValueError:
                await ctx.send("You must enter a valid number!")
        
        await ctx.send("How many places should score?")
        
        while True:
            try:
                num_places_msg = await self.bot.wait_for('message', check=msg_check)
                num_places = int(num_places_msg.content)
                break
            except ValueError:
                await ctx.send("You must enter a valid number!")

        
        
        self.settings_dict = {"KillSetting": kill_setting}

        for i in range(num_places):
            await ctx.send(f"How many points should {i + 1} get?")
            while True:
                try:
                    scores_msg = await self.bot.wait_for('message', check=msg_check)
                    break
                except ValueError:
                    await ctx.send("You must enter a valid number!")

            self.settings_dict[i + 1] = int(scores_msg.content)

        await ctx.send(embed=self.create_embed())

    def get_settings(self):
        return self.settings_dict
        
    def create_embed(self):
        settings_embed = discord.Embed(
            title='Settings',
            description='Current Settings',
            color=discord.Color.blue()
        )
        settings_embed.add_field(name="Points Per Kill", value=self.settings_dict["KillSetting"])
        for key, value in self.settings_dict.items():
            if not isinstance(key, int):
                continue
            settings_embed.add_field(name=f"Place {key} Score", value=value)
        settings_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
        return settings_embed
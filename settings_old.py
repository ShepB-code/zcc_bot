#Settings cog for the ZCC Events Bot
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get

class Settings(commands.Cog):
    """Cog for the Settings Command"""
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = 757700872791654500
        self.settings_embed = None
        self.settings_dict = {}
    @commands.group()
    async def settings(self, ctx):

        if ctx.invoked_subcommand is None:
            if not self.settings_embed:
                await ctx.send("You don't have any current settings. You can add settings or update settings by using the `?settings update` command.")
            else:
                
                await ctx.send(embed=self.settings_embed)
    
    @settings.command()
    async def update(self, ctx):

        channel = ctx.channel
        message = ctx.message
        author = ctx.message.author
        bot_id = 757700872791654500

        await ctx.send(author.guild_permissions)

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

        settings_embed = discord.Embed(
            title='Settings',
            description='Current Settings',
            color=discord.Color.blue()
        )
        settings_embed.add_field(name="Points Per Kill", value=kill_setting)
        
        self.settings_dict = {"KillSetting": kill_setting}

        for i in range(num_places):
            await ctx.send(f"How many points should {i + 1} get?")
            while True:
                try:
                    scores_msg = await self.bot.wait_for('message', check=msg_check)
                    settings_embed.add_field(name=f"Place {i + 1} Score", value=int(scores_msg.content))
                    break
                except ValueError:
                    await ctx.send("You must enter a valid number!")

            self.settings_dict[i + 1] = int(scores_msg.content)


        settings_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.user.id.avatar_url)

        await ctx.send(embed=settings_embed)

    def get_settings(self):
        return self.settings_dict
        
#Cog for the info command
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio


class Info(commands.Cog):
    prefix = "+"
    """Cog for the Info Command"""

    def __init__(self, bot):
        self.bot = bot
        self.prefix =  self.bot.command_prefix


    @commands.command(
        help="Hi I'm here to help"
    )
    async def info(self, ctx):

        cogs = list(self.bot.cogs)

            
        shep_id = 498331656822849536
        peter_id = 516652903763542017
        message = ctx.message
        emoji_list = ['🤖', '🏠']

        info_embed_home = discord.Embed(
            title="Info",
            description=f"Information about the ZCC Bot\nReact with {emoji_list[0]} to see the commands for this bot",
            color=discord.Color.blue()
        )
        info_embed_home.add_field(name="Created", value="September, 2020", inline=True)
        info_embed_home.add_field(name="Creators", value=f"{self.bot.get_user(shep_id).mention} & {self.bot.get_user(peter_id).mention}", inline=True)
        info_embed_home.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
        
        commands_embed = discord.Embed(
            title="Commands",
            description=f"Commands in the ZCC Bot\nReact with {emoji_list[1]} to see info about the ZCC Bot",
            color=discord.Color.blue()
        )

        for name in cogs:
            cog = self.bot.get_cog(name)
            for c in [command for command in cog.walk_commands()]:
                commands_embed.add_field(name=c.name, value=c.help.replace("{prefix}", self.prefix), inline=False)
                
        """
        commands_embed.add_field(name="Settings", value=f"`{prefix}settings` to check current settings\n`{prefix}settings update` to update settings", inline=False)
        commands_embed.add_field(name="Calculate", value=f"There are two ways to use this command\n\nFirst Usage:\n`{prefix}calc or {prefix}c`, followed by two parameters: `kills` and `place number`\n\nSecond Usage:\n`{prefix}calc or {prefix}c`, followed by at least 4 paramters: `player_name`, `match_name`, `kills`, and `placing`.\n\nUsing this same format, you can enter and calculate many matches in one call.\n\nExample: `{prefix}calc Shep MatchOne 10 1 MatchTwo 20 2`", inline=False)
        commands_embed.add_field(name="Results", value=f"`{prefix}results` to get the top *10* scores that have been entered.\nYou can add any integer as a parameter to this function to get specific placings.\nExample: `{prefix}results 50` would get the top 50 scores.", inline=False)
        """
        embed_message = await ctx.send(embed=info_embed_home)

        commands_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
        for emoji in emoji_list: 
            await embed_message.add_reaction(emoji)

            
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in emoji_list


        i = 0
        j = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                
                if str(reaction) == emoji_list[0]:
                    i += 1 #using this to check which embed i'm on
                    await embed_message.edit(embed=commands_embed)
                elif str(reaction) == emoji_list[1]:
                    j += 1
                    await embed_message.edit(embed=info_embed_home)
            except asyncio.TimeoutError:
                if i > j:
                    commands_embed.color = discord.Color.dark_grey()
                    commands_embed.description = 'Inactive'
                    await embed_message.edit(embed=commands_embed)
                    break
                else: #assuming that j > i
                    info_embed_home.color = discord.Color.dark_grey()
                    info_embed_home.description = 'Inactive'
                    await embed_message.edit(embed=info_embed_home)
                    break
                

            
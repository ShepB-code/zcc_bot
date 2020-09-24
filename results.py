#Results Cog for the ZCC Events Bot

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
from calculate import Calculate

class Results(commands.Cog):
    """Cog for the Results command"""

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def results(self, ctx, *args):
        

            
        leaderboard = self.bot.get_cog('Calculate').get_sorted_leaderboard()
        if not args:
            leaderboard_num = min(10, len(leaderboard))
        else: 
            leaderboard_num = min(int(args[0]), len(leaderboard))
    
        leaderboard_embed = discord.Embed(
            title=f'Top {leaderboard_num} Leaderboard',
            color=discord.Color.blue()
        )
        for i in range(leaderboard_num):
            leaderboard_embed.add_field(name=f"{i + 1}. {leaderboard[i][0]}", value=f"Score: **{leaderboard[i][1]}**", inline=False)
        
        
        leaderboard_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)


        await ctx.send(embed=leaderboard_embed)
        
        
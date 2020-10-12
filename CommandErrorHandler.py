#Cog for the zcc_bot error handler
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get

class CommandErrorHandler(commands.Cog):
    """Cog for the CommandErrorHandler Command"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You are missing the {error.missing_perms} required to run this command")
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("That command doesn't exist!")
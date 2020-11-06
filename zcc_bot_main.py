#ZCC Project

import discord
import itertools
from discord.ext import commands
import discord.utils

#Importing Cogs
#import settings
import settings
import calculate
import results
import CommandErrorHandler
import info
import DataWriter
import DataSender
import MatchMaker

import stats
guild_id = 765015176587640842
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='+', intents=intents)

stats.command_impact = 0


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.invisible, activity=discord.Game('Made by Shep and Peter!'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.event
async def on_command_completion(ctx):
    stats.command_impact += 1
    
bot.add_cog(settings.Settings(bot))
bot.add_cog(calculate.Calculate(bot))
bot.add_cog(results.Results(bot))
#bot.add_cog(CommandErrorHandler.CommandErrorHandler(bot))
bot.add_cog(info.Info(bot))
bot.add_cog(DataSender.DataSender(bot, guild_id))
bot.add_cog(DataWriter.DataWriter(bot))
bot.add_cog(MatchMaker.MatchMaker(bot))
with open('work_bot_token.txt', 'r') as f:
    bot.run(f.read().strip())
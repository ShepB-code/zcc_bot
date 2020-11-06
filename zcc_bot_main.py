#ZCC Project

import discord
import itertools
from discord.ext import commands
import discord.utils
import os
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
import help_functions

guild_id = 765015176587640842
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='+', intents=intents)


command_impact = 0


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Made by Shep and Peter!'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.event
async def on_command_completion(ctx):
    global command_impact
    command_impact += 1

def get_impact():
    global command_impact
    return command_impact

bot.add_cog(settings.Settings(bot))
bot.add_cog(calculate.Calculate(bot))
bot.add_cog(results.Results(bot))
bot.add_cog(CommandErrorHandler.CommandErrorHandler(bot))
bot.add_cog(info.Info(bot))
bot.add_cog(DataSender.DataSender(bot, guild_id))
bot.add_cog(DataWriter.DataWriter(bot))
bot.add_cog(MatchMaker.MatchMaker(bot))
bot.add_cog(help_functions.Impact(bot))

if "BOT_TOKEN" in os.environ.keys():
    print("Starting bot...")
    bot.run(os.environ['BOT_TOKEN'])
else:
    print(os.environ.keys())
    with open('work_bot_token.txt', 'r') as f:
        bot.run(f.read().strip())
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

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Made by Shep and Peter!'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

bot.add_cog(settings.Settings(bot))
bot.add_cog(calculate.Calculate(bot))
bot.add_cog(results.Results(bot))
bot.add_cog(CommandErrorHandler.CommandErrorHandler(bot))
bot.add_cog(info.Info(bot))

with open('token.txt', 'r') as f:
    bot.run(f.read().strip())

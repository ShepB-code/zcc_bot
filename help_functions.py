#global command_impact
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json

class Impact(commands.Cog):
    command_impact = 0
    guild = 0    
    def __init__(self, bot):
        self.bot = bot
        self.file_name = "data.json"
    def write_stats(self, key, value):
        with open(self.file_name, 'r') as f:
            file_dict = json.load(f)
        
        file_dict["stats"][key] = value
        with open(self.file_name, "w") as outfile: 
            json.dump(file_dict, outfile, indent=4)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        Impact.command_impact += 1
        self.write_stats("command_impact", Impact.command_impact)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        Impact.guild += 1
        self.write_stats("guilds", Impact.guild)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        Impact.guild -= 1
        self.write_stats("guilds", Impact.guild)
        
        
            
def embed_footer():
    embed_footer = f"Made by Shep and Peter - Bot Impact: {Impact.command_impact}"

    return embed_footer
async def message_wait_for(bot, ctx, msg, timeout=20):
    try:
        def message_check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        user_message = await bot.wait_for("message", timeout=timeout, check=message_check)
        
        return user_message
    except asyncio.TimeoutError:
        new_msg = msg.content + " (Inactive)"
        await msg.edit(content=new_msg)
    
        raise asyncio.TimeoutError

async def reaction_wait_for(bot, ctx, emojis, msg, timeout=20):
    try:
        for emoji in emojis:
            await msg.add_reaction(emoji)
        def reaction_check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emojis
        reaction, user = await bot.wait_for("reaction_add", timeout=timeout, check=reaction_check)
        return str(reaction), user
    
    except asyncio.TimeoutError:
        if len(msg.embeds):
            embed = msg.embeds[0]
            embed.color = discord.Color.dark_grey()
            embed.title += "(Inactive)"
            await msg.edit(embed=embed)
        else:
            new_msg = msg.content + " (Inactive)"
            await msg.edit(content=new_msg)

        raise asyncio.TimeoutError
    
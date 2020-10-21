#Cog to load data from discord
import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import json

from clanClass import ClanClass
from playerClass import PlayerClass

class DataWriter(commands.Cog):
    """Cog for the Data command"""

    def __init__(self, bot):
        self.bot = bot

    def write_json(self, load_type, data):
        file_dict = dict()
        with open("data.json", 'r') as f:
            file_dict = json.load(f)
        
        if load_type == "clan":
            file_dict["clan"][data["clan_name"]] = data
        elif load_type == "player":
            file_dict["player"][data["player_name"]] = data
            
            
        '''
        elif isinstance(data) == Player:
            file_dict["player"][data.get_name()] = data
        '''
        with open("data.json", "w") as outfile: 
            json.dump(file_dict, outfile, indent=4)
    
    #@commands.has_guild_permissions(administrator=True)
    @commands.group()
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please invoke a subcommand `+add clan or +add player`")

    @add.command()
    async def clan(self, ctx, *args):
        clan_name = args[0].lower()
        creation_date = args[1]
        clan_leaders = args[2]
        clan_image = args[3]
        
        clan = ClanClass(clan_name, creation_date, clan_leaders, clan_image)
        clan_data = clan.get_clan_data()
        self.write_json("clan", clan_data)
        
        
    
    
    @add.command()
    async def player(self, ctx, member : discord.Member, *args):
        player_name = member.name.lower()
        clan = args[0].lower()
        #player_image = args[1]
        player_image = str(member.avatar_url)
        
        await ctx.send(f"name {player_name} clan {clan} player_image {player_image}")
        player = PlayerClass(player_name, clan, player_image)
        player_data = player.get_player_data()
        self.write_json("player", player_data)

    



    


    
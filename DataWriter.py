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
    @commands.group(
        help="`{prefix}add` is used to add clans and players"
    )
    async def add(self, ctx):
        prefix = self.bot.command_prefix
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Please invoke a subcommand `{prefix}add clan` or `{prefix}add player`")

    @add.command(
        help="`{prefix}add clan` is used to add a clan to a json file.\nUsage: `{prefix}add clan clan_name, creation_date, clan_leader(s), clan_image` (No commas)"
    )
    async def clan(self, ctx, *args):
        new_args = (" ".join(args)).split(":")
        clan_name = new_args[0]

        clan_info = new_args[1].split()
        creation_date = clan_info[0]
        clan_leaders = clan_info[1]
        clan_image = clan_info[2]
        
        clan = ClanClass(clan_name, creation_date, clan_leaders, clan_image)
        clan_data = clan.get_clan_data()
        self.write_json("clan", clan_data)
        
        
    
    
    @add.command(
        help="`{prefix}add player` is used to add a player to a json file.\nUsage: `{prefix}add player mention_player, player_clan` (No commas)"
    )
    async def player(self, ctx, member : discord.Member, *args):
        player_name = member.name.lower()
        clan = args[0].lower()
        #player_image = args[1]
        player_image = str(member.avatar_url)
        
        await ctx.send(f"name {player_name} clan {clan} player_image {player_image}")
        player = PlayerClass(player_name, clan, player_image)
        player_data = player.get_player_data()
        self.write_json("player", player_data)

    



    


    
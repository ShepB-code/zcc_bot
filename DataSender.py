#Cog to set info for clans & matches

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json
from clanClass import ClanClass

class DataSender(commands.Cog):
    """Cog for the clan command"""

    def __init__(self, bot):
        self.bot = bot
    
    def read_json(self):
        with open("data.json", 'r') as f:
            return json.load(f)
    def write_json(self, load_type, data):
        file_dict = dict()
        with open("data.json", 'r') as f:
            file_dict = json.load(f)
        if load_type == "clan":
            file_dict["clan"][data['clan_name']] = data
        elif load_type == "change_clan":
            file_dict["clan"] = data
        elif load_type == "player":
            file_dict["player"][data["player_name"]] = data
        

        with open("data.json", "w") as outfile: 
            json.dump(file_dict, outfile, indent=4)
        
    # This function was written very late at night, please do not judge
    @commands.command()
    async def clan(self, ctx, *args):
        message = ctx.message
        author = ctx.message.author
        channel = ctx.channel
        guild_id = 740596566632562760
        clan_name = args[0]
        clan_data = self.read_json()["clan"]
        current_clan = clan_data[clan_name]

        def create_embed(current_clan):
            clan_embed = discord.Embed(
                title=current_clan['clan_name'] + " 📜",
                description="Clan Information and Stats",
                color=discord.Color.blue()
                )

            clan_embed.add_field(name="Leader(s) 👑", value=current_clan['leaders'], inline=True)
            clan_embed.add_field(name="Creation Date ⏰", value=current_clan['creation_date'], inline=True)
            clan_embed.add_field(name="CS Wins 🏆", value=current_clan['cs_wins'], inline=False)
            clan_embed.add_field(name="Matches Played 🥊", value=current_clan['cs_matches'], inline=True)
            clan_embed.add_field(name="Winrate 📈", value=current_clan['win_rate'], inline=False)
            clan_embed.set_image(url=current_clan['clan_image'])
            clan_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
            
            return clan_embed

        if ctx.guild.id == guild_id and author.guild_permissions.administrator:
            
            
            
            if clan_name in clan_data.keys():
                #Add if/else for admin
                clan_embed = create_embed(current_clan)
                embed_message = await ctx.send(embed=clan_embed)
                embed_dict = clan_embed.to_dict()
                
                emoji_list = ["📜","👑", "⏰", "📷","🏆", "🥊", "❌"]

                for emoji in emoji_list:
                    await embed_message.add_reaction(emoji)

                def reaction_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in emoji_list
                def message_check(message):
                        return message.author == author and message.channel == channel
                try:
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)
                        type_change = ""
                        
                        
                        if str(reaction) == "📜":
                            msg = await ctx.send("Please enter a new name: ")
                            type_change = "clan_name"
                        elif str(reaction) == "👑":
                            msg = await ctx.send("Please enter a new leader(s): ")
                            type_change = "leaders"
                            i = 0
                        elif str(reaction) == "⏰":
                            msg = await ctx.send("Please enter a new creation date: ")
                            type_change = "creation_date"
                            i=1
                        elif str(reaction) == "📷":
                            msg = await ctx.send("Please enter a new clan image URL: ")
                            type_change = "clan_image"
                        elif str(reaction) == "🏆":
                            msg = await ctx.send("Please enter the amount of wins you want to add: ")
                            type_change = "cs_wins"
                            i=2
                        elif str(reaction) == "🥊":
                            msg = await ctx.send("Please enter a new match: ")
                            type_change = "cs_matches"
                            i=3
                        elif str(reaction) == "❌":
                            raise asyncio.TimeoutError
                        
                        update_info = await self.bot.wait_for('message', timeout=20.0, check=message_check)
                        
                        update_info = update_info.content

                        if type_change == "clan_name" or type_change == "clan_image" or type_change == "leaders" or type_change == "creation_date":
                            current_clan[type_change] = update_info
                            
                        else:
                            if type_change == "cs_wins":
                                current_clan["cs_wins"] += int(update_info)
                                current_clan["cs_matches"] += int(update_info)
                                embed_dict['fields'][3]['value'] = current_clan["cs_matches"] #auto update

                            else:
                                current_clan["cs_matches"] += int(update_info)

                            current_clan['win_rate'] = float(current_clan["cs_wins"]) / float(current_clan["cs_matches"])
                            embed_dict['fields'][4]['value'] = str(current_clan['win_rate'] * 100) + "%" #auto update

                        
                        if type_change == "clan_name":
                            embed_dict['title'] = current_clan[type_change]
                            clan_data[current_clan[type_change]] = clan_data.pop(clan_name)
                            self.write_json("change_clan", clan_data)
                            #TODO Duplicate clans
                        elif type_change == "clan_image":
                            embed_dict["image"]["url"] = current_clan[type_change]
                            self.write_json("clan", current_clan)
                        else:
                            embed_dict['fields'][i]['value'] = current_clan[type_change]
                            self.write_json("clan", current_clan)

                        
                        await embed_message.edit(embed=discord.Embed.from_dict(embed_dict))



                except asyncio.TimeoutError:
                    clan_embed.color = discord.Color.dark_grey()
                    clan_embed.title += " (Inactive)"
                    await embed_message.edit(embed=clan_embed)
        else:
            embed_message = await ctx.send(embed=create_embed(current_clan))

            #raise discord.ext.commands.MissingPermissions(missing_perms="Administrator") 
        
    @commands.command()
    async def player(self, ctx, *args):
        message = ctx.message
        author = ctx.message.author
        channel = ctx.channel
        guild_id = 740596566632562760
        player_name = args[0]
        player_data = self.read_json()["player"]
        current_player = player_data[player_name]

        def create_embed(current_player):
            player_embed = discord.Embed(
                title=current_player["player_name"],
                description="Player information and stats",
                color=discord.Color.blue()
            )
            player_embed.add_field(name="Clan Affiliation", value=f'{current_player["clan"]} react with 🔎 to view the clan', inline=True)
            player_embed.add_field(name="Wins", value=current_player["cs_wins"], inline=False)
            player_embed.add_field(name="Total Matches Played", value=current_player["cs_matches"], inline=True)
            player_embed.add_field(name="Win Rate", value=current_player["win_rate"], inline=False)
            player_embed.set_thumbnail(url=current_player["player_image"])

            return player_embed

        if ctx.guild.id == guild_id and author.guild_permissions.administrator:

            if player_name in player_data.keys():
                player_embed = create_embed(current_player)
                embed_message = await ctx.send(embed=player_embed)
                embed_dict = player_embed.to_dict()

                emoji_list = ["📜", "📷","🏆", "🥊", "🔎","❌"]

                for emoji in emoji_list:
                    await embed_message.add_reaction(emoji)

                def reaction_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in emoji_list
                def message_check(message):
                        return message.author == author and message.channel == channel
                
                try:
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)
                        type_change = ""

                        if str(reaction) == "📜":
                            msg = await ctx.send("Please enter a new clan: ")
                            type_change = "clan"
                            i = 0
                        elif str(reaction) == "📷":
                            await ctx.send("Not added yet")
                            type_change = "player_image"
                        elif str(reaction) == "🏆":
                            msg = await ctx.send("Please enter the amount of wins you want to add: ")
                            type_change = "cs_wins"
                            i = 1
                        elif str(reaction) == "🥊":
                            msg = await ctx.send("Please the matches you want to add: ")
                            type_change = "cs_matches"
                            i = 2
                        elif str(reaction) == "🔎":
                            pass
                        elif str(reaction) == "❌":
                            raise asyncio.TimeoutError
                        
                        update_info = await self.bot.wait_for('message', timeout=20.0, check=message_check)
                        
                        update_info = update_info.content

                        if type_change == "player_image":
                            current_player[type_change] = update_info
                        elif type_change == "clan":
                            current_player[type_change] = update_info
                        else:
                            if type_change == "cs_wins":
                                current_player["cs_wins"] += int(update_info)
                                current_player["cs_matches"] += int(update_info)
                                embed_dict["fields"][2]["value"] = current_player["cs_matches"]
                            else:
                                current_player["cs_matches"] += int(update_info)
                            
                            current_player["win_rate"] = float(current_player["cs_wins"]) / float(current_player["cs_matches"])
                            embed_dict['fields'][3]['value'] = str(current_player['win_rate'] * 100) + "%" #auto update
                        
                        if type_change == "player_image":
                            pass #not implimented
                        else:
                            embed_dict["fields"][i]["value"] = current_player[type_change]
                            self.write_json("player", current_player)
                        
                        await embed_message.edit(embed=discord.Embed.from_dict(embed_dict))

                except asyncio.TimeoutError:
                    player_embed.color = discord.Color.dark_grey()
                    player_embed.title += " (Inactive)"
                    await embed_message.edit(embed=player_embed)
            else:
                await ctx.send("That player doesn't exist!")
        else:
            embed_message = await ctx.send(embed=create_embed(current_player))




    
        
        

    
        
        

    
        
        

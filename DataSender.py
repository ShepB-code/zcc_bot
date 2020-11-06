#Cog to set info for clans & matches

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json
from clanClass import ClanClass

from help_functions import embed_footer

class DataSender(commands.Cog):
    prefix = "+"
    """Cog for the clan command"""
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.file_name = "data.json"
        prefix = self.bot.command_prefix

    def read_json(self):
        with open(self.file_name, 'r') as f:
            return json.load(f)
    def write_json(self, load_type, data):
        file_dict = dict()
        with open(self.file_name, 'r') as f:
            file_dict = json.load(f)
        if load_type == "clan":
            file_dict["clan"][data['clan_name']] = data
        elif load_type == "change_clan":
            file_dict["clan"] = data
        elif load_type == "player":
            file_dict["player"][data["player_name"]] = data
        

        with open("data.json", "w") as outfile: 
            json.dump(file_dict, outfile, indent=4)
    
    async def update_embed_message(self, ctx, embed_message, embed):
        if embed_message:
            await embed_message.edit(embed=embed)
            await embed_message.clear_reactions()
        else:
            embed_message = await ctx.send(embed=embed)
        return embed_message

    def is_admin(self, ctx, author):
        return ctx.guild.id == self.guild_id and author.guild_permissions.administrator 
    async def add_emoji_list(self, embed_message, emoji_list):
        for emoji in emoji_list:
            await embed_message.add_reaction(emoji)
        return emoji_list
    
    async def get_type_change(self, ctx, reaction, emoji_dict):
        msg = await ctx.send(emoji_dict[str(reaction)][0])
        type_change = emoji_dict[str(reaction)][1]
        index = emoji_dict[str(reaction)][2]
        return msg, type_change, index
    # This function was written very late at night, please do not judge
    @commands.command(
        help="`{prefix}clan` is used to view and edit clan information\nUsage: `{prefix}clan clan_name`"
    )
    async def clan(self, ctx, *args, passed_command=None, embed_message=None, current_player=None):
        message = ctx.message
        author = ctx.message.author
        channel = ctx.channel
        clan_name = args[0].lower()
        clan_data = self.read_json()["clan"]

        if clan_name in clan_data.keys():
            current_clan = clan_data[clan_name]

            def create_embed(current_clan):
                clan_embed = discord.Embed(
                    title=current_clan['clan_name'].capitalize() + " 📜",
                    description="Clan Information and Stats",
                    color=discord.Color.blue()
                    )

                clan_embed.add_field(name="Leader(s) 👑", value=current_clan['leaders'], inline=True)
                clan_embed.add_field(name="Creation Date ⏰", value=current_clan['creation_date'], inline=True)
                clan_embed.add_field(name="CS Wins 🏆", value=current_clan['cs_wins'], inline=False)
                clan_embed.add_field(name="Matches Played 🥊", value=current_clan['cs_matches'], inline=True)
                clan_embed.add_field(name="Winrate 📈", value=current_clan['win_rate'], inline=False)
                clan_embed.set_image(url=current_clan['clan_image'])
                clan_embed.set_footer(text=embed_footer(), icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
                
                return clan_embed
            
            clan_embed = create_embed(current_clan)

            embed_message = await self.update_embed_message(ctx, embed_message, clan_embed)
            
            if self.is_admin(ctx, author):
                
                embed_dict = clan_embed.to_dict()

                
                if clan_name in clan_data.keys():
                    #Add if/else for admin
                    emoji_dict = {
                        "📜": ["Please enters a new name: ", "clan_name", None],
                        "👑": ["Please enter a new leader(s): ", "leaders", 0],
                        "⏰": ["Please enter a new creation date: ", "creation_date", 1],
                        "📷": ["Please enter a new clan image URL: ", "clan_image", None],
                        "🏆": ["Please enter the amount of wins you want to add: ", "cs_wins", 2],
                        "🥊": ["Please enter a new match: ", "cs_matches", 3]
                    }
                    
                    emoji_list = await self.add_emoji_list(embed_message, list(emoji_dict.keys()) + ["❌"])
                    if passed_command:
                        emoji_list.append("⏪")
                        await embed_message.add_reaction("⏪")
                    
                    def reaction_check(reaction, user):
                        return user == message.author and str(reaction.emoji) in emoji_list
                    def message_check(message):
                        return message.author == author and message.channel == channel
                    try:
                        while True:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)
                            type_change = ""
                            
                            
                            if str(reaction) == "⏪" and passed_command:
                                return await passed_command.__call__(ctx, current_player["player_name"], embed_message=embed_message)
                            elif str(reaction) == "❌":
                                raise asyncio.TimeoutError

                            #call function
                        
                            
                            msg, type_change, i = await self.get_type_change(ctx, reaction, emoji_dict)
                            update_info_message = await self.bot.wait_for('message', timeout=20.0, check=message_check)
                            
                            update_info = update_info_message.content

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
                                embed_dict['fields'][4]['value'] = str(int(current_clan['win_rate'] * 100)) + "%" #auto update

                            
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
                            await msg.delete()
                            await update_info_message.delete()

                    except asyncio.TimeoutError:
                        clan_embed.color = discord.Color.dark_grey()
                        clan_embed.title += "(Inactive)"
                        await embed_message.edit(embed=clan_embed)
        else:
            await ctx.send("That clan doesn't exist!")

            #raise discord.ext.commands.MissingPermissions(missing_perms="Administrator") 
        
    # TODO Add discord ID To json, and auto update profile picture
    @commands.command(
        help="`{prefix}player` is used to view and edit clan information\nUsage: `{prefix}player player_name`"
    )
    async def player(self, ctx, *args, embed_message=None):
        message = ctx.message
        author = ctx.message.author
        channel = ctx.channel
        player_name = args[0].lower()
        player_data = self.read_json()["player"]

        if player_name in player_data.keys():
            current_player = player_data[player_name]
            
            def create_embed(current_player):
                player_embed = discord.Embed(
                    title=current_player["player_name"].capitalize(),
                    description="Player information and stats",
                    color=discord.Color.blue()
                )
                player_embed.add_field(name="Clan Affiliation", value=f'{current_player["clan"].capitalize()} react with 🔎 to view the clan', inline=True)
                player_embed.add_field(name="Wins", value=current_player["cs_wins"], inline=False)
                player_embed.add_field(name="Total Matches Played", value=current_player["cs_matches"], inline=True)
                player_embed.add_field(name="Win Rate", value=current_player["win_rate"], inline=False)
                player_embed.set_thumbnail(url=current_player["player_image"])
                player_embed.set_footer(text=embed_footer(), icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
                return player_embed
        
            
            player_embed = create_embed(current_player)
            embed_message = await self.update_embed_message(ctx, embed_message, player_embed)

            
            if self.is_admin(ctx, author):

                embed_dict = player_embed.to_dict()

            
                emoji_dict = {"📜": ["Please enter a new clan: ", "clan", 0],
                                "🏆": ["Please enter the amount of wins you want to add: ", "cs_wins", 1],
                                "🥊": ["Please enter a new match: ", "cs_matches", 2]
                            }
                emoji_list = await self.add_emoji_list(embed_message, list(emoji_dict.keys()) + ["🔎", "❌"])

                def reaction_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in emoji_list
                def message_check(message):
                        return message.author == author and message.channel == channel
                
                try:
                    while True:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=reaction_check)
                        
                        if str(reaction) == "🔎":
                            return await self.bot.get_command("clan").__call__(ctx, current_player["clan"], passed_command=self.bot.get_command("player"), embed_message=embed_message, current_player=current_player)
                        elif str(reaction) == "❌":
                            raise asyncio.TimeoutError
                        msg, type_change, i = await self.get_type_change(ctx, reaction, emoji_dict)
                        
                        update_info_message = await self.bot.wait_for('message', timeout=20.0, check=message_check)
                        
                        update_info = update_info_message.content

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
                            embed_dict['fields'][3]['value'] = str(int(current_player['win_rate'] * 100)) + "%" #auto update
                        
                        if type_change == "player_image":
                            pass #not implimented
                        else:
                            embed_dict["fields"][i]["value"] = current_player[type_change]
                            self.write_json("player", current_player)
                        
                        await embed_message.edit(embed=discord.Embed.from_dict(embed_dict))
                        await msg.delete()
                        await update_info_message.delete()

                except asyncio.TimeoutError:
                    player_embed.color = discord.Color.dark_grey()
                    player_embed.title += "(Inactive)"
                    await embed_message.edit(embed=player_embed)
        else:
            await ctx.send("That player doesn't exist!")
       
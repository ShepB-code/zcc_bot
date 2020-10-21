#Scrim Command for Instinct bots

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio
import json 

class MatchMaker(commands.Cog):
    """Cog for the Scrim command"""

    def __init__(self, bot):
        self.bot = bot
        self.file_name = "data.json"

    def is_admin(self, author):
        return author.guild_permissions.administrator 
    
    def read_json(self):
        with open(self.file_name, 'r') as f:
            return json.load(f)
    def write_json(self, guild_id, data):
        file_dict = dict()
        with open(self.file_name, 'r') as f:
            file_dict = json.load(f)
        file_dict["scrim_settings"][guild_id] = data
        with open("data.json", "w") as outfile: 
            json.dump(file_dict, outfile, indent=4)

    async def message_wait_for(self, ctx, timeout=20):
        def message_check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        user_message = await self.bot.wait_for("message", timeout=timeout, check=message_check)
        
        return user_message
    async def reaction_wait_for(self, ctx, emojis, msg, timeout=20):
        for emoji in emojis:
            await msg.add_reaction(emoji)
        def reaction_check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emojis
        reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout, check=reaction_check)
        return str(reaction), user
    
    async def get_message_from_emojis(self, ctx, reaction, emoji_dict):
        msg = await ctx.send(emoji_dict[reaction][0])
        type_change = emoji_dict[reaction][1]
        index = emoji_dict[reaction][2]
        return msg, type_change, index
    @commands.group()
    async def scrim(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcommand invoked. ")
    
    @scrim.command()
    async def settings(self, ctx):
        scrim_settings = self.read_json()["scrim_settings"] 
        author = ctx.message.author
        guild = ctx.guild
        guild_id = str(guild.id)

        def create_embed(current_settings, guild_name, guild_image):
            settings_embed = discord.Embed(
                title=guild_name.capitalize() + " 📜",
                description="Clan Information and Stats",
                color=discord.Color.blue()
                )
            
            roles = " ".join([guild.get_role(role_id).mention for role_id in current_settings['roles']])
            
            settings_embed.add_field(name="Roles 📜", value=roles, inline=True)
            settings_embed.add_field(name="Channel 📺", value=guild.get_channel(current_settings['channel']).mention, inline=True)
            settings_embed.set_thumbnail(url=guild_image)
            settings_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
            
            return settings_embed 
        settings_embed = None
        
        if guild_id in scrim_settings.keys():
            current_settings = scrim_settings[guild_id]
            settings_embed = create_embed(current_settings, guild.name, guild.icon_url)
        
            if self.is_admin(author):
                embed_message = await ctx.send(embed=settings_embed)
                embed_dict = settings_embed.to_dict()
                try:
                    while True:
                        reaction, user = await self.reaction_wait_for(ctx, ["📜", "📺", "❌"], embed_message)
                        emoji_dict = {
                            "📜": ["Please @ roles you would like to update", "roles", 0],
                            "📺": ["Please mention new channel", "channel", 1]
                        }


                        if reaction == "❌":
                            raise asyncio.TimeoutError                          
                        msg, type_change, index = await self.get_message_from_emojis(ctx, reaction, emoji_dict)
                        user_message = await self.message_wait_for(ctx)
                        if type_change == "roles":   
                            embed_dict["fields"][index]["value"] = " ".join([role.mention for role in user_message.role_mentions])
                            current_settings[type_change] = [role.id for role in user_message.role_mentions]
                        else:
                            embed_dict["fields"][index]["value"] = user_message.channel_mentions[0].mention
                            current_settings[type_change] = user_message.channel_mentions[0].id
                        
                        self.write_json(guild_id, current_settings)
                        await embed_message.edit(embed=discord.Embed.from_dict(embed_dict))

                        await msg.delete()
                        await user_message.delete()
                        
                except asyncio.TimeoutError:
                    settings_embed.color = discord.Color.dark_grey()
                    settings_embed.title += "(Inactive)"
                await embed_message.edit(embed=settings_embed)
                #Send embed with emojis
            elif set([role.id for role in author.roles]) & set(scrim_settings[guild_id]["roles"]):
                embed_message = await ctx.send(embed=settings_embed)
            else:
                #send no embed
                await ctx.send("You don't have permission to run this command.")
                #raise discord.ext.commands.MissingPermissions
                
        else:
            if self.is_admin(author):
                msg = await ctx.send("There are no saved settings. Would you like to create scrim settings? ")

                reaction, user = await self.reaction_wait_for(ctx, ["✅", "❌"], msg)

                if reaction == "❌":
                    return
                
                roles_list = list()
                while True:
                    msg = await ctx.send("Please @ the roles that you want to add. Default perm is admin.")

                    add_role = (await self.message_wait_for(ctx)).role_mentions
                    
                    roles_list += add_role
                    continue_message = await ctx.send("Would you like to add more roles?")
                    reaction, user = await self.reaction_wait_for(ctx, ["✅", "❌"], continue_message)

                    await continue_message.delete()
                    if reaction == "❌":
                        break
                    await msg.delete()

                msg = await ctx.send("Please enter the channel you want to send scrims to. #channel_name")
                channel_add = (await self.message_wait_for(ctx)).channel_mentions[0]
                
                confirmation_embed = discord.Embed(
                    title="Confirm Settings",
                    description="Please react to confirm or delete these settings",
                    color=discord.Color.blue()
                )
                confirmation_embed.add_field(name="Roles", value=" ".join([role.mention for role in roles_list]), inline=True)
                confirmation_embed.add_field(name="Channel", value=channel_add.mention, inline=True)

                msg = await ctx.send(embed=confirmation_embed)
                reaction, user = await self.reaction_wait_for(ctx, ["✅", "❌"], msg)

                if reaction == "❌":
                    return
                
                
                self.write_json(guild_id, {"guild_name": guild.name, "roles": [role.id for role in roles_list], "channel": channel_add.id})
            else:
                await ctx.send("You don't have permissions to create new settings.")
        #create settings
            
        
 
            
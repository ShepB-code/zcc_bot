#Scrim Command for Instinct bots

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get
import asyncio

class Scrim(commands.Cog):
    """Cog for the Scrim command"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def scrim(self, ctx, *args):
    
        channel = ctx.channel
        message = ctx.message
        author = ctx.message.author
        
        author_roles = [role.name for role in ctx.author.roles] # Gets all the roles that the author (person who called the command) has.

        

        if 'Test' in author_roles: # Trying to see if a certain role is in author_roles
            try:
                def msg_check(m):
                    return m.author == author and m.channel == channel
                        
                    # Bot waits for the author, that called the command, to enter a message
                

                # FIRST QUESTION

                    # This is the first question that the bot asks
                await ctx.send('Enter the type of scrim you are hosting (Which Game)') #Question

                scrim_type_msg =  # The bot waits for an answer to the question

                scrim_type = scrim_type_msg.content #Bot stores that information in a variable

                #SECOND QUESTION
                await ctx.send('Enter the opponent you will be playing:') #Question

                opponent_msg = await self.bot.wait_for('message', timeout=20.0, check=msg_check) #The bot waits for an answer to the question

                scrim_opponent = opponent_msg.content #Bot stores that information in a variable

                #THIRD QUESTION
                await ctx.send('Enter the time for the scrim:') #Question

                time_msg = await self.bot.wait_for('message', timeout=20.0, check=msg_check) #The bot waits for an answer to the question

                scrim_time = time_msg.content #Bot stores that information in a variable

                #FOURTH QUESTION

                american_region_emoji = '🌎'
                europe_region_emoji = '🌍'
                asia_region_emoji = '🌏'
                region_emoji_list = [american_region_emoji, europe_region_emoji, asia_region_emoji]

                region_msg = await ctx.send(f'Enter the region for the scrim: React with {american_region_emoji} for the US region, react with {europe_region_emoji} for the EU region, or react with {asia_region_emoji} for the ASIA region!') #Question

               
                
            
                for emoji in region_emoji_list:
                    await region_msg.add_reaction(emoji)
                
                def region_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in region_emoji_list
            
                region_reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=region_check) #The bot waits for an answer to the question

                #Bot stores that information in a variable
                if str(region_reaction) == american_region_emoji:
                    scrim_region = 'USA'
                elif str(region_reaction) == europe_region_emoji: 
                    scrim_region = 'EU'
                elif str(region_reaction) == asia_region_emoji:
                    scrim_region = 'ASIA'

         
                
                #FIFTH QUESTION
                react_msg = await ctx.send('React with the number of rounds you are going to play') #Question (Stored in a variable so you can add reactions to it)

                round_reaction_dict = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6} #Dictionary for each of the emojis with the key as the emoji and the value as the number (Makes it easier later on)
                
                for key in round_reaction_dict: #Cycling through the dictionary keys (Emojis)
                    await react_msg.add_reaction(key) #Adding the keys (emojis) to the message above (react_message)
                
            
                def round_react_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in round_reaction_dict.keys() #This function checks for a reaction add on a message, and returns the user that reacted and the reaction made (ONLY RETURNS THE USER IF THE USER MATCHES THE AUTHOR!)


                round_reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=round_react_check) #Bot waits for the reaction add

                
                for key in round_reaction_dict.keys(): #Once again cycling through the keys of the reaction dict
                    if str(round_reaction) == key: #Trying to find a match for the reaction that was added
                        number_of_rounds = round_reaction_dict[key] #Once the match is found, the value of that key is stored in a variable to be added to the embed

                    else: #this should never happen, but why not
                        pass
                
                #SIXTH QUESTION
                main_team_emoji = '👑'
                sub_team_emoji = '🧢'
                team_emoji_list = [main_team_emoji, sub_team_emoji] #Storing the emojis in a list for the check function

                team_msg = await ctx.send(f'React with the team you want to use: {main_team_emoji} for main team, and {sub_team_emoji} for sub team!') #Once again storing this message as a variable to add reactions

                for emoji in team_emoji_list: #Cycling through team_emoji_list
                    await team_msg.add_reaction(emoji) #Adding the values as reactions to team_msg

                def team_reaction_check(reaction, user): #Very similiar to the previous check function, but this one checks for emojis in the list, not the dict.
                    return user == message.author and str(reaction.emoji) in team_emoji_list

                team_reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=team_reaction_check) #Waiting for the reaction_add

                if str(team_reaction) == main_team_emoji: #Checking to see if the reaction added to team_msg is equal to main_team_emoji
                    scrim_team = 'Mainteam' #If it is, it writes the scrim_team variable
                
                elif str(team_reaction) == sub_team_emoji: #Checking to see if the reaction added to team_msg is equal to sub_Team_emoji
                    scrim_team = 'Subteam' #If it is, it writes the scrim_team variable
                

                #EMBED
                #Basically just compiling all the data we gathered and adding it into one giant box :)
                scrim_embed = discord.Embed(
                    title='SCRIM',
                    description=f'{scrim_type} Scrim',
                    color=discord.Colour.blurple()
                )
                scrim_embed.add_field(name='REGION', value=scrim_region, inline=False)
                scrim_embed.add_field(name='TIME', value=scrim_time, inline=False)
                scrim_embed.add_field(name='OPPONENT', value=scrim_opponent, inline=False)
                scrim_embed.add_field(name='NUMBER OF ROUNDS', value=number_of_rounds, inline=False)
                scrim_embed.add_field(name='TEAM', value=scrim_team, inline=False)
                scrim_embed.set_footer(text='Confirm the scrim details by reacting below!')

                cancel_confirm_msg = await ctx.send(embed=scrim_embed) #Sending the embed, but attaching it to a variable so that we can add reactions.

               

                cancel_reaction = '❌' 
                confirm_reaction = '✔'

                cancel_confirm_reactions = [cancel_reaction, confirm_reaction] #Putting it in a list for the check function

                for reaction in cancel_confirm_reactions: #Cycling through the list
                    await cancel_confirm_msg.add_reaction(reaction) #Adding the emojis in the list to the cancel_confirm_msg

                def cancel_confirm_check(reaction, user): #Similiar to the previous check function
                    return user == message.author and str(reaction.emoji) in cancel_confirm_reactions

                cancel_confirm_reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=cancel_confirm_check) #Waiting for a reaction to be added on cancel_confirm_msg


                if str(cancel_confirm_reaction) == cancel_reaction: #If the added reaction == the cancel emoji
                    await ctx.send("Scrim has been deleted!") #CANCEL THE SCRIM! (basically just scraps all the data)
                    
                elif str(cancel_confirm_reaction) == confirm_reaction: #If the added reaction == the confirm emoji
                    await ctx.send("Scrim is being posted!") #Post the scrim!
                    for channel in ctx.guild.text_channels:
                        if channel.name == 'testing': #Finding the right channel to post the embed to
                            await channel.send(embed=scrim_embed)  #Posting the scrim!

                            for role in ctx.guild.roles: #Indexing through the server roles
                                if scrim_region == 'USA' and role.name == 'USA':
                                    await channel.send(role.mention)
                                elif scrim_region == 'EU' and role.name =='EU':
                                    await channel.send(role.mention)
                                elif scrim_region == 'ASIA' and role.name == 'ASIA':
                                    await channel.send(role.mention)
                           
            except: #If one of the bot.wait_for's times out, the data is scrapped
                await ctx.send("Timed out, please call the command again.")

        else: #If they don't have the right role to use the command
            await ctx.send("You don't have the right perms to call this command.")
            


        #await ctx.send(f'EMOJI: {reaction_two}, FROM USER: {user_two}')

        

            
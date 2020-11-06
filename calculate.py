#Calculate Cog for the ZCC Events Bot

import discord
import itertools
from discord.ext import commands
import discord.utils
from discord.utils import get

from settings import Settings

class Calculate(commands.Cog):
    """Cog for the Calculate command"""

    def __init__(self, bot):
        self.bot = bot
        self.help_embed = discord.Embed(
            title='Calc Help',
            color=discord.Color.blue()
        )
        self.data = dict()
        self.prefix =  self.bot.command_prefix

        
    def total(self, kills, place):
        settings = self.bot.get_cog('Settings').get_settings()
        kill_value = settings['KillSetting']

        if place in settings.keys():
            place_value = settings[place]
        else:
            place_value = 0
        
        equation = f'(({kills} * {kill_value}) + {place_value})'

        return f"{equation} = **{eval(equation)}**", eval(equation)
    
    def get_sorted_leaderboard(self):
        return sorted(self.data.items(), key=lambda x: x[1], reverse=True)

    @commands.command(
        name="Calc",
        help=
        """
        This command is used to calculate scores for players,\
        given the kills they got and their in-game placing.
        Usage: `{prefix}c(alc) (Kills) (Placing)`\
        or `{prefix}c(alc) (MatchNum) (Kills) (Placing) (MatchNum) (Kills) (Placing)`\
        """,
        aliases=['c', 'calc']
    )
    @commands.has_guild_permissions(administrator=True)
    async def calc(self, ctx, *args):
        show_equation = "((kill_amount * points_per_kill) + points_for_place)"
        bot_id = 757700872791654500
        total_score = 0

        try:
            
            if len(args) > 2:
                name = args[0]

                i = 1
                temp_value_list = list()
                value_list = list()

                #Organizing all the args into separate lists
                
                while True:
                    temp_value_list.append(args[i])
                    i += 1
                    if (i - 1) % 3 == 0:
                        value_list.append(temp_value_list)
                        temp_value_list = list()

                    if i == len(args):
                        break
                
                calc_embed = discord.Embed(
                    title="Calculation",
                    description=show_equation,
                    color=discord.Color.blue()
                )
                
                for item in value_list:
                    total_tuple = self.total(int(item[1]), int(item[2]))
                    total_score += total_tuple[1]
                    calc_embed.add_field(name=item[0], value=total_tuple[0], inline=False)
            
                calc_embed.add_field(name="Total Score", value=f'**{total_score}**')
                
                self.data[name] = total_score
            else:
                kill_input = int(args[0])
                place_input = int(args[1])

                calc_embed = discord.Embed(
                    title="Calculation",
                    description=show_equation,
                    color=discord.Color.blue()
                )
                calc_embed.add_field(name='Total', value=self.total(kill_input, place_input))
            
            #Adding final imformation to the embed, then sending it
            calc_embed.set_footer(text='Made by Shep and Peter', icon_url=self.bot.get_user(self.bot.user.id).avatar_url)
            await ctx.send(embed=calc_embed)
            

        except ValueError:
            await ctx.send("When calling `?calculate`, you must give it at least two parameters: kills and place. A valid call to this command would be `?calculate 10 1`. ")   
        except KeyError:
            await ctx.send("It appears that you don't have any settings. Please use `?settings update` to create settings. ")
        

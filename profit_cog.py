import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import ships


class Profit:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def profit(self, value1, value2):
        embed = discord.Embed(
            title='Market Information',
            description='O.D.I.N. Merchant Module',
            color=discord.Color.dark_green()
        )

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ODIN-bd3fd42186ba.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Items').get_worksheet(2)

        #  QT generators and their speed in m/s
        qtgen = {
            'goliath': 39337480,
            'drift': 42000700,
            'expedition': 43704980,
            'rush': 44123050,
            'beacon': 45958490,
            'eos': 46681120,
            'bolon': 70759160,
            'odyssey': 73686030,
            'crossfield': 84187440,
            'kama': 99314530,
            'pontes': 133904700
        }

        starts = {
            'CruS': 'Crusader_start'
        }

        destinations = {
            'Hur': 'Hurston'
        }

        names = {
            'CruS': 'Crusader',
            'Hur': 'Hurston'
        }

        def travel_time():
            destination = wks.find(destinations.get(value1))
            starting_point = wks.find(starts.get(value2))
            dest_column_gen = list(map(int, re.sub("[^0-9]", " ", str(destination)).split()))
            start_row_gen = list(map(int, re.sub("[^0-9]", " ", str(starting_point)).split()))
            distance_value_gen = int(wks.cell(start_row_gen[0], dest_column_gen[1]).value)
            dist_calc = float(((int(distance_value_gen) * 1000)/ int(qtgen.get('pontes')))/60)
            return '{0:.2f}'.format(dist_calc)

        embed.set_footer(text='Orical Dynamic Information Network')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
        embed.add_field(name='Route Data', value='{} to {}'.format(names.get(value2),names.get(value1)), inline=False)
        embed.add_field(name='Ship Data', value='{} carrying {}'.format(ships.cat.name, 'Aluminum'), inline=False)
        embed.add_field(name='Travel Data',
                        value='{} minute Atmo > Space\n{} minutes in Quantum Travel\n{} minutes Space > Atmo'
                        .format(5, travel_time(), 5)
                        , inline=False)
        embed.add_field(name='ETA', value='13.97 minutes', inline=False)
        embed.add_field(name='Profit Data',
                        value='100 SCU of Aluminum\nGross: 125 aUEC\nNet: 7 aUEC\nProfit/Minute: 0.50/minute',
                        inline=False)

        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Profit(client))

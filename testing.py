import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import names
import pymssql


class Test:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, value1, value2):
        embed = discord.Embed(
            title='Market Information',
            description='O.D.I.N. Merchant Module',
            color=discord.Color.dark_green()
        )

        # connection string to SQL server
        conn = pymssql.connect(server='68.0.187.171', user='odin', password='odin', database='ODIN')
        cursor = conn.cursor()
        cursor2 = conn.cursor()

        #  Access to worksheet information
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ODIN-bd3fd42186ba.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Items').get_worksheet(0)

        #  Logic for pulling information from the spreadsheet and populating an embed
        def selling():
            #  if 'all' is called loops through all items and pushes out everything with no value from requested station
            if value2 == 'all':
                sell_station_gen = wks.find(names.facilities.get(value1).lower())
                sell_column_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_station_gen)).split()))
                col_loc = sell_column_gen[1] + 1
                col_data = wks.col_values(col_loc)

                #  Iterate loop logic (need to come up with a way to automate i so its not hard coded)
                def looper():
                    i = 6
                    while i < 30:
                        if col_data[i] == '0':
                            i += 1
                        else:
                            embed.add_field(name=wks.cell(i + 1, 1).value,
                                            value='Sells for {} aUEC'.format(col_data[i]), inline=True)
                            i += 1
                return looper()
            #  returns an individual items price or inability to sell from requested station
            else:
                sell_station_gen = wks.find(names.facilities.get(value1))
                sell_item_gen = wks.find(names.items.get(value2))
                sell_column_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_station_gen)).split()))
                sell_row_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_item_gen)).split()))
                sell_value_gen = wks.cell(sell_row_gen[0], sell_column_gen[1] + 1).value
                if sell_value_gen == '0':
                    return embed.add_field(name=names.items.get(value2),
                                           value='Unavailable at this location', inline=False)
                else:
                    return embed.add_field(name=names.items.get(value2),
                                           value='Sells for {} aUEC'.format(sell_value_gen), inline=False)

        #  Information to be placed in embeds no matter what is called by the user
        embed.set_footer(text='Orical Dynamic Information Network')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
        embed.add_field(name='{} Offload'.format(names.facilities.get(value1)),
                        value='====================', inline=False)
        selling()

        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Test(client))
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import names


class Sell:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def sell(self, value1, value2):
        embed = discord.Embed(
            title='Market Information',
            description='O.D.I.N. Merchant Module',
            color=discord.Color.dark_green()
        )

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ODIN-bd3fd42186ba.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Items').get_worksheet(0)

        def selling():
            sell_station_gen = wks.find(names.facilities.get(value1))
            sell_item_gen = wks.find(names.items.get(value2))
            sell_column_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_station_gen)).split()))
            sell_row_gen = list(map(int, re.sub("[^0-9]", " ", str(sell_item_gen)).split()))
            sell_value_gen = wks.cell(sell_row_gen[0], sell_column_gen[1] + 1).value
            if sell_value_gen == '0':
                return 'Cannot be sold here'
            else:
                return 'Sells for {} aUEC'.format(sell_value_gen)

        embed.set_footer(text='Orical Dynamic Information Network')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
        embed.add_field(name=names.facilities.get(value1), value='====================', inline=False)
        embed.add_field(name=names.items.get(value2), value=selling(), inline=False)

        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Sell(client))

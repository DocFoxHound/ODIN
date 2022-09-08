import discord
from discord.ext import commands
import names
import pymssql


class Test:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def sql(self, station, item):
        """
        User specified input for processing dB queries
        :param station: The station or facility the user would like information about
        :param item: the specific item or a query of all items from station in the first param
        :return: inputs are used as keys for dicts (names, items) and as SELECT params for dB query
        :rtype: str
        """
        embed = discord.Embed(
            title='Market Information',
            description='O.D.I.N. Merchant Module',
            color=discord.Color.dark_green()
        )

        # connection string to SQL server
        conn = pymssql.connect(server='68.0.187.171', user='odin', password='odin', database='ODIN', port='49172')
        cursor = conn.cursor()

        def selling():
            """
            Pulls information from the ODIN database using results from the params station and item.
            :return: Populates an embed with results from a dB query
            :rtype: str, int
            """

            if item == 'all':
                def looper():
                    cursor.execute("SELECT station, item, sellPrice FROM market WHERE station=%s and sellPrice >0",
                                   names.facilities.get(station).lower().replace(" ", ""))
                    for data in cursor.fetchall():
                        embed.add_field(name='{}'.format(data[1]),
                                        value='{} aUEC'.format(data[2]), inline=True)
                return looper()
            else:
                cursor.execute("SELECT station, item, sellPrice FROM market WHERE station=%s and item=%s",
                               (names.facilities.get(station).lower().replace(" ", ""), names.items.get(item)))
                sell_value_gen = cursor.fetchall()
                if sell_value_gen[0][2] == 0:
                    return embed.add_field(name=names.items.get(item),
                                           value='Unavailable at this location', inline=False)
                else:
                    return embed.add_field(name=names.items.get(item),
                                           value='Sells for {} aUEC'.format(sell_value_gen[0][2]), inline=False)

        #  Standard information to be placed in embeds
        embed.set_footer(text='Orical Dynamic Information Network')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
        embed.add_field(name='{} Offload'.format(names.facilities.get(station)),
                        value='=' * 20, inline=False)
        selling()

        conn.close()
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Test(client))

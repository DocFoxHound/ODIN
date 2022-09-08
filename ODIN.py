import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from discord.ext import commands
import discord

TOKEN = 'NTM0NjAyMzA4NzkzNzk0NTcw.Dx7_Kw.2Oymduw5gpAm3sd3FobIt3G3pTA'

client = commands.Bot(command_prefix='?')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('ODIN-bd3fd42186ba.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Items').get_worksheet(0)

# !! Cogs go in extensions list !! =====================================================================================

extensions = ['sell_cog', 'buy_cog', 'profit_cog', 'testing', 'sqltesting', 'buyat_cog']

# !! Cogs go in extensions list !! =====================================================================================

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='?odin'))
    print('O.D.I.N. Online...')



@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='O.D.I.N.')
    await client.add_roles(member, role)

@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def odin():
    embed = discord.Embed(
        title='Help Command',
        description='O.D.I.N. Merchant Shard',
        color=discord.Color.dark_red()
    )


    embed.set_footer(text='Orical Dynamic Information Network')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
    embed.add_field(name='ODIN', value='ODIN', inline=False)

    await client.say(embed=embed)

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    client.run(TOKEN)

#keep from closing
input()
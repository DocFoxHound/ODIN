import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import names
import pymssql
from functions import shipInfoFunc
from functions import travelTimeFunc
#trying my hand at making a COG do something. Here is what is needed for the COG to output all items buyable, and where to sell them at...
#1 get buying location
#2 get money to spend
#3 get ship cargo space

#4 get all items at location
#4.5 get amount purchasable of items at location (todo)
#5 get all buy prices of items at all locations
#6 get all locations each item sells
#6.5 get amount sellable of items at location (todo)
#7 get all sell prices at locations each item sells

#8 travel time between origin and every sell location
#9 profit margin at every sell location
#10 profit margin / time spent travelling
#in all honesty, I tried to stick to this order, but it fell out after like number 5

#11 show list of all possible routes
class Buyat:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def buyat(self, def_station, def_ship, def_money):
        embed = discord.Embed(title='Market Information', description='O.D.I.N. Merchant Module', color=discord.Color.dark_green())
        embed.set_footer(text='Orical Dynamic Information Network')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/533520537415188480/c21d351059ea7c841fd634fa5081e4f1.png?size=128')
        embed.add_field(name='Top Ten Commodities to Sell', value='====================', inline=False)

        class originItems(object): #this is the list of items at the user-defined station (in this case, Levski)
            def __init__(self, name, buyPrice):
                self.name = name
                self.buyPrice = buyPrice
        class Item(object): #this is a list of objects to be filled by items sellable elsewhere in the universe
            def __init__(self, name, sellPrice, system, planet, station, travelDistance, travelTime, profit, uecmin):
                self.name = name
                self.sellPrice = sellPrice
                self.system = system
                self.planet = planet
                self.station = station
                self.travelDistance = travelDistance
                self.travelTime = travelTime
                self.profit = profit
                self.uecmin = uecmin
        try:
            
            #transform the user-input "def_station" into a "station" our code will understand
            station = def_station.lower()
            ship = def_ship.lower()
            money = int(def_money)
            
            #connection string to SQL server
            conn = pymssql.connect(server='68.0.187.171', user='odin', password='odin', database='ODIN', port='49172')  
            cursor = conn.cursor()
            
            #3 get ship cargo space. I really should place this later in the program as it doesn't make much sense here. But just remember we'll use it again.
            playerCargoSpace = shipInfoFunc(ship).cargo
            
            #4 get all buyable items at location. 
            cursor.execute('SELECT item FROM Market WHERE station=%s AND buyPrice>0', station)
            buyableItemNameList = cursor.fetchall() #you have to end a cursor command before you can start a new one.
            cursor.execute('SELECT buyPrice FROM Market WHERE station=%s AND buyPrice>0', station)
            buyableItemPriceList = cursor.fetchall() #doesn't matter if its a whole new cursor or not
            buyableItemList = []
            i=0
            while i < len(buyableItemNameList): 
                buyableItemList.append(originItems(buyableItemNameList[i], buyableItemPriceList[i])) #buyableItemList stores the items at our location, and can be accessed as such: buyableItemList[i].name or .buyPrice
                i += 1
            i=0
            
            #5 get all buy prices of items at all locations
            #declaring all the empty lists I will use
            sellItemNameList = []
            sellItemSystemList = []
            sellItemPlanetList = []
            sellItemStationList = []
            sellItemPriceList = []
            sellItemList = []
            i = 0
            while i < len(buyableItemList): #get the commodity name of every selling opportunity elsewhere in the verse (basically if it sells somewhere else, grab the name of the commodity (Agricultural Supplies for example))
                cursor.execute('SELECT item FROM Market WHERE item=%s AND sellPrice>0', *buyableItemList[i].name)
                sellItemNameList = sellItemNameList + cursor.fetchall()
                i += 1
            i = 0
            while i < len(buyableItemList): #get the price at which every commodity sells elsewhere
                cursor.execute('SELECT sellPrice FROM Market WHERE item=%s AND sellPrice>0', *buyableItemList[i].name)
                sellItemPriceList = sellItemPriceList + cursor.fetchall()
                i += 1
            i=0
            while i < len(buyableItemList): #get the system every selling opportunity is in
                cursor.execute('SELECT system FROM Market WHERE item=%s AND sellPrice>0', *buyableItemList[i].name)
                sellItemSystemList = sellItemSystemList + cursor.fetchall()
                i += 1
            i = 0
            while i < len(buyableItemList): #get the planet every selling opportunity is in
                cursor.execute('SELECT planet FROM Market WHERE item=%s AND sellPrice>0', *buyableItemList[i].name)
                sellItemPlanetList = sellItemPlanetList + cursor.fetchall()
                i += 1
            i = 0
            while i < len(buyableItemList): #get the station every item elsewhere belongs in
                cursor.execute('SELECT station FROM Market WHERE item=%s AND sellPrice>0', *buyableItemList[i].name)
                sellItemStationList = sellItemStationList + cursor.fetchall()
                i += 1
            
            #make an object list of all the items sellable throughout the universe that are purchasable at origin (Levski as a test). THIS IS A VERY IMPORTANT LIST
            i = 0
            while i < len(sellItemNameList):
                sellItemList.append(Item(*sellItemNameList[i], *sellItemPriceList[i],  *sellItemSystemList[i], *sellItemPlanetList[i], *sellItemStationList[i], 0, 0, 0, 0)) #the last four will be defined as we go, but for now they are all 0's
                i += 1
            
            #time to travel to the sell point
            i = 0 
            while i < len(sellItemList): #iterate through all the sellItemList objects
                sellItemList[i].travelTime = travelTimeFunc(station, sellItemList[i].station, ship)
                i += 1
                
            #before we can complete the uec/minute, we need to find out how much a player can first profit.
            #first we find out how much a player will spend filling up his ship
            i = 0
            while i<len(sellItemList):
                cursor.execute(('SELECT buyPrice FROM Market WHERE station=%s AND item=%s'), (station, sellItemList[i].name))
                variableprice = float(*cursor.fetchone())
                cursor.execute(('SELECT maxbuyamount FROM Market WHERE station=%s AND item=%s'),(station, sellItemList[i].name))
                variablemaxbuyable = int(*cursor.fetchone())
                cursor.execute(('SELECT unitperscu FROM Market WHERE station=%s AND item=%s'),(station, sellItemList[i].name))
                variableunitperscu = int(*cursor.fetchone())

                maxScuBuyable = variablemaxbuyable/variableunitperscu #it originally comes in units, so I have to convert it to SCU's
                buypriceperscu = variableprice * variableunitperscu #presently in game there 100 units of commodities per scu. Later we can swap this out with a call to the database where we'd keep the amount/SCU
                remainingMoneyToSpend = money #this will count down
                totalScuToBuy = 0 #and this will count up
                while remainingMoneyToSpend > buypriceperscu and totalScuToBuy <= playerCargoSpace and totalScuToBuy <= maxScuBuyable: #as long as we have money to spend and space to fit...
                    totalScuToBuy = totalScuToBuy + 1
                    remainingMoneyToSpend = remainingMoneyToSpend - buypriceperscu
                
                #How much did it take us to buy all that? This much
                maxBuyTotalUEC = totalScuToBuy*buypriceperscu

                #then we find out how much the sale will get us
                sellpriceperscu = sellItemList[i].sellPrice * 100 #presently in game there 100 units of commodities per scu
                maxSellTotalUEC = totalScuToBuy*sellpriceperscu

                #now we get the difference for the profit
                profit = maxSellTotalUEC - maxBuyTotalUEC #??? profit

                #now lets put that to the item in the list
                sellItemList[i].profit = profit

                #now we get to do the juicy uec/min calculation...
                #drum roll please
                #heeeeere we goooooo~
                uecminute = int(sellItemList[i].profit) / int(sellItemList[i].travelTime)
                #...that was it?
                sellItemList[i].uecmin = uecminute
                i += 1

            #now lets sort it to only show the highest in each item
            sellItemList = sorted(sellItemList, key=lambda Item: Item.uecmin, reverse=True)
            
            #and this spits out the top ten to the terminal
            i=0
            x=0
            if len(sellItemList) < 10:
                x = len(sellItemList)
            else:
                x = 10
            while i<x:
                ename = sellItemList[i].name
                estation = sellItemList[i].station
                eprofit = str("{0:.2f}".format(sellItemList[i].profit))
                euecmin = str("{0:.2f}".format(sellItemList[i].uecmin))
                embed.add_field(name=ename, value=estation, inline=True)
                embed.add_field(name="UEC/min: " + euecmin, value="Total Profit: **" + eprofit + "**", inline=True)
                #print(sellItemList[i].name, "|| SELL AT:", sellItemList[i].station, "|| PROFIT:", "{0:.2f}".format(sellItemList[i].profit), "|| UEC/MIN:", "{0:.2f}".format(sellItemList[i].uecmin))
                i += 1

            
            await self.client.say(embed=embed)

            #always remember to close connections
            conn.close()
        except Exception as e:
            print(e)
def setup(client):
    client.add_cog(Buyat(client))
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import names
import pymssql

#to retrieve the travel times
def travelTimeFunc (start, end, userShip): #where start is a station, and end is a station
    #1 get start system (planet doesn't matter as you can QT from anywhere within a system to the landing point in another system)
    #2 get the end station
    #3 get the end planet
    #4 get the end system
    #5 add time to get from commodity terminal to ship to spool to QT jump start...
    #6 get distance from start system to end system
    #7 check if additional jumps are needed to planet (not HUR or CRU R&R stations) 
    #8 add time to exit QT, cooldown, spool, and enter QT for travel to planet
    #9 get distance from arrival location to planet
    #10 check if additional jumps are needed to station (not Port Olisar, or R&R stations)
    #11 add time to exit QT, cooldown, spool, and enter QT for travel to station
    #12 add time to spline around planet
    #13 get distance from station that QD dumps player out (for example, 60km for Yela)
    #14 get ship afterburner speed * 0.75 (for speed up & slow down)
    #15 do math to figure out how long it takes to slowboat the scmDistance(s)
    #16 get ship QD speed
    #17 get the time it will take to cover all the QT distances
    try:
        #connection string to SQL server
        conn = pymssql.connect(server='68.0.187.171', user='odin', password='odin', database='ODIN', port='49172')  
        cursor = conn.cursor()
        finalTime = int(0)

        #1 get the starting station / check if it is spelled correctly
        try:
            cursor.execute('SELECT system FROM Market WHERE station=%s', start)
            startSystem = cursor.fetchone()
        except Exception as e:
            print(e)
            
        #4 get the ending system / check if it is spelled correctly
        try:
            cursor.execute('SELECT system FROM Market WHERE station=%s', end) 
            endSystem = cursor.fetchone()
        except Exception as e:
            print(e)

        #2 get the ending station
        cursor.execute('SELECT station FROM Market WHERE station=%s', end) 
        endStation = cursor.fetchone()
        
        #3 get the ending planet
        cursor.execute('SELECT planet FROM Market WHERE station=%s', end) 
        endPlanet = cursor.fetchone()
        
        #5 add time to get from commodity terminal to ship to spool to QT jump start
        finalTime = finalTime + 140 #measurements have 140 seconds being the amount of time it usually takes to get the ship up off the pad, spooled, and into QT
        
        #6 get distance from start system to end system
        cursor.execute(('SELECT distance FROM StantonDistance WHERE starting=%s AND ending=%s'), (startSystem, endSystem))
        distancevariable = int(*cursor.fetchone())
        
        scmDistance = 0
        #7 check if additional jumps are needed to planet (not HUR or CUR R&R stations) 
        if "cur l1" in endPlanet or "cur l1" in endPlanet or "cur l2" in endPlanet or "cur l3" in endPlanet or "cur l4" in endPlanet or "cur l5" in endPlanet or "hur l1" in endPlanet or "hur l2" in endPlanet or "hur l3" in endPlanet or "hur l4" in endPlanet or "hur l5" in endPlanet:
            scmDistance = 26000
            shipAft = shipInfoFunc(userShip).aftSpeed
            finalTime = finalTime + ((scmDistance/shipAft) * 1.5) #add extra time for speed up, speed down, and land
         
        else: #only continues if the endplanet is not a R&R station
            #8 add time to exit QT, cooldown, spool, and enter QT for travel AT SYSTEM AIMED AT PLANET
            
            finalTime = finalTime + 45
            
            #9 get distance from arrival location to planet
            if "crusader" in endSystem:
                cursor.execute("SELECT distance FROM CrusaderDistance WHERE ending=%s", endPlanet)
                distancevariable = distancevariable + int(*cursor.fetchone())
            elif "hurston" in endSystem:
                cursor.execute("SELECT distance FROM HurstonDistance WHERE ending=%s", endPlanet)
                distancevariable = distancevariable + int(*cursor.fetchone())
            elif "delamar" in endSystem:
                cursor.execute("SELECT distance FROM DelamarDistance WHERE ending=%s", endPlanet)
                distancevariable = distancevariable + int(*cursor.fetchone())
            
            #10 check if additional jumps are needed to station (not Port Olisar, or R&R stations)
            if "portolisar" in endPlanet:
                scmDistance = 8000
            else: #only continues if the end planet is not olisar
                #11 add time to exit QT, cooldown, spool, and enter QT for travel to station
                finalTime = finalTime + 45
                #12 add time to spline around planet
                finalTime = finalTime + 20

                #13 get distance from station that QD dumps player out (for example, 60km for Yela)
                if "yela" in endPlanet:
                    if "grimhex" in endStation:
                        scmDistance = 18000
                    elif "jumptown" in endStation:
                        scmDistance = 532000
                    else:
                        scmDistance = 60000
                elif "daymar" in endPlanet:
                    scmDistance = 60000
                elif "cellin" in endPlanet:
                    scmDistance = 60000
                elif "hurston" in endPlanet:
                    scmDistance = 125000
                elif "aberdeen" in endPlanet:
                    scmDistance = 60000
                elif "arial" in endPlanet:
                    scmDistance = 60000
                elif "magda" in endPlanet:
                    scmDistance = 60000
                elif "ita" in endPlanet:
                    scmDistance = 60000

        #14 get ship afterburner speed
        shipAft = shipInfoFunc(userShip).aftSpeed

        #15 do math to figure out how long it takes to slowboat the scmDistance(s)
        finalTime = finalTime + ((scmDistance/shipAft) * 1.75) #times 1.75 to account for speed up, slow down, and land times
      
        #16 get ship QD speed
        shipQDSpeed = shipInfoFunc(userShip).qtspeed

        #17 get the time it will take to cover all the QT distances
        finalTime = finalTime + ((int(distancevariable) * 1000)/shipQDSpeed) #distance variable is in km, shipQDSpeed is in m

        #make it in minutes
        finalTime = (finalTime/60)

        return finalTime
    except Exception as e:
        print(e)
#retrieve ship info as an object
def shipInfoFunc (userShip):
    class ship(object):
        def __init__(self, name, minCrew, maxCrew, cargo, scmSpeed, aftSpeed, drive, drivesize, qtspeed):
            self.name = name
            self.minCrew = minCrew
            self.maxCrew = maxCrew
            self.cargo = cargo
            self.scmSpeed = scmSpeed
            self.aftSpeed = aftSpeed
            self.drive = drive
            self.drivesize = drivesize
            self.qtspeed = qtspeed
    
    userShip = userShip.lower()

    conn = pymssql.connect(server='68.0.187.171', user='odin', password='odin', database='ODIN', port='49172')   
    cursor = conn.cursor()

    #get ship name
    var_name = userShip

    #get ship's minCrew
    cursor.execute('SELECT minCrew FROM ships WHERE shipName=%s', userShip)
    var_minCrew = int(*cursor.fetchone())

    #get ship's maxCrew
    cursor.execute('SELECT maxCrew FROM ships WHERE shipName=%s', userShip)
    var_maxCrew = int(*cursor.fetchone())

    #get ship's cargo space
    cursor.execute('SELECT cargo FROM ships WHERE shipName=%s', userShip)
    var_cargo = int(*cursor.fetchone())

    #get ship's scmSpeed
    cursor.execute('SELECT scmSpeed FROM ships WHERE shipName=%s', userShip)
    var_scmSpeed = int(*cursor.fetchone())

    #get ship's aftSpeed
    cursor.execute('SELECT aftSpeed FROM ships WHERE shipName=%s', userShip)
    var_aftSpeed = int(*cursor.fetchone())

    #get ship's drive
    cursor.execute('SELECT drive FROM ships WHERE shipName=%s', userShip)
    var_drive = cursor.fetchone()

    #get ship's drivesize
    cursor.execute('SELECT drivesize FROM ships WHERE shipName=%s', userShip)
    var_drivesize = int(*cursor.fetchone())

    #get ship's qtspeed
    cursor.execute('SELECT qtspeed FROM ships WHERE shipName=%s', userShip)
    var_qtspeed = int(*cursor.fetchone())

    newShip = ship(var_name, var_minCrew, var_maxCrew, var_cargo, var_scmSpeed, var_aftSpeed, var_drive, var_drivesize, var_qtspeed)

    return newShip
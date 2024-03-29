class Ships:
    def __init__(self, name, min_crew, max_crew, cargo, scm_speed, aft_speed):
        self.name = name
        self.min_crew = min_crew
        self.max_crew = max_crew
        self.cargo = cargo
        self.scm_speed = scm_speed
        self.aft_speed = aft_speed


hornet7c = Ships('FC7 Hornet', 1, 1, 2, 235, 1225)
mercury = Ships('Mercury Star Runner', 2, 3, 96, 215, 1050)
hulle = Ships('Hull E', 4, 5, 98304, 0, 0)
hulld = Ships('Hull D', 3, 5, 20736, 0, 0)
hullc = Ships('Hull C', 2, 4, 4608, 0, 0)
hullb = Ships('Hull B', 1, 1, 384, 0, 0)
hulla = Ships('Hull A', 1, 1, 48, 0, 0)
auroracl = Ships('Aurora CL', 1, 1, 6, 185, 1095)
auroraes = Ships('Aurora ES', 1, 1, 0, 190, 1140)
auroralx = Ships('Aurora LX', 1, 1, 0, 190, 1200)
auroramr = Ships('Aurora MR', 1, 1, 0, 195, 1210)
auroraln = Ships('Aurora LN', 1, 1, 0, 185, 1210)
aquila = Ships('Constellation Aquila', 3, 4, 96, 190, 985)
alpha = Ships('Mustang Alpha', 1, 1, 6, 255, 1160)
terrapin = Ships('Terrapin', 1, 1, 0, 210, 1205)
polaris = Ships('Polaris', 6, 14, 216, 0, 0)
wildfire = Ships('F7C Hornet Wildfire', 1, 1, 0, 185, 1224)
hurricane = Ships('Hurricane', 2, 2, 0, 265, 1125)
khartu = Ships('Khartu-Al', 1, 1, 0, 300, 1325)
starfarer = Ships('Starfarer', 4, 6, 295, 115, 890)
stalker = Ships('Avenger Stalker', 1, 1, 0, 250, 1310)
buccaneer = Ships('Buccaneer', 1, 1, 0, 280, 1315)
renegade = Ships('Avenger Titan Renegade', 1, 1, 8, 205, 1115)
gladius = Ships('Gladius', 1, 1, 0, 280, 1235)
merlin = Ships('P52 Merlin', 1, 1, 0, 270, 1030)
valiant = Ships('Gladius Valiant', 1, 1, 0, 220, 1236)
carrack = Ships('Carrack', 4, 6, 1000, 0, 0)
redeemer = Ships('Redeemr', 3, 5, 0, 0, 0)
herald = Ships('Herald', 1, 1, 0, 235, 1360)
javelin = Ships('Javelin', 12, 80, 5400, 0, 0)
beta = Ships('Mustang Beta', 1, 1, 0, 250, 1215)
gamma = Ships('Mustang Gamma', 1, 1, 0, 325, 1340)
delta = Ships('Mustang Delta', 1, 1, 0, 240, 1225)
omega = Ships('Mustang Omega', 1, 1, 0, 325, 1340)
santokyai = Ships("San'Tok.Yai", 1, 1, 0, 265, 0)
arrow = Ships('Arrow', 1, 1, 0, 270, 0)
triage = Ships('Apollo Triage', 0, 2, 28, 205, 0)
medivac = Ships('Apollo Medivac', 0, 2, 28, 195, 0)
vulture = Ships('Vulture', 1, 1, 12, 165, 0)
emerald = Ships('Constellation Phoenix Emerald', 3, 4, 0, 0, 0)
vulcan = Ships('Vulcan', 1, 3, 12, 210, 0)
hammerhead = Ships('Hammerhead', 3, 9, 40, 0, 0)
hawk = Ships('Hawk', 1, 1, 0, 200, 500)
pioneer = Ships('Pioneer', 4, 8, 600, 85, 0)
raven = Ships('Saber Raven', 1, 1, 0, 275, 1235)
explorer = Ships('600I Explorer', 2, 5, 40, 145, 975)
touring = Ships('600I Touring', 3, 5, 16, 135, 950)
andromeda = Ships('Constellation Andromeda', 3, 4, 96, 190, 910)
eclipse = Ships('Eclipse', 1, 1, 0, 195, 980)
defender = Ships('Defender', 1, 2, 0, 0, 0)
hoplite = Ships('Vanguard Hoplite', 2, 2, 0, 230, 1020)
warden = Ships('Vanguard Warden', 2, 2, 0, 225, 1115)
origin300 = Ships('300I', 1, 1, 2, 275, 1190)
origin315 = Ships('315P', 1, 1, 2, 275, 1225)
origin325 = Ships('325A', 1, 1, 2, 270, 1315)
origin350 = Ships('350R', 1, 1, 0, 345, 1345)
ghost = Ships('F7C-S Hornet Ghost', 1, 1, 0, 235, 1225)
tracker = Ships('F7C-R Hornet Tracker', 1, 1, 0, 240, 1215)
superhornet = Ships('F7C-M Super Hornet', 1, 2, 0, 230, 1220)
freelancer = Ships('Freelancer', 2, 4, 66, 205, 1005)
m50 = Ships('M50', 1, 1, 0, 330, 1345)
cat = Ships('Caterpillar', 2, 4, 576, 130, 890)
scythe = Ships('Scythe', 1, 1, 0, 285, 1240)
idrism = Ships('Idris-M', 8, 28, 831, 0, 0)
idrisp = Ships('Idris-P', 8, 28, 995, 0, 0)
fdur = Ships('Freelancer DUR', 2, 4, 28, 0, 0)
fmax = Ships('Freelancer MAX', 2, 4, 122, 0, 0)
fmis = Ships('Freelancer MIS', 2, 4, 28, 0, 0)
merchantman = Ships('Merchantman', 4, 8, 3584, 0, 0)
hornet7a = Ships('F7A Hornet', 1, 1, 0, 0, 0)
taurus = Ships('Constellation Taurus', 3, 4, 0, 0, 0)
phoenix = Ships('Constellation Phoenix', 3, 4, 0, 0, 0)
reclamer = Ships('Reclaimer', 4, 5, 180, 100, 930)
origin890 = Ships('890 Jump', 3, 5, 1600, 0, 0)
black = Ships('Cutlass Black', 2, 2, 46, 220, 1115)
red = Ships('Cutlass Red', 2, 2, 16, 0, 0)
blue = Ships('Blue', 2, 2, 25, 0, 0)
gladiator = Ships('Gladiator', 1, 2, 0, 200, 980)
orion = Ships('Orion', 4, 7, 384, 0, 0)
bomber = Ships('Retaliator Bomber', 4, 7, 0, 145, 814)
gemini = Ships('Starfarer Gemini', 4, 6, 295, 120, 890)
kore = Ships('Reliant Kore', 1, 2, 4, 220, 1150)
genesis = Ships('Genesis Starliner', 2, 8, 300, 0, 0)
glaive = Ships('Glaive', 1, 1, 0, 255, 1230)
harbinger = Ships('Vanguard Harbinger', 2, 2, 0, 0, 0)
sentinel = Ships('Vanguard Sentinel', 2, 2, 0, 0, 0)
endeavor = Ships('Endeavor', 3, 5, 500, 0, 0)
saber = Ships('Saber', 1, 1, 0, 275, 1235)
base = Ships('Retaliator Base', 4, 7, 0, 185, 815)
warlock = Ships('Avenger Warlock', 1, 1, 0, 240, 1305)
titan = Ships('Avenger Titan', 1, 1, 8, 260, 1115)
crucible = Ships('Crucible', 3, 8, 230, 0, 0)
archimedes = Ships('P72 Archimedes', 1, 1, 0, 0, 0)
mako = Ships('Reliant Mako', 1, 2, 0, 0, 0)
sen = Ships('Reliant Sen', 1, 2, 2, 0, 0)
tana = Ships('Reliant Tana', 1, 2, 0, 0, 0)
blade = Ships('Blade', 1, 1, 0, 290, 1240)
prospector = Ships('Prospector', 1, 1, 0, 200, 1210)
mpuvp = Ships('MPUV Personnel', 1, 1, 0, 150, 920)
mpuvc = Ships('MPUV Cargo', 1, 1, 2, 150, 900)
prowler = Ships('Prowler', 2, 2, 0, 0, 0)
comet = Ships('Saber Comet', 1, 1, 0, 215, 1235)
origin85x = Ships('85X', 1, 2, 0, 255, 1185)
catp = Ships('Caterpillar Pirate Edition', 2, 4, 576, 100, 892)
razor = Ships('Razor', 1, 1, 0, 335, 1345)
razorex = Ships('Razor EX', 1, 1, 0, 325, 1340)
razorlx = Ships('Razor LX', 1, 1, 0, 340, 1345)
origin100 = Ships('100I', 1, 1, 2, 210, 0)
origin125 = Ships('125A', 1, 1, 2, 230, 0)
origin135 = Ships('135C', 1, 1, 6, 190, 0)
c2hercules = Ships('C2 Hercules', 0, 2, 624, 135, 0)
m2hercules = Ships('M2 Hercules', 0, 3, 468, 130, 0)
a2hercules = Ships('A2 Hercules', 0, 8, 234, 130, 0)
valkyrie = Ships('Valkyrie', 0, 5, 0, 0, 0)
kraken = Ships('Kraken', 0, 10, 3792, 0, 0)
valkyriele = Ships('Valkyrie Liberator Edition', 0, 5, 0, 0, 0)
alphavin = Ships('Mustang Alpha Vindicator', 1, 1, 6, 255, 1160)

#  Test for formatting
'''
entry_name = blade
print(f'SPECS\nName---------:{entry_name.name}\nMin Crew-----:{entry_name.min_crew}\nMax Crew-----:{entry_name.max_crew}'
      f'\nCargo--------:{entry_name.cargo}\nSMC Speed----:{entry_name.scm_speed} m/s\nAfterburner--:{entry_name.aft_speed} m/s')
'''

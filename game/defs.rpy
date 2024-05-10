# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


image bg lake = "BG/lake.jpg"
image bg hut = "BG/hut.jpg"
image bg exterior = "BG/exterior.jpg"
image bg market = "BG/market.jpg"
image bg lakeside = "BG/lakeside.jpg"
image bg night = "Bg/night.jpg"
image bg sunset = "BG/sunset.jpg"
image bg water_close = "BG/waterclose.jpg"
image bg boats = "BG/boats.jpg"
image bg nightmarket = "BG/nightmarket.jpg"

image fishing gear = "BG_Props/fishing_gear.png"

image baitshop = "UrgNPCs/Trin.png"
image fishshop = "UrgNPCs/Roro.png"

define You = Character("You",color="#ffffff")

define Baitshop = Character("Trinika",color="#e4f82e")
define Fishshop = Character("Roro",color="#913bb3")
define Guy = Character("Guy", color="#375388")
define Giftshop = Character("Horse", color="#853118")

define npc = Character("[currentCharacter.name]",color="#52d69f") ## can't figure out how to make this color dynamic

## Not required to, but you may feel free to credit: _sae7
##
## This file is a self-contained basic fishing mini-game.
## You do not need anything else with this.
## You may freely add/change/distribute/etc. for personal and commercial projects.
##


init -5 python:
    import math
    import random
    ## Defining a `Fish` class with name, weight, height, and price of the fish.
    ## Price of the fish is equivalent to the weight divided by 2 times the height
    class Fish:
        def __init__(self, name, weight, height, description="This dumb fish isn't sexy AT ALL", dateable=True, max_affection=0, nameColor="#fff", lureTraits=["normal"], giftTraits=[], specialLure=None, negativeTraits=["crappy"],creator="",creatorUrl=""):
            self.name = name
            if (dateable):
                self.weight = weight
                self.height = height
            else:
                self.weight = (weight/2) + weight*renpy.random.random()
                self.height = (height/2) + height*renpy.random.random()
            self.price = round( (self.weight + self.height)*0.75 ,2)
            self.dateable = dateable
            if (dateable):
                self.max_affection = max_affection
            else:
                self.max_affection = 0
                self.nameColor = nameColor
            self.description = description
            self.stage=0
            self.lureTraits = lureTraits
            self.giftTraits = giftTraits
            if (specialLure != None):
                self.specialLure = Lure(specialLure,"A lure that can be used to instantly catch "+name,traits=[str(name)])
            if dateable:
                self.negativeTraits = negativeTraits
            else:
                self.negativeTraits = []
            self.caughtTimes = 0
            self.affectionLevel = 0
            self.creator = creator
            self.creatorUrl = creatorUrl
            self.stagesSeen = []

    caught_times = 1
    affection_level = 2
    weight = 3
    stage = 4
    variant = 4

    def character_trait(traitToGet):
        if traitToGet==caught_times:
            return currentCharacter.caughtTimes
        elif traitToGet==affection_level:
            return currentCharacter.affectionLevel
        elif traitToGet==weight:
            return currentCharacter.weight
        elif traitToGet==stage:
            return currentCharacter.stage

    class Lure:
        def __init__(self, name, description="A lure", uses=0, traits=["normal"], price=0):
            self.name = name
            self.price = price
            self.description = description
            self.uses = uses
            self.traits = traits
            self.image = "Lures/" + self.name + ".png"

    ## Defining an `Inventory` class that contains a list of our items and our coins.
    ## We have 2 methods, `addItem` and `sellItem`. Of course we could add more methods, and even allow for stacking of similar typed fishes.
    ## However, since we have varying weight and height, it is best not to stack them in 1 inventory slot.
    class Inventory:
        def __init__(self):
            self.items = []
            self.fish=[]
            self.gifts=[]
            self.victims=[]
            self.coins = 0.0

        ## `addItem` method - does what it's called. It adds the item (in this project, it adds fishes) into our inventory.
        def addItem(self, item):
            self.items.append(item)

        ## `sellItem` method - does what it's called. It sells the item (fishes) by deleting it from our inventory and adds coins based on the price of the fish.
        def sellItem(self, item):
            self.items.remove(item)
            self.coins += item.price
    
    def increase_affection(num):
        currentCharacter.affectionLevel += num
        renpy.call("affectionIncrease")

    def obtainSpecialLure():
        playersLures.addItem(currentCharacter.specialLure)
        currentLure = currentCharacter.specialLure
        renpy.call("get_lure")


    ## Instantiate our `Inventory` class for reusability
    inventory = Inventory()

    ##JUNK FISH
    Trout = Fish("Trout",2.0,2.0,dateable=False)
    Perch = Fish("Perch",2.0,2.0,dateable=False)
    Clownfish = Fish("Clown Fish",2,2,dateable=False,description="Marine biology fact: Not actually funny.")
    Banana = Fish("Banana Squid",0.8,0.6,dateable=False,description="One slippery customer.")
    Boot = Fish("Sole",2.4,0.8,dateable=False,description="Has a uniquely leathery texture.")
    iFsh = Fish("iFsh",69.9,3.6,dateable=False,description="A fish with no eyes but one incredibly swish and contemporary 'i'")

    #LURES
    Hook = Lure("Hook","A lure that's shaped like a fishing hook, who's horrible idea was that?",0,["normal","crappy"],1.50)
    Minnow = Lure("Minnow","Less tasty than the real thing but also more sustainable",0,["normal"],12.99)
    HulaGirl = Lure("Hula Girl","She shimmies! She shakes! She culturally appropriates! Good for hooking especailly horny catches",0,["normal","horny"],99.99)
    GraphicRasta = Lure("Graphic Rasta","This rastafarian skulls proves you can be cool AND celebrate your faith!",0,["normal","cool"],99.99)

    #GIFTS


    #fill the character pool with a bunch of junk fish
    characters = [Trout,Trout,Trout,Perch,Perch,Perch,Clownfish,Clownfish,Banana,Banana,Boot,Boot,iFsh]

    #this will be what's avaible to the player to catch when they start fishing (based on lure used)
    datingPool = []
    caughtToday = []
    fishyDex = []

    ##players starting lures
    playersLures = Inventory()
    playersLures.items = [Hook]

    ##bait shop's starting lures
    baitshopsLures = Inventory()
    baitshopsLures.items = [Minnow,HulaGirl,GraphicRasta]

    giftshopItems = Inventory()
    giftshopItems.gifts = []

    ## Method to generate a random fish from our 3 pools of possible fishes AND add it to our inventory in one go.
    ## To make a new fish, simply:
    ## `Fish(name="Fish Name", weight=round(renpy.random.uniform(2, 5), 2), height=renpy.random.randint(16, 28))`
    ## `name` is the name of the fish.
    ## `weight` is randomly generated between 2.0 to 5.0. 3.44444 for example, rounded to 2 decimal places, would be 3.44
    ## `height` is randomly generated between 16 to 28.
    ## Unfortunately I didn't account for fishes not to be exact whole-number heights before I started writing these documentations.
    def getFish():
        fish = renpy.random.choice(characters)
        inventory.addItem(fish)

    currentCharacter = None
    currentStage = 0
    currentExpression = ""
    stringo = ""
    currentLure = None

    endOfDay = False
    datingPoolSet = False

    location = "Home"

    playerName="Fisher"

## Our flag, whether or not we are casting our fish... rod... I don't know, I don't fish.
default casting = False

init python:
    def characterCode(st,at):
        stringo=""
        if currentCharacter.dateable:
            stringo = "Characters/[currentCharacter.name]/[currentCharacter.name]"
        else:
            stringo = "Characters/JunkFish/[currentCharacter.name]"
        if currentStage > 0:
            stringo = stringo + "_" + str(currentStage)
            if currentExpression != "":
                stringo = stringo + "_" + currentExpression
        stringo = stringo + ".png"
        return stringo,None

    def setStage(number):
        currentCharacter.stage=number
        currentStage=number

    def setExpression(string):
        currentExpression=string

    def clearExpression():
        currentExpression=""

    def increaseWeight(number):
        currentCharacter.weight = currentCharacter.weight + number

    def lureCode(st,at):
        if (currentLure):
            return currentLure.image, None
        else:
            return "Lures/hook.jpg", None
    
    
##time of day system
init -6 python:
    seconds = 21560
    day = 1

    def timeCode(sec):
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        #print("seconds value in hours:",hour)
        #print("seconds value in minutes:",min)
        return "{size=40}%02d:%02d" % (hour, min)

    def advanceMinutes(mins):
        global seconds
        seconds = seconds + (mins*60)

    def advanceHours(hours):
        global seconds
        seconds = seconds + ((hours*60)*60)


    affection_level = 0
    max_affection = 100

image character = DynamicDisplayable(characterCode)

image lure = DynamicDisplayable(lureCode)

screen clock:
    frame:
        xsize 384
        align(1.0,0.0)
        offset (-10,10)
        padding(10,10)
        vbox xalign 0.5:
            text "[timeCode(seconds)]" size 40 xalign 0.5
            timer 1.0 action IncrementVariable("seconds", 1) repeat True
            text "Day [day]" size 30 xalign 0.5
            text "$[playersLures.coins:.2f]" size 25 xalign 0.5
            $bleh = max(1,len(playersLures.fish)/6)
            grid 6 bleh:
                for y in playersLures.fish:
                    add "Minigame/fish.png" xysize(64,24)


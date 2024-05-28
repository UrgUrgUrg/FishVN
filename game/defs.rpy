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
image bg underwater = "BG/underwater.jpg"

image fishing gear = "BG_Props/fishing_gear.png"

image baitshop = "UrgNPCs/Trin.png"
image fishshop = "UrgNPCs/Roro.png"
image rodShop = "UrgNPCs/Rodney.png"
image giftShop = "UrgNPCs/Horse.png"
image blackMarket = "UrgNPCS/Guy.png"

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


init -600 python:
    import math
    import random

    characters=[]

    ## Defining a `Fish` class with name, weight, height, and price of the fish.
    ## Price of the fish is equivalent to the weight divided by 2 times the height
    class Fish:
        def __init__(self, name, weight=160.00, height=5.2, description="This dumb fish isn't sexy AT ALL", max_affection=100, nameColor="#fff", lureTraits=["normal"], giftTraits=["edible"], specialLure=None, commonality=1,negativeTraits=["crappy"],creator="",creatorUrl="",dateable=True,):
            global characters
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
            self.unlocked_traits=[]
            self.commonality=commonality
            for i in range(self.commonality):
                characters.append(self)

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

    baseLures=[]
    class Lure:
        def __init__(self, name, description="A lure", uses=0, traits=["normal"], price=0):
            global baseLures
            self.name = name
            self.price = price
            self.description = description
            self.uses = uses
            self.traits = traits
            self.image = "Lures/" + self.name + ".png"
            baseLures.append(self)

    baseGifts = []
    class Gift:
        def __init__(self, name, description="A gift", traits=["normal"], price=0.99, alt_names=[]):
            global baseGifts
            self.name = name
            self.price = price
            self.description = description
            self.traits = traits
            self.image = "Gifts/" + self.name + ".png"
            self.alt_names = alt_names
            baseGifts.append(self)

    class Upgrade:
        def __init__(self, name, description="Fishing rod upgrade", price=0,requires=None):
            self.name = name
            self.price = price
            self.description = description
            self.requires = requires
            

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
            self.upgrades = []

        ## `addItem` method - does what it's called. It adds the item (in this project, it adds fishes) into our inventory.
        def addItem(self, item):
            self.items.append(item)

        ## `sellItem` method - does what it's called. It sells the item (fishes) by deleting it from our inventory and adds coins based on the price of the fish.
        def sellItem(self, item):
            self.items.remove(item)
            self.coins += item.price


    def obtainSpecialLure():
        playersLures.addItem(currentCharacter.specialLure)
        currentLure = currentCharacter.specialLure
        renpy.call("get_lure")


    ## Instantiate our `Inventory` class for reusability
    inventory = Inventory()

    ##JUNK FISH
    Trout = Fish("Trout",2.0,2.0,dateable=False,commonality=3)
    Perch = Fish("Perch",2.0,2.0,dateable=False,commonality=3)
    Clownfish = Fish("Clown Fish",2,2,dateable=False,description="Marine biology fact: Not actually funny.",commonality=3)
    Banana = Fish("Banana Squid",0.8,0.6,dateable=False,description="One slippery customer.",commonality=2)
    Boot = Fish("Sole",2.4,0.8,dateable=False,description="Has a uniquely leathery texture.",commonality=2)
    iFsh = Fish("iFsh",69.9,3.6,dateable=False,description="A fish with no eyes but one incredibly swish and contemporary 'i'",commonality=2)

    #LURES
    Hook = Lure("Hook","A lure that's shaped like a fishing hook, who's horrible idea was that?",0,["normal","crappy"],1.50)
    Minnow = Lure("Minnow","Less tasty than the real thing but also more sustainable",0,["normal"],5.99)
    HulaGirl = Lure("Hula Girl","She shimmies! She shakes! She culturally appropriates! Good for hooking especially horny catches",0,["normal","horny"],29.99)
    GraphicRasta = Lure("Graphic Rasta","This rastafarian skull proves you can be cool AND celebrate your faith!",0,["normal","cool"],29.99)

    #GIFTS
    Candy = Gift("Box Of Candy","a selection of chocolates - the box is in the shape of a heart in honour of the organ chocolate does the most damage to.",["edible","sweet","romantic","chocolate"],6.99)
    Chips = Gift("Bag Of Chips","For the potential partner who's already 'all that'",["edible","savoury","casual","chips"],2.99)
    Apple = Gift("Apple","Use to attract teachers and repel doctors",["edible","sweet","healthy","fruit"],1.23)
    BananaFruit = Gift("Banana","I don't WANT to write the 'appeal' joke but there's just no way aRIND it",["edible","sweet","healthy","fruit"],0.58)
    Lager = Gift("Can Of Lager","Makes a satisfying noise when opened",["beer","alcohol","casual"],1.81)
    ImportLager = Gift("Can of Imported Lager","WHERE was it imported from? Does it matter, it costs more and is therefore a better gift!",["beer","alcohol","fancy"],3.46)
    DVD = Gift("Digital Versatile Disc","Wait, they still make these?",["media"],4.99)
    Console = Gift("Game Console","Okay so it's a knock-off product - but it's not like it's going to work underwater anyway! It's the gesture that counts!",["tech","media"],399.00,["Fintendo Switch","Breemdeck","Place-station 5","X-Lox"])
    Plushy = Gift("Plushy","A cute and cuddly lil so-and-so",["cute","soft"],15.99)
    Kitchenware = Gift("Kitchen Gadget","Just don't buy so many of these that you also end up needing a bigger kitchen",["homeware","tech","cooking"],104.78,["Air Fryer","Spiralizer","Coffee Machine","Bao Bun Steamer","Rice Cooker","Slow Cooker","Smoothie Maker","Mixer","Wine Fridge"])
    CostumeNecklace = Gift("Costume Necklace","Pretty but might dissolve once submerged",["pretty","jewellery","shiny"],29.99)
    DiamondNecklace = Gift("Diamond Necklace","An Eye-wateringly expensive extravagence.",["pretty","jewellery","shiny","valuable"], 3455.00)
    

    #UPGRADES
    Rod = Upgrade("Fishing Rod","Your trusty rod",0.00)
    Auto1 = Upgrade("Motorized Handle","This hands-free reeling solution increases your reeling power lets you automatically win on any catch under 2lbs",40.00,Rod)
    Auto2 = Upgrade("Gas-powered Motor","It's Environmentally unfriendly, yes but it's even more unfriendly to fish. Increases your reelking power and automatically catches anything lighter than 25lbs",60.00,Auto1)
    Auto3 = Upgrade("Overclocked Motor","It could explode at any moment, killing you instantly. But before it does that enjoy the extra reeling power and automatically catching anything lighter than 50lbs",80.00,Auto2)
    Hook1 = Upgrade("Extra hook","Attatch more hooks to your rod - more hooks means more fish caught in less time (though the hauls will be heavier)",20.00,Rod)
    Hook2 = Upgrade("Extra extra hook","It's just another hook - identical to the last one you bought so why it is more expensive? Blame inflation I guess", 30.00,Hook1)
    Hook3 = Upgrade("Frankly Unnecessary Extra Hook","At this point you just need to admit it: You're hooked on hooks and willing to pay any price for your next fix", 45.00,Hook2)
    Line1 = Upgrade("Reinforced line","Good news: this extra thick line means far less breakages. Bad news: Your remake of The Tingler will have to go on hiatus.", 25.00, Rod)
    Line2 = Upgrade("Unbreakable line","Say GOODBYE to lose states FOR GOOD. It's like you don't even care about the effort put into coding that 'your line broke' screen!",50.00,Line1)
    Auto4 = Upgrade("Nuclear Fishin' Core","Enough energy to power the whole island put to far better use as a means to increase your reeling power and automatically catch any haul under 100lbs. The power! THE POWER!",120.00,Auto3)
    
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

    datingPool = []
    caughtToday = []
    fishyDex = []
    playersLures = Inventory()

    ##bait shop's starting lures
    baitshopsLures = Inventory()

    giftshopItems = Inventory()

    rodShopItems = Inventory()

    currentCharacter = None
    currentStage = 0
    currentExpression = ""
    stringo = ""
    currentLure = None

    endOfDay = False
    datingPoolSet = False

    location = "Home"

    playerName="Fisher"


    baitshopsLures.items = [Minnow,HulaGirl,GraphicRasta]
    rodShopItems.upgrades=[Auto1,Hook1,Line1,Auto2,Hook2,Line2,Auto3,Hook3,Auto4]
    giftshopItems.gifts = [Candy,Chips,Apple,BananaFruit,DVD,Console,Lager,ImportLager,Plushy,Kitchenware]
    playersLures.items = [Hook]

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

    def galleryImageCode(st,at):
        global globallll
        stringo = "Characters/"+currentCharacter.name+"/"+currentCharacter.name+"_Gallery.png"
        if (not renpy.loadable(stringo)):
            stringo = "Characters/"+currentCharacter.name+"/"+currentCharacter.name+".png"
        return stringo, None

    def setStage(number):
        global currentCharacter
        global currentStage
        currentCharacter.stage=number
        currentStage=number
        renpy.show("character",[expressionChange])

    def setExpression(string):
        global currentCharacter
        global currentExpression
        currentExpression=string
        print(currentExpression+" is the current expressionO")
        renpy.show("character",[expressionChange])


    def clearExpression():
        global currentExpression
        if (currentExpression!=""):
            currentExpression=""
            renpy.show("character",[expressionChange])

    def increaseWeight(number):
        global currentCharacter
        currentCharacter.weight = currentCharacter.weight + number

    def lureCode(st,at):
        if (currentLure):
            return currentLure.image, None
        else:
            return "Lures/hook.jpg", None
    
transform expressionChange:
    yoffset 0.0
    linear 0.05 yoffset 10
    linear 0.1 yoffset 0.0
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


image galleryImage = Composite(
    (1920,1080),
    (0,0), "interface/HeartBG.jpg",
    (0,0), DynamicDisplayable(galleryImageCode)
)

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
            vpgrid cols 10 xalign 0.5 spacing 4 xmaximum 600:
                for y in playersLures.fish:
                    add "Minigame/fish.png" xysize( 32 ,12)



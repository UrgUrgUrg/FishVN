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
                self.weight = random.randrange(weight/2, weight*2) 
                self.weight = random.randrange(height/2, height*2) 
            self.price = round((weight/2) * height, 2)
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
            self.coins = 0

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
    Clownfish = Fish("Clown Fish",2,2,dateable=False)

    #LURES
    Hook = Lure("Hook","A lure that's shaped like a fishing hook, who's horrible idea was that?",0,["normal","crappy"],1.50)
    Minnow = Lure("Minnow","Less tasty than the real thing but also more sustainable",0,["normal"],12.99)
    HulaGirl = Lure("Hula Girl","She shimmies! She shakes! She culturally appropriates! Good for hooking especailly horny catches",0,["normal","horny"],99.99)
    GraphicRasta = Lure("Graphic Rasta","This rastafarian skulls proves you can be cool AND celebrate your faith!",0,["normal","cool"],99.99)

    #fill the character pool with a bunch of junk fish
    characters = [Trout,Trout,Perch,Perch,Trout,Clownfish]

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

    playerName="Fisher"

## Our flag, whether or not we are casting our fish... rod... I don't know, I don't fish.
default casting = False

label get_lure:
    play sound "SFX/getItem.ogg"
    show lure at topleft
    with easeinleft
    "Obtained [currentLure.name]"
    hide lure
    with dissolve
    return
    

transform fadeAway:
    align (0.5,0.5) alpha 1.0
    ease 2.0 alpha 0.0

label affectionIncrease:
    show text "{size=40}{color=#e64fb3}{b}AFFECTION INCREASED{/b}" with dissolve
    with Pause(1.5)
    hide text with dissolve
    return

## A transform to vibrate our text.
transform vibrate:
    rotate 0
    linear 0.1 rotate 5
    linear 0.1 rotate 0
    linear 0.1 rotate -5
    linear 0.1 rotate 0
    repeat

transform dontvibrate:
    rotate 0

label clockTest:
    "The time is [timeCode(seconds)]"
    menu:
        "wait ten minutes":
            $advanceMinutes(10)
        "wait an hour":
            $advanceHours(1)
    jump clockTest

label start:
    show screen clock
    $playersLures.addItem(GraphicRasta)
    $playersLures.addItem(HulaGirl)
    $playersLures.addItem(Minnow)
    $currentLure = playersLures.items[-1]
    jump hut

label hut:
    play music "hut.ogg"
    scene hut
    with dissolve
    menu:
        "Go to town":
            $advanceMinutes(10)
            jump town
        "Walk down to the lake":
            $advanceMinutes(15)
            jump lakeside
        "Go to bed":
            scene black
            with dissolve
            $seconds = 21560
            $endOfDay=False
            $datingPoolSet=False
            $caughtToday=[]
            "Zzz"
            scene hut
            with dissolve

init:
    $blackMarketUnlocked=False

label town:
    play music "market.ogg"
    scene bg market
    with dissolve
    menu:
        "Around you are several market stalls"
        "Go back home":
            $advanceMinutes(10)
            jump hut
        "Vist the bait stall":
            jump baitShop
        "Visit the gift stall":
            jump giftShop
        "Visit the black market" if blackMarketUnlocked:
            jump blackMarket
        "Sell your catches":
            jump fishShop
        "Walk to the lake":
            $advanceMinutes(5)
            jump lakeside

init:
    $rememberLure = 0

label fishingMenu:
    show lure at topleft
    with easeinleft
    menu fishing_menu:
        "Select your lure":
            $advanceMinutes(10)
            hide lure
            with easeinleft
            call screen lure_select
            $currentLure = playersLures.items[_return]
            if (rememberLure != _return):
                $remberLure = _return
                $datingPoolSet=False
                "You have equipped [currentLure.name]"
            else:
                "You decided to stick with [currentLure.name]"
            jump fishingMenu
        "Put fishing rod away":
            $advanceMinutes(20)
            play sound "SFX/closechest.ogg"
            jump lakeside
        "{color=#43f2ff}{size=+20}{b}Start Fishing{/b}{size=-20}" if not endOfDay:
            jump fishing_start

label lakeside:
    play music "Bossanova.ogg"
    scene bg lake
    with dissolve
    menu:
        "Unpack your fishing gear":
            $advanceMinutes(20)
            show fishing gear
            with dissolve
            play sound "SFX/setup.ogg"
            jump fishingMenu
        "Return home":
            $advanceMinutes(15)
            jump hut
        "Walk to town":
            $advanceMinutes(5)
            jump town


screen lure_select(shop = False):
    default activeButton = rememberLure
    default lureList = playersLures.items
    on "show" action If(shop,SetScreenVariable("lureList",baitshopsLures.items),SetScreenVariable("lureList",playersLures.items))
    frame align (0.9,0.5) xysize (600,800) padding(30,30):
        viewport draggable True:
            vbox:
                text lureList[activeButton].name size 60 xalign(0.5) color("#89deff")
                text lureList[activeButton].description
                null height 20
                if shop:
                    text "$"+ lureList[activeButton].price size 40 color("#d0ff28")
    frame align (0.2,0.5) xysize (900,800):
        vbox:                    
            text "Owned Lures..."
            viewport draggable True mousewheel True:
                grid 2 3 xalign(0.5):
                    for i, numeral index numeral in enumerate(lureList):
                        $imageString = lureList[i].image
                        $textString = lureList[i].name
                        button action Return(i),Hide("lure_select") hovered SetScreenVariable("activeButton",i):
                            vbox:
                                if (activeButton==i):
                                    add "[imageString]" at vibrate
                                else:
                                    add "[imageString]" at dontvibrate
                                text "[textString]"  xalign(0.5)

label baitShop:
    Baitshop "Welcome to De Bait Club, mon. We'll help you catch the fish of your dreams."
    jump baitshopMenu

label baitshopMenu:
    menu:
        "Browse her wares":
            call lure_select(shop=True)
            "You chose [baitshopsLures.items[_return]]"
        "Leave De Bait Club"

label giftShop:
    jump town

label fishShop:
    jump town

label blackMarket:
    jump town

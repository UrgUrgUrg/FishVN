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
        def __init__(self, name, weight, height, description="This dumb fish isn't sexy AT ALL", dateable=True, lureTraits=["normal"], giftTraits=[], specialLure=None, negativeTraits=["crappy"]):
            self.name = name
            if (dateable):
                self.weight = weight
                self.height = height
            else:
                self.weight = random.randrange(weight/2, weight*2) 
                self.weight = random.randrange(height/2, height*2) 
            self.price = round((weight/2) * height, 2)
            self.dateable = dateable
            self.description = description
            self.stage=0
            self.lureTraits = lureTraits
            self.giftTraits = giftTraits
            if (specialLure != None):
                self.specialLure = Lure(specialLure,"A lure that can be used to instantly catch "+name)
            if dateable:
                self.negativeTraits = negativeTraits
            else:
                self.negativeTraits = []
            self.caughtTimes = 0
            self.affectionLevel = 0

    caught_times = 1
    affection_level = 2

    def character_trait(traitToGet):
        if traitToGet==caught_times:
            return currentCharacter.caughtTimes
        elif traitToGet==affection_level:
            return currentCharacter.affectionLevel

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
        renpy.call_screen("affectionIncrease")

    def obtainSpecialLure():
        playersLures.addItem(currentCharacter.specialLure)
        currentLure = currentCharacter.specialLure
        renpy.call("get_lure")


    ## Instantiate our `Inventory` class for reusability
    inventory = Inventory()

    playersLures = Inventory()
    baitshopsLures = Inventory()


    ##JUNK FISH
    Trout = Fish("Trout",2.0,2.0,dateable=False)
    Perch = Fish("Perch",2.0,2.0,dateable=False)
    Clownfish = Fish("Clown Fish",2,2,dateable=False)

    #LURES
    Hook = Lure("Hook","A lure that's shaped like a fishing hook, who's horrible idea was that?",0,["normal","crappy"],1.50)

    #fill the character pool with a bunch of junk fish
    characters = [Trout,Trout,Trout,Perch,Perch,Clownfish]

    datingPool = []

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

    currentCharacter = characters[0]
    currentStage = 0
    currentExpression = ""
    stringo = ""
    currentLure = None

    endOfDay = False
    datingPoolSet = False

## Our flag, whether or not we are casting our fish... rod... I don't know, I don't fish.
default casting = False

label get_lure:
    play sound "SFX/getItem.ogg"
    show lure at topleft
    with easeinleft
    "Obtained [currentLure.name]"
    hide lure
    with dissolve
    

transform fadeAway:
    align (0.5,0.5) alpha 1.0
    ease 2.0 alpha 0.0

screen affectionIncrease:
    window at fadeAway:
        align (0.5,0.5)
        xysize (500,500)
        text "{color=#c96868}AFFECTION/nINCREASED"
    timer 2.0 action Hide("affectionIncrease")

## A transform to vibrate our text.
transform vibrate:
    pos(0.5, 0.4) anchor(0.5, 0.5) rotate 0
    linear 0.1 rotate 5
    linear 0.1 rotate 0
    linear 0.1 rotate -5
    linear 0.1 rotate 0
    repeat

label start:
    $playersLures.addItem(Hook)
    $currentLure = playersLures.items[0]
    jump hut

label hut:
    play music "hut.ogg"
    scene hut
    with dissolve
    menu:
        "Go to town":
            jump lakeside
        "Walk down to the lake":
            jump lakeside
        "Go to bed":
            scene black
            with dissolve
            $endOfDay=False
            $datingPoolSet=False
            "Your bookie always told you you'd end up sleeping with the fishes one day..."
            scene hut
            with dissolve

label fishingMenu:
    show lure at topleft
    with easeinleft
    menu fishing_menu:
        "Select your lure":
            hide lure
            with easeinleft
            call screen lure_select
            $currentLure = playersLures.items[_return]
            jump fishingMenu
        "Put fishing rod away":
            play sound "SFX/closechest.ogg"
            jump lakeside
        "{color=#43f2ff}{size=+20}{b}Start Fishing{/b}{size=-20}" if not endOfDay:
            jump fishing_start

label lakeside:
    play music "Bossanova.ogg"
    scene bg lake
    with dissolve
    menu:
        "Unpack your fishing rod":
            play sound "SFX/setup.ogg"
            jump fishingMenu
        "Walk back to town":
            return


screen lure_select:
    text "Owned Lures..."
    grid 3 3:
        align (0.5,0.5)
        xysize(800,800)
        for i, numeral index numeral in enumerate(playersLures.items):
            $imageString = playersLures.items[i].image
            $textString = playersLures.items[i].name
            button action Return(i),Hide("lure_select"):
                vbox:
                    add "[imageString]"
                    text "[textString]"



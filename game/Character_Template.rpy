init python:
## Define your characters stats, height and weight slightly contribute to their difficulty in the fishing game 
## lureTraits is a list of traits that fishing lures can have that will attract your character
## giftTraits is a list of traits gifts can ahve taht will increase your character's affection bar - valid traits are TBD 

    Lophi = Fish(
        name="Lophi",
        description="Somewhat guarded lantern fish.",
        weight=399.8,
        height=5.7,
        dateable=True,
        lureTraits = ["normal","horny","cool"],
        giftTraits = ["edible","sentimental"],
        specialLure = "Lantern fish fish lantern"
        creator="UrgUrgUrg",
        creatorUrl="https://crayondrawlings.neocities.org",
    )
    ## This next bit's super important as it adds them to the game's characters, make sure your character's name gets added in place of 'Lophi' here
    characters.append(Lophi)

## Define what colour your character's name has
define lophi = Character("Lophi",color="#51cfc9")

## These 'labels' are where your content will be written, their naming convention is important!
## they also all need to end in 'return'

init:
    $lophiGotFat=False
##feel free to define other varaibles you wnat to keep track of

label Lophi_Catch:

    ## 'caught_times' will incement whenever the player catches your character.
    ## You acn check this value like so:SS
    if (character_trait(caught_times)==1):
        lophi "Now just what the fuck do you think you're up to, homie?"
        menu:
            "Damn girl, you're thicker than the Mariana Trench":
                "The lantern above the creature's head glows a vibrant pink"
                lophi "Sh-shut the fuck up, ho. You don't know what your bitch-ass is talking about"
                $increase_affection(5)
                
                ## above is a function for increasing this character's affection towards the player - make sure to only
                ## use in a part of the label that only triggers once
            "Just catching fish!":
                lophi "Catching... OH. Oh that's fucking cute. You think you CAUGHT me. Nuh UH, holmes. Nope. I only came up here to see what was up, I could have got away from your bitch-ass little string on a stick any time."
    elif (character_trait(caught_times==2)):
        jump label_example
    elif (character_trait(affection_level) < 10):
            lophi "Are you for real? THIS fool again?!"
    elif (character_trait(affection_level) < 20):
            lophi "What you bothering me for this time? It better be either to feed me or rub my fins"
    elif (character_trait(affection_level) < 20):
            ## here's how to set expressions, now Lophi will use Lophi_happy.png and Lophi_1_happy.png
            ## instead of Lophi.png or Lophi_1.png
            $setExpression("happy")
            lophi "Sup holmes"
            $clearExpression()     # simple function to reset character's expression string to ""
            ####
    ### heres' how you can your character to progress to a new visual stage
    ### This will make Lophi use her Lophi_1.png image instead of Lophi.png
    if (character_trait(affection_level)>10):
        setStage(1)
    ####
    return

label Lophi_AcceptGift:
    ## Character accepts a gift, increasing their affection level by it's value
    if (character_trait(affection_level)<10):
        lophi "Your ass think my ass can be BRIBED? *sucks teeth*"
    elif (character_trait(affection_level)<20):
        lophi "A'ight. You a suck-up but you cute with it."
    else:
        $setExpression("happy")
        lophi "Maybe you do know how to show a girl a good time. Here why don'tchu have this..."
        ## This function will allow you to make your character give the player their 'talk to any time' lure
        $obtainSpecialLure()
    return

label Lophi_UsedSpecialLure:
    lophi "Finally, I was tired of waiting for your bitch ass to call me up here."
    return

label Lophi_RejectGift:
    ## Character rejects a gift (it does not contain one of their 'giftTraits')
    lophi "That's ratchet."
    return

label Lophi_ThrownBack:
    ## A little optional sign-off for when the player has talked to your character enough
    ## and throws them abck in the water
    if character_trait(affection_level) > 10:
        lophi "Later holmes"
    else:
        lophi "Bye bitch"
    return

label label_example:
    ##Feel free to create your own labels and reference them from within the labels above to help keep things organized
    lophi "Motherfucker I had JUST sat down for lunch!"
    return



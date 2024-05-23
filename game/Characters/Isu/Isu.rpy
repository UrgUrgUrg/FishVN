init python:
## Define your characters stats, 

    Isu = Fish(
        name="Isu",
            ## ^ Your character's name, your below labels must use this
        nameColor="#60bed2",
            ## ^ Define what colour your character's name has above their dialogue boxes - not implemented yet, this specifically is hard for w/e reason
        description="A feisty squid with a short temper and an eye for treasure",
            ## ^ Something short and sweet for their entry in the fishydex
        weight=286.7,
        height=5.47,
            ## ^ height and weight slightly contribute to their difficulty in the fishing game 
        max_affection=100,
            ## ^ how much accumulated gift value the player will need to invest to unlock the 'Confession' scene
        lureTraits = ["shiny","tasty","cool"],
            ## ^ Traits that a lure can have that will attract this character - take out 'normal' to make them more rewarding to discover
        giftTraits = ["edible","valuable","shiny"],
            ## ^ Traits that a gift can have that will cause this character to accept
        specialLure = "Black Pearl",
            ## ^ The name of this character's unique lure (optional)
        creator="SquidFriend",
        creatorUrl="https://twitter.com/ZachtVisachtig",
            ## ^ Bio info about you
    )
    
    characters.append(Isu)
        ## ^This bit of code's's super important as it adds your Fish() object to the game's characters, make sure your character's object name gets added in place of 'Isu' here

    #characters = [Isu]
        ### ^ Uncomment the code above to make Isu the game's ONLY character - this will be super helpful for testing!

init:
    $IsuGotFat=False
##feel free to define other varaibles you want to keep track of


## Below you can use Renpy labels to create scenes with your character, their naming convention is
##important!
## the structure of them is:

## Charactername_Catch - what character say to you when they emmerge from the water
## Charactername_Talk - what happens when the player selects the 'Talk to' option
## Charactername_AcceptGift - what happens when a player chooses 'give gift to' and selects a gift the character likes
## Charactername_RejectGift - what happens when a character doesn't like a gift
## Characteranme_Confession - when you've maxed out your characters' affection bar, this special scene plays. Optionally supply a 'Charactername_Gallery.png' file to include an unlocked gallery image
## Charactername_Thrownback - what the character says when the conversation is over and the character is thrown back into the lake
## Charactername_Tranquilised - What the character says if the player attempts to tranquilise them and add them to their inventory

## characters have an affection level that goes from 0 to the number you set as their max_affection
## (default 100). As their affection increases, more scenes are unlocked.

## Creating a label named Charactername_Talk_10 will create an alternative version of the 'talk' scene
## that only plays when their affection level is equal to or greater than 10

## Creating a label named Charactername_Talk_10_revisit will create an alternative version of the 'Talk'
## scene that plays if the player encounters the character, has seen the content in 'Characternmae_Talk_10'
## but hasn't yet increased their affection enough to unlock a new stage of content - in this way anything
## special you set up in this affection tier's dialogue (such as choices that increase/decrease affection)
## will only occur once

label Isu_Catch:
        ## create dialogue lines by putting 'npc ' in front of quoted text
    npc "Who the hell are you? You got some nerve trying to nab me. You better have a good explanation..."
        ## and narration by just adding a line of quoted text on it's own
    "The Squid seems angry to have been hooked and her tentacles are writhing with unknows intent, she's glaring straight into my soul. I should probably watch my wording"
    return

label Isu_Catch_revisit:
    npc "You're not gonna like how this ends."
    "Slowly but steadily tentacles begin to surround you as you lock eyes"
    return

label Isu_Talk:
    npc "Well, speak up already!"
    menu:
        "Wow, you sure look round and squishy!":
            npc "... I'm going to devour you now..."
            "Tentacles surround and constrict as you're being forced underneath the great squids body, where a large nasty beak waits to greet you. You died"
            "I was looking for somebody to who'd be interested in treasure."
            npc "Treasure you say?"
            "She seems intrigued"
            $increase_affection(5)
            ## above is a function for increasing this character's affection towards the player - make sure to only
            ## use in a part of the label that only triggers once
        "I uhh... Was just trying to catch some fish":
            npc "Really now? Never occured to you that maybe I wouldn't enjoy getting \"caught\"? But I s'pose that I could overlook this grievous insult of yours with some kind of compensation... hehe"
    call Isu_convo
    return

label Isu_Talk_revisit:
    call label_IsuConvo
    return

label Isu_AcceptGift:
    ## Character accepts a gift, increasing their affection level by it's value
    npc "Your ass think my ass can be BRIBED? *sucks teeth*"
    return

label Isu_RejectGift:
    ## Character rejects a gift (it does not contain one of their 'giftTraits')
    npc "That's ratchet."
    return

label Isu_ThrownBack:
    ## A little optional sign-off for when the player has talked to your character enough
    ## and throws them back in the water
    npc "Bye bitch"
    return

label Isu_UsedSpecialLure:
    npc "Finally, I was tired of waiting for your bitch ass to call me up here."
    return

label Isu_Confession:
    npc "Hey... look..."
    npc "I'm sorry I was frontin' wichu before. I don't really trust new people that easily."
    npc "Especially not you surface-dwellin' types who generally wanna eat me or study me or melt my ass into a soap bar or yell out jokes about Ohio to me that, straight up, I do not get!! And will not look up context for!!"
    npc "But, I really like hanging wichu... Like a lot. You ain't scared of me, you don't pity me... Hell, you act like I'm doin' YOU a favor lettin' me sit here eating your shrimp and bitching..."
    npc "What I'm tryna say is... I wanna be real wichu. I don't want these talks to stop... Like, ever? I don't think I actaully wanna be more than a fathom away from your mammaly-ass, nasty-ass toenail-havin' feet ever again..."
    npc "Can we... I dunno... \nMake that happen?"
    menu:
        "*kiss her*":
            npc "WOOOOAH!!!"
            npc "OH SHIT!!! OH FUCK!!"
            npc "Oh goddamn I didn't know if I'd be ready but I WAS READY"
            npc "I'm so glad we made this official, boo. You are the greatest motherfuckin' thing in my goddamn life - You know that."
            npc "Oh my God, I can't stop blushing. I need to get back in the water and cool my ass off."
            npc "And you'll be here when I come back, right? Aw fuck it, you've got our special lure. Just call me up whenever, baby"
            npc "(I just called [playername] 'baby' what the fuck? What the FUCK, Isu)"

## The below scenes will only play if the player has increased Isu's affection to 10
## or more

label Isu_Catch_10:
    npc "Are you for real? THIS fool again?"
    return

label Isu_Talk_10:
    npc "Pff, whatever."
    call Isu_convo

label Isu_AcceptGift_10:
    npc "A'ight. You a suck-up but you cute with it."
    return

## The below scenes will only play if the player has increased Isu's affection to 25
## or more

label Isu_Catch_25:
    npc "What you bothering me for this time? It better be either to feed me or rub my fins"
    return

label Isu_AcceptGift_25:
    $setExpression("happy")
    npc "Maybe you do know how to show a girl a good time. Here why don'tchu have this..."
    ## This function will allow you to make your character give the player their 'catch any time' lure
    $obtainSpecialLure()
    return

label Isu_RejectGift_25:
    npc "Aw c'mon holmes. You know my taste better'n that."
    return

label Isu_Talk_25:
    npc "Yeah I guess I'm down to talk for a while."
    npc "You know - just to kill time for a while"
    npc "(not like this is a highlight of my day or nothing)"
    call Isu_convo
    return

label Isu_Thrownback_25:
    npc "Later homie"
    return

## The below scenes will only play if the player has increased Isu's affection to 50
## or more

label Isu_Catch_50:
    $setExpression("happy")
    npc "Sup holmes"
    $clearExpression()     # simple function to reset character's expression string to ""
    return

label Isu_Talk_50:
    npc "Whachu wanna ask me, holmes?"
    call Isu_convo
    return

init:
    $IsuGotFat=False ## You can define your own varibles in an 'init' block

label Isu_AcceptGift_50:
    npc "This pampering's starting to affect my damn waistline."
    $IsuGotFat=True
        ### ^  then set them like so
    $setStage(1)
        ### ^ heres' how you can your character to progress to a new visual stage
        ### This will make Isu use her Isu_1.png image instead of Isu.png
        ### check which stage a character's on directly with 'character_trait(stage)'
    $increaseWeight(20)
        ## ^ just for fun, change the character's weight stat, very slightly
        ## affecting how they play in the minigame (can also use minus value)
    return

## This revisit label will ensure that Isu's weight only increases once this tier 
label Isu_AcceptGift_50_revisit:
    npc "Seriously, am I lookin' chunkier to you?"
    return

label Isu_RejectGift_50:
    npc "I can only talk like this wichu 'cos we tight: This gift fucking sucks, dude"
    return

## The following labels are for when Isu's affection has reached it's maximum - after her confession scene.

label Isu_Catch_100:
    npc "Hey baby."
    return

label Isu_Talk_100:
    npc "My brothers are STOKED to meet you, by the way. You ain't gonna tell them I'm secretly a mushy, gushy dork around you right?"
    call Isu_convo

label Isu_Talk_100_revisit:
    npc "Yeah you talk away, baby. I'ma just watch yo mouth go up and down and think about how it'd feel sucking my tailfin"
    call Isu_convo

label Isu_AcceptGift_100:
    npc "That's sweet of you, baby but next time save it for some other fish. I already like yo ass"
    return

label Isu_RejectGift_100:
    npc "Siiigh, even after all this time you still buy me the most ratchet junk..."
    return

    ## You acn create your own renpy labels and reference them from within the labels above to help keep
    ## things further organized.
    ## This is a general dialogue tree you can talk to Isu with at any stage of your relationship.
    ## It makes use of some renpy techniques you might want (but should not feel pressured) to use
    ## in your own script.

init:
    $askedIsuAbout = []
        ## ^An uncluttered way of tracking what dialogue choices have already been selected

label Isu_convo:
    menu:
        "Tell me about yourself":
            if (affection_level<1):
                    ## ^ Alternative way of checking affection level
                npc "Man, fuck you. Buy me dinner first."
            elif (affection_level<50):
                npc "Well shit, since you've got me on the line and all... What does your ass wanna know?"
                jump Isu_questions
            else:
                npc "AMA, homie."
                jump Isu_questions
        "I think your new weight looks good on you" if (IsuGotFat is True and not 'complimentweight' in list(askedIsuAbout)):
            "Isu just about manages to supress her smirk, but her lantern glows warmly regardless."
            npc "Shut up, dumbass."
            $increase_affection(10)
            $askedIsuAbout.append("complimentweight")
        "*End conversation*":
            pass
    return

label Isu_questions:
    menu:
        "I'm [playerName]" if not 'introductions' in list(askedIsuAbout):
            npc "Isu. It's... 'an event in my day' to meet you."
            $askedIsuAbout.append("introductions")
            jump Isu_questions
        "Any family?" if not 'family' in list(askedIsuAbout):
            npc "I live with my three brothers, way down at the bottom of the lake."
            npc "The littlest one's kinda sick and the other two are just fuck-ups so it's up to big sis here to keep 'em fed and out of tuna nets."
            $askedIsuAbout.append("family") ### add this to topics taht have been spoken about
            jump Isu_questions
        "What are your brother's names?" if 'family' in list(askedIsuAbout) and not 'brothernames' in list(askedIsuAbout):
            if (affection_level < 25):
                    ## ^ Alternative way of checking affection level
                npc "Who wants to fucken know, Zuckerburg? Keep this shit between us!"
            else:
                npc "Mychal, Perco and... sigh... Bullshit Artist Supreme. He... uh, chose his own name after he transitioned."
                npc "That fool's OLDER than me if you can believe it (my ass sure can't sometimes)."
                npc "Then Myc and Perk are the two babies, Myc was born with a buncha problems so Perk's super protective of him"
                npc "He's adorable tryna be this Big Tough Older Brother. Like I wasn't changin' yo diapers five minutes ago, dude! Sit down!"
                "Isu looks whistful for a second, her lantern's color settles ona  cool blue"
                npc "It'd be cool if you could come down and meet 'em some day. You'd... prolly need like a diving suit or something."
                $askedIsuAbout.append("brothernames")
            jump Isu_questions
        "Aren't anglerfish usually saltwater creatures?" if not 'freshwater' in list(askedIsuAbout):
            npc "My family moved! You got a problem with that?"
            npc "I dunno, the algae out here's meant to be good for my lil' brother's gill condition or some shit."
            npc "Gotta try this stuff out if it's for family, y'know."
            $askedIsuAbout.append("freshwater")
            jump Isu_questions
        "I'll stop interrogating you now":
            npc "Kind of you!"
            jump Isu_convo



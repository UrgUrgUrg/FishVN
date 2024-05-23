default fishingTimer = 0
default fishDepth = 0
default fishWeight = 400
default fishingX = 960
default fishX = 960
default fishSpeed = 15
default distance = 0
default charName = ""
default correctSide = False

init python:
    import math
    

    class DynamicLine(renpy.Displayable):

        def __init__(self, x1, y1, x2, y2, **kwargs):
            super(DynamicLine, self).__init__(**kwargs)
            self.x1 = max(0,x1)
            self.y1 = max(0,y1)
            self.x2 = max(0,x2)
            self.y2 = max(5,y2)
            #self.child = renpy.displayable("Minigame/Rod.png")

        def render(self, width, height, st, at):
            r = renpy.Render(1920, 1080)
            s = r.canvas()
            ##blueness = min(255,max(0,(fishDepth/2500)*255))
            blueness = 50
            greenness=0
            redness=0
            if (correctSide):
                greenness = 255
            else:
                redness = 255
            c = (redness,greenness,blueness)
            t = max(0,2 + 3*distance)
            s.polygon(c, [(max(0,self.x1-t), max(0,self.y1)),(max(1,self.x1+t),max(0,self.y1)),(max(1,self.x2+t),max(1,self.y2)),(max(0,self.x2-t),max(1,self.y2))],0)

           ## t = Transform(child=self.child)

            # Create a render from the child.
            #child_render = renpy.render(t, width, height, st, at)

            # Blit (draw) the child's render to our render.
            #r.blit(child_render, (self.x1-318, 0))
            return r

       ## def event(self, ev, x, y, st):
            ##self.x1 = fishingX
            ##self.y2 = fishDepth
            ##renpy.redraw(self, 0)

    def dynamic_rotate(trans, st, at):
        if st >0.6:
            return None
        elif st > 0.4:
            theValue = -30*distance
            trans.rotate = (theValue*st)
            return 0
        elif st < 0.2:
            theValue = 30*distance
            trans.rotate = (theValue*st)
            return 0
        else:
            theValue = -30*distance
            trans.rotate = (theValue*st)
            return 0

    def flipRod(trans,st,at):
        if (fishX > fishingX):
            trans.xzoom = 1.0
        else:
            trans.xzoom = -1.0
        return 0.1
        
transform rodrot:
    transform_anchor True anchor(1.0, 0.0) rotate 0 xzoom 1.0
    function dynamic_rotate
    function flipRod
    repeat   

transform slowzoom:
    xysize (500,500)
    ease 3.0 xysize (700,700)

transform struggle:
    rotate 0 
    ease 0.4 rotate 80*distance 
    ease 0.2 rotate 0
    ease 0.4 rotate -80*distance
    ease 0.2 rotate 0
    repeat
      

screen minigame:
    #variables
    modal True
    default tick = 0
    default reversal = False
    default fishEnergy = 100.0
    default allowedDistance = 1300
    default reelTimer = 0
    $fishingX = (renpy.get_mouse_pos()[0])
    key "K_LEFT" action SetVariable("fishingX",fishingX - 1) 
    key "K_RIGHT" action SetVariable("fishingX",fishingX + 1) 
    on "show" action SetVariable("fishingTimer",0)
    on "show" action SetVariable("fishX",renpy.random.randint(900, 1020))
    on "show" action SetVariable("fishDepth",min(2500 - currentCharacter.weight*2,1100.0 + (currentCharacter.weight)))
    #graphics
    on "show" action Play("sound","SFX/HitWater.ogg"), Play("music","Reggae.ogg")
    add DynamicDisplayable(characterCode) at struggle:
        anchor(0.5,0.3)
        xpos round(fishX)
        ypos round(fishDepth)
        xsize 200
        ysize 200 
    add DynamicLine(fishingX, 5, fishX, max(5,fishDepth))
    add "Minigame/Rod.png" xpos fishingX at rodrot
    text "Time: [fishingTimer] \n FishX: [fishX] FishDepth: [fishDepth]\n Tick: [tick] - [reversal]\n Distance: [distance]\n Fishenergy: [fishEnergy] Fish speed: [(fishSpeed+(fishEnergy*0.2))]"
    #gameplay code
    timer 0.1 action SetVariable("fishDepth", fishDepth+(fishWeight/15)) repeat True
    timer 0.4 action SetScreenVariable("allowedDistance",(max(30,fishDepth/2500)*1300)) repeat True
    button:
        xsize 1920
        ysize 1080
        keysym "K_SPACE"
        action SetScreenVariable("reelTimer",5), Play("sound","SFX/Reeling.ogg")
    timer 0.05 action If(reelTimer>0, SetVariable("fishDepth",max(0,fishDepth-25-(100-fishEnergy)))), SetScreenVariable("reelTimer",reelTimer-1) repeat True
    timer 0.05 action SetVariable("distance", ((math.dist( (fishingX,5),(fishX,5))) / allowedDistance)*1) repeat True
    timer 5.0 action IncrementVariable("fishingTimer", 1) repeat True
    $fishForce=(fishSpeed-(fishEnergy*0.2))
    timer 0.01 action If(reversal is True, SetVariable("fishX",max(max(0,fishingX-allowedDistance),fishX-fishForce)), SetVariable("fishX",min(min(1920,fishingX+allowedDistance),fishX+fishForce))) repeat True
    timer 1.0 action If(renpy.random.randint(0,1)==0,SetScreenVariable("reversal",False),SetScreenVariable("reversal", True)) repeat True
    timer 0.01 action If((reversal==True and (fishX>fishingX)) or (reversal==False and (fishX<fishingX)),SetVariable("correctSide",True),SetVariable("correctSide", False)) repeat True
    timer 0.01 action If(correctSide,SetScreenVariable("fishEnergy", max(0.0,fishEnergy - (11.0*distance))), SetScreenVariable("fishEnergy", min(100.0,fishEnergy + 0.25))) repeat True
    bar:
        value AnimatedValue(value=fishEnergy, range=100, delay=0.1, old_value=None)
        xysize(1000, 50)
        align (0.5,0.6)
    text "LINE SLACK: [fishEnergy:.3f]%" align(0.5,0.6)
    bar:
        value AnimatedValue(value=fishDepth, range = 2500, delay=0.1, old_value=None)
        bar_vertical True
        bar_invert True
        thumb "Minigame/fish.png"
        align(0.01,0.5)
        ysize 1240
        xsize 40
        bottom_bar Solid("#e70c0c")
    timer 0.5 action If(fishDepth>(2500),Show("failGame"),NullAction()) repeat True
    timer 0.5 action If(fishDepth<25,Show("winGame"),NullAction()) repeat True
    
screen failGame:
    ## When this screen is shown, we hide our mini-game, because the player has already failed at this point! Also resets casting flag to False
    on "show" action Hide("minigame")
    on "show" action Stop("sound"), Play("sound","SFX/snap.ogg")
    ## Left click, space, and whatever button player uses to advance game will automatically hide the fail screen.
    ##dismiss action Hide("failGame")
    text "Your line broke!!" size 100 align(0.5, 0.5)
    ## Automatically hides the screen if the player doesn't click within 1.0 second.
    timer 2.0 action Hide("failGame"), Jump("justFailed")

screen winGame:
    ## When this screen is shown, we hide our mini-game, because the player has already failed at this point! Also resets casting flag to False
    on "show" action Hide("minigame")
    on "show" action Stop("sound"), Play("sound","SFX/splash.ogg"), Play("sound","victory.ogg",loop=False),PauseAudio("music",True)
    timer 1.5 action PauseAudio("music",False)
    ## Left click, space, and whatever button player uses to advance game will automatically hide the fail screen.
    ##dismiss action Hide("winGame")
    add DynamicDisplayable(characterCode) at slowzoom:
        size (500, 500)
        align (0.5,0.0)
    text "Thou Hath Caught A Fishy" size 100 align(0.5, 0.5)
    ## Automatically hides the screen if the player doesn't click within 1.0 second.
    timer 3.0 action Hide("winGame"), Jump("caught_character")

label fishing_start:
    if not datingPoolSet:
        python:
            datingPool=[]
            for c in characters:
                for t in c.lureTraits:
                    for lt in currentLure.traits:
                        if t==lt:
                            if (not c in caughtToday):
                                if not c.dateable:
                                    c.height = c.height/2 + c.height*random.random()
                                    c.weight = c.weight/2 + c.weight*random.random()
                                c.price = round((c.weight + c.height)*0.75, 2)
                                datingPool.append(c)
            renpy.random.shuffle(datingPool)
        $datingPoolSet=True
    jump fishing

label justFailed:
    play music "fishing.ogg"
    $advanceMinutes(fishingTimer)
    "Reattaching line.{w=0.2}.{w=0.2}.{w=0.2}."
    $advanceMinutes(15)
    if not currentCharacter in list(datingPool):
        $datingPool.append(currentCharacter)
    jump fishing_menu

label fishing:
    play sound "SFX/cast.ogg"
    $advanceMinutes(10)
    if datingPool:
        python:
            currentCharacter = datingPool.pop()
            fishWeight = currentCharacter.weight
            fishSpeed = max(3,currentCharacter.weight/20)
            charName = currentCharacter.name
            currentExpression = ""
            currentStage = currentCharacter.stage
        "You cast your line{w=0.2}.{w=0.2}.{w=0.3}.{w=0.3}.{w=0.4}.\nA bite!"
    else:
        "You cast your line{w=0.2}.{w=0.2}.{w=0.3}.{w=0.3}.{w=0.4}.{w=0.4}.{w=0.4}.\nBut nothing else seems to be biting today. Maybe they're tired of this lure..."
        jump fishing_menu 
    menu:
        "This catch seems about [str(round(currentCharacter.weight))] lbs"
        "Reel 'em in!":
            scene bg underwater
            with dissolve
            # call screen minigame
            if (fishing_settings=="skip"):
                call screen winGame
            else:
                call screen minigame
        "Keep waiting":
            jump fishing
        "End fishing":
            jump fishingMenu

transform throwback:
    transform_anchor True anchor(0.5, 0.5) rotate 0 xzoom 1.0 yzoom 1.0 xoffset 0 yoffset 0
    linear 0.5 yoffset -700 xzoom 0.5 yzoom 0.5 rotate 700
    linear 1.0 yoffset -200 xzoom 0.0 yzoom 0.0 rotate 1300

label findLabel(suffix):
    if (not currentCharacter.dateable):
        return
    $i = 0
    $stageQueue = []
    $expressionString = charName.replace(" ", "_")+"_"+suffix

    if (renpy.has_label(expressionString)):
        if (not expressionString in list(currentCharacter.stagesSeen)):
            $currentCharacter.stagesSeen.append(expressionString)
            call expression expressionString
            return
        else:
            $stageQueue.append(expressionString)

    while (i <= currentCharacter.affectionLevel):
        $theString = expressionString+"_"+str(i)
        if (renpy.has_label(theString)):
            if (not theString in list(currentCharacter.stagesSeen)):
                $currentCharacter.stagesSeen.append(theString)
                call expression theString
                return
            else:
                $stageQueue.append(theString)
        $i += 1
    $i=0

    if stageQueue:
        if renpy.has_label(stageQueue[-1]+"_revisit"):
            call expression stageQueue[-1]+"_revisit"
            return
        else:
            call expression stageQueue[-1]
            return
    else:
        return


        


    return

init python:
    affectionMusic = [1,2,5,7,10]


label caught_character:
    scene lake
    with dissolve
    if (currentCharacter.dateable):
        $caughtToday.append(currentCharacter) ##cant catch twice in one day even if you switch lures
        if currentCharacter.affectionLevel>0:
            $musicNum = min(affectionMusic, key=lambda x:abs(x-((currentCharacter.affectionLevel/currentCharacter.max_affection)*10)))
        else:
            $musicNum = affectionMusic[0]
        play music "affection_level_"+str(musicNum)+".ogg"
    else:
        play music "normalfish.ogg"
    $advanceMinutes(fishingTimer)
    $currentCharacter.caughtTimes += 1
    $talkedTo=False
    $givenGift=False
    $affection_level = currentCharacter.affectionLevel
    $max_affection = currentCharacter.max_affection
    if not currentCharacter in fishyDex:
        $fishyDex.append(currentCharacter)
    $clearExpression()
    show character:
        align (0.5,0.3)
    with easeinbottom
    call findLabel("Catch")
    jump catch_menu

transform galleryReveal:
    xzoom 1.0 yzoom 1.0 alpha 0.0 align (0.25,0.1)
    ease 1.0 alpha 1.0
    ease 3.0 xzoom 0.5 yzoom 0.5

label check_for_confession:
    if currentCharacter.dateable:
        if (currentCharacter.affectionLevel >= currentCharacter.max_affection):
            if not (charName+"_Confession") in list(currentCharacter.stagesSeen):
                play music "affection_level_10.ogg"
                if renpy.has_label(charName+"_Confession"):
                    call findLabel("Confession")
                show galleryImage at galleryReveal
                "You have succesfully reached max affection for [charName]"
                hide galleryImage
                with dissolve
                $currentCharacter.stagesSeen.append(charName+"_Confession")
    return

default giftsGiven = []

label catch_menu:
    call check_for_confession
    menu char_menu:
        "Talk with [charName]" if not talkedTo:
            $clearExpression()
            $advanceHours(1)
            $talkedTo=True
            if (currentCharacter.dateable == True):
                if renpy.has_label(charName+"_Talk"):
                    call findLabel("Talk")
                else:
                    "You and [charName] chat for a while."
                jump catch_menu
            else:
                jump blubtalk
        "Give [charName] a gift" if (currentCharacter.dateable == True) and not givenGift and list(playersLures.gifts):
            $clearExpression()
            call screen gift_select(playersLures.gifts,True)
            if _return!=["horace"]:
                $giftsGiven = _return
                $advanceHours(1)
                $givenGift=True
                $renpy.random.shuffle(currentCharacter.giftTraits)
                $giftAccepted=False
                python:
                    for i in list(currentCharacter.giftTraits):
                        for y in giftsGiven[0].traits:
                            if y==i:
                                giftAccepted=True
                $lenno = len(giftsGiven)
                "You offer [charName] a gift ([giftsGiven[0].name] x [lenno])"
                if giftAccepted:
                    jump gift_accept
                else:
                    jump gift_reject
            else:
                jump catch_menu
        "Add [charName] to inventory" if not currentCharacter.dateable:
            hide character
            with easeoutbottom
            play sound "SFX/fishadd.ogg"
            $playersLures.fish.append(currentCharacter)
            jump fishingMenu
        "Throw [charName] back":
            jump end_converstion

label gift_accept:
    if renpy.has_label(charName+"_AcceptGift"):
        call findLabel("AcceptGift")
    "[charName] has accepted your gift"
    python:
        for g in list(giftsGiven):
            playersLures.gifts.remove(g)
    $increase_affection(round(giftsGiven[0].price * len(giftsGiven)))
    $giftsGiven=[]
    jump catch_menu

label gift_reject:
    if renpy.has_label(charName+"_RejectGift"):
        call findLabel("RejectGift")
    "[charName] has rejected your gift"
    $increase_affection(2)
    $giftsGiven=[]
    jump catch_menu

label end_converstion:
    play sound "SFX/whoosh.ogg"
    show character at throwback
    pause 2.0
    play sound "SFX/splash.ogg"
    hide character
    if renpy.has_label(charName+"_ThrownBack"):
        call findLabel("ThrownBack")
    hide character
    with easeinbottom
    $currentCharacter=None
    jump fishing_menu

default fish_responses = [
"[charName] stares at you blankly",
"[charName] thrashes about on the end of your line",
"You're starting to feel kind of sorry for [charName]",
"[charName] opens it's mouth? Maybe to say something romantic?!! Okay nope, it's closed it again",
"[charName] says nothing",
"[charName] is being aloof",
"[charName] blubs",
"[charName] glubs",
"[charName] stares into space",
"[charName] continues the process of perishing slowly",
"[charName] struggles.",
"[charName] almost slips from your hand, the minx!",
"[charName] is either non-sentient or REALLY wants you to stop hitting on them.",
"[charName]'s gills open and close with romanatic intrigue",
"[charName] is actively becoming less wet",
"[charName] is just not into you"
    ]
default fish_pickup = [
        "So... swim here often?",
        "I couldn't help but notice the gleam of your scales",
        "You haven't blinked since you saw me... I often have that effect on people",
        "You'd look great next to some chips",
        "One, two, three four five, once I caught a fish who VIBED",
        "Just thought I'd... drop you a line",
        "You're a great listener",
        "*Wait for [charName] to make the first move*",
        "You seem cold...",
        "I heard their were plenty of fish in the sea but I'll bet none are as hot as you",
        "You're not still part of a school are you? I don't want this to be that kind of dating sim...",
        "How's life?",
        "Lovely weather today",
        "On a scale of one to ten... you have hundreds of scales!",
        "You watch that Bake-Off show?",
        "Did it hurt... When you got a hook through the side of your face??"
    ]


label blubtalk:
    jump blub_menu

label blub_menu:
    $renpy.random.shuffle(fish_pickup)
    menu:
        "[fish_pickup[0]!ti]":
            pass
        "[fish_pickup[1]!ti]":
            pass
        "[fish_pickup[2]!ti]":
            pass
        "End the conversation":
            jump catch_menu
    "[renpy.random.choice(fish_responses)!ti]"
    jump blub_menu





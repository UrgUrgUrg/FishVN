
init python:
    import math
    fishingTimer = 0
    fishDepth = 0
    fishWeight = 400
    fishingX = 960
    fishX = 960
    fishSpeed = 30
    fishLeft = True
    distance = 0
    charName = ""

    class DynamicLine(renpy.Displayable):

        def __init__(self, x1, y1, x2, y2, **kwargs):
            super(DynamicLine, self).__init__(**kwargs)
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            #self.child = renpy.displayable("Minigame/Rod.png")

        def render(self, width, height, st, at):
            r = renpy.Render(1920, 1080)
            s = r.canvas()
            redness = min(255,max(0,(fishDepth/2000)*255))
            greenness = min(255,255*distance)
            c = (redness,greenness,0)
            t = 2 + 2*distance
            s.polygon(c, [(self.x1-t, self.y1),(self.x1+t,self.y1),(self.x2+t,self.y2),(self.x2-t,self.y2)],0)

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
        


transform rodrot:
    transform_anchor True anchor(1.0, 0.0) rotate 0
    function dynamic_rotate
    repeat   

transform slowzoom:
    xysize (500,500)
    ease 3.0 xysize (700,700)
      


screen minigame:
    #variables
    modal True
    default tick = 0
    default reversal = False
    default lineSlack = 200
    default fishEnergy = 100.0
    default correctSide = False
    $fishingX = renpy.get_mouse_pos()[0]
    on "show" action SetVariable("fishingTimer",0)
    on "show" action SetVariable("fishX",renpy.random.randint(900, 1020))
    on "show" action SetVariable("fishDepth",1100)
    #graphics
    on "show" action Play("sound","SFX/HitWater.ogg"), Play("music","Reggae.ogg")
    add DynamicDisplayable(characterCode):
        anchor(0.5,0.2)
        xpos round(fishX)
        ypos round(fishDepth)
        xsize 200
        ysize 200 
    add DynamicLine(fishingX, 5, fishX, fishDepth)
    add "Minigame/Rod.png" xpos fishingX at rodrot
    text "Time: [fishingTimer] \n FishX: [fishX] FishDepth: [fishDepth]\n Tick: [tick] - [reversal]\n Distance: [distance]\n Fishenergy: [fishEnergy] Fish speed: [(fishSpeed+(fishEnergy*0.2))]"
    #gameplay code
    timer 0.5 action SetVariable("fishDepth", fishDepth+1+(fishWeight/200)) repeat True
    button:
        xsize 1920
        ysize 1080
        action SetVariable("fishDepth",fishDepth-max(1,(60-fishEnergy)-(40*(1.0-distance)) )), Play("sound","SFX/reeling.ogg")
    timer 0.05 action SetVariable("distance", (math.dist((fishingX,5),(fishX,5))/1920)*1) repeat True
    timer 0.05 action IncrementVariable("fishingTimer", 1) repeat True
    if reversal:
        timer 0.05 action SetVariable("fishX",fishX-(fishSpeed-(fishEnergy*0.2))) repeat True
    else:
        timer 0.05 action SetVariable("fishX",fishX+(fishSpeed-(fishEnergy*0.2))) repeat True
    timer 0.1 repeat True action If(not reversal, SetScreenVariable("tick", tick + renpy.random.randint(0,6)), SetScreenVariable("tick", tick - renpy.random.randint(0,6)))
    if fishX > 1920:
        timer 0.1 action SetScreenVariable("reversal", True)
    elif fishX < 0:
        timer 0.1 action SetScreenVariable("reversal", False)
    elif tick > 80:
        timer 0.1 action SetScreenVariable("reversal", True)
        ## If our tick is less than 5, including negative number, we will un-resverse the bar and it'll begin to increase again!
    elif tick < 5:
        timer 0.1 action SetScreenVariable("reversal", False)
    if (reversal and (fishX>fishingX)):
        $correctSide=True
    elif ((not reversal) and (fishingX>fishX)):
        $correctSide=True
    else:
        $correctSide=False
    timer 0.1 action If(correctSide,SetScreenVariable("fishEnergy", max(0.0,fishEnergy - (3.0*distance))), SetScreenVariable("fishEnergy", min(100.0,fishEnergy + 0.5))) repeat True
    bar:
        value AnimatedValue(value=fishEnergy, range=100, delay=0.1, old_value=None)
        xysize(1000, 50)
        align (0.5,0.6)
    text "FISH ENERGY: [fishEnergy]%" align(0.5,0.6)
    bar:
        value AnimatedValue(value=fishDepth, range = 2000, delay=0.1, old_value=None)
        bar_vertical True
        bar_invert True
        thumb "Minigame/fish.png"
        align(0.01,0.5)
        ysize 1240
        xsize 40
        bottom_bar Solid("#e70c0c")
    timer 0.5 action If(fishDepth>2000,Show("failGame"),NullAction()) repeat True
    timer 0.5 action If(fishDepth<5,Show("winGame"),NullAction()) repeat True
    

screen failGame:
    ## When this screen is shown, we hide our mini-game, because the player has already failed at this point! Also resets casting flag to False
    on "show" action Hide("minigame")
    on "show" action Stop("sound"), Play("sound","SFX/snap.ogg")
    ## Left click, space, and whatever button player uses to advance game will automatically hide the fail screen.
    ##dismiss action Hide("failGame")
    text "Your line broke!!" size 100 align(0.5, 0.5)
    ## Automatically hides the screen if the player doesn't click within 1.0 second.
    timer 2.0 action Hide("failGame"), Jump("fishingMenu"), Play("music","Bossanova.ogg")

screen winGame:
    ## When this screen is shown, we hide our mini-game, because the player has already failed at this point! Also resets casting flag to False
    on "show" action Hide("minigame")
    on "show" action Stop("sound"), Play("sound","SFX/splash.ogg"),Play("music","victory.ogg"), Queue("music","Bossanova.ogg")
    ## Left click, space, and whatever button player uses to advance game will automatically hide the fail screen.
    ##dismiss action Hide("winGame")
    add DynamicDisplayable(characterCode) at slowzoom:
        size (500, 500)
        align (0.5,0.0)
    text "Thou Hath Caught A Fishy" size 100 align(0.5, 0.5)
    ## Automatically hides the screen if the player doesn't click within 1.0 second.
    timer 3.0 action Hide("winGame"), Jump("caught_character"), Play("music","Bossanova.ogg")


label fishing_start:
    if not datingPoolSet:
        python:
            datingPool=[]
            for c in characters:
                for t in c.lureTraits:
                    for lt in currentLure.traits:
                        print(lt + "compares to "+t)
                        if t==lt:
                            datingPool.append(c)
                            break
            renpy.random.shuffle(datingPool)
            print(datingPool)
            print(datingPool[0].name)
        $datingPoolSet=True
    jump fishing

label fishing:
    play sound "SFX/cast.ogg"
    if (len(datingPool) < 1):
        "You cast your line{w=0.2}.{w=0.2}.{w=0.3}.{w=0.3}.{w=0.4}.\nBut nothing else seems to be biting today."
        $endOfDay=True
        jump fishingMenu
    else:
        python:
            currentCharacter = datingPool.pop()
            print(datingPool[len(datingPool)-1].name)
            fishWeight = currentCharacter.weight
            fishSpeed = max(3,currentCharacter.weight/20)
            charName = currentCharacter.name
        "You cast your line{w=0.2}.{w=0.2}.{w=0.3}.{w=0.3}.{w=0.4}.\nA bite!"
    menu:
        "This catch seems about [currentCharacter.weight] lbs"
        "Reel 'em in!":
            call screen minigame
        "Keep waiting":
            jump fishing
        "End fishing":
            jump fishingMenu


label caught_character:
    $currentCharacter.caughtTimes += 1
    show character at top
    with easeinbottom
    menu:
        "Talk with [charName]":
            $print(charName+"_Catch")
            if (currentCharacter.dateable == True):
                $renpy.call(charName+"_Catch")
                jump end_converstion
            else:
                jump blubtalk
        "Give [charName] a gift" if (currentCharacter.dateable == True):
            $renpy.call(charName+"_AcceptGift")
            "[charName] has accepted your gift"
            $increase_affection(3)
            jump end_converstion
        "Add [charName] to inventory" if not currentCharacter.dateable:
            hide character
            with easeinbottom
            $getFish()
            jump fishingMenu
        "Throw [charName] back":
            play sound "splash.ogg"
            jump end_converstion

label end_converstion:
    hide character
    with easeinbottom
    jump fishingMenu

init:
    $fish_responses = [
"[charName] stares at you blankly",
"[charName] thrashes about on the end of your line",
"You're starting to feel kind of sorry for [charName]",
"[charName] opens it's mouth? Maybe to say something romantic?!! Okay nope, it's closed it again",
"[charName] says nothing",
"[charName] is being aloof",
"[charName] blubs",
"[charName] glubs"
    ]
    $fish_pickup = [
        "So... swim here often?",
        "I couldn't help but notice the gleam of your scales",
        "You haven't blinked since you saw me... I often have that effect on people",
        "You'd look great next to some chips",
        "One, two, three four five, once I caught a fish who VIBED",
        "Just thought I'd... drop you a line",
        "You're a great listener",
        "*Wait for [charName] to make the first move*",
        "You seem cold..."
    ]


label blubtalk:
    show character at top
    with easeinbottom
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
            jump caught_character
    "[renpy.random.choice(fish_responses)!ti]"
    jump blub_menu





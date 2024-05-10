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
    $location="Home"
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
            jump sleep

label sleep:
    stop music fadeout 2.0
    scene black
    with dissolve
    $seconds = 21560
    $endOfDay=False
    $datingPoolSet=False
    $caughtToday=[]
    $dayProgress=0
    $day += 1
    "Zzz"
    play sound "SFX/alarmclock.ogg"
    scene hut
    with dissolve
    jump hut

init:
    $blackMarketUnlocked=False

label town:
    $location="Market"
    play music "market.ogg"
    jump town_menu

init:
    $rememberLure = 0

label fishingMenu:
    scene lake
    with dissolve
    show fishing gear
    with dissolve
    play sound "SFX/setup.ogg"
    call check_time
    show lure at topleft
    with easeinleft
    menu fishing_menu:
        "Select your lure" if not endOfDay:
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
            hide fishing gear
            with dissolve
            $advanceMinutes(20)
            play sound "SFX/closechest.ogg"
            jump lakeside
        "{color=#43f2ff}{size=+20}{b}Start Fishing{/b}{size=-20}" if not endOfDay:
            scene bg water_close
            with dissolve
            jump fishing_start

init:
    $dayProgress = 0

label check_time:
    if seconds < 32400:
        if dayProgress==0:
            if location=="Lake":
                scene bg lakeside
                with dissolve
                "The riverside is tranquil and quiet"
            $dayProgress=1
    elif seconds > 32400:
        if dayProgress==1:
            if location=="Lake":
                scene bg boats
                with dissolve
                "The islander's 9-to-5 is in full swing, but you manage to peel away from the commercial fishing boats that have started dotting the landscape and find a nice secluded spot."
            $dayProgress=2
    elif second > 68400:
        if dayProgress==2:
            if location=="Lake":
                scene bg sunset
                with dissolve
                "You notice the other fishers begin to pack their gear up as the day draws to a close, it will soon be too dark to fish safely."
            $dayProgress=3
    elif second > 75600:
        if dayProgress==3:
            if location=="Lake":
                scene bg night
                with dissolve
                "It's dark. you will be eaten by a grouper..."
            $dayProgress=4
            $endOfDay=True    
    elif second > 82800:
        "You can't keep your eyes open any longer, you decide to head back home and turn in"
        jump sleep
    return

label lakeside:
    $location="Lake"
    play music "Bossanova.ogg"
    call check_time
    if not endOfDay:
        scene bg lakeside
        with dissolve
    menu:
        "Unpack your fishing gear" if not endOfDay:
            $advanceMinutes(20)
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
                    if (lureList[activeButton].price > playersLures.coins):
                        text "$[lureList[activeButton].price:.2f]" size 40 color("#ee1616")
                    else:
                        text "$[lureList[activeButton].price:.2f]" size 40 color("#d0ff28")
                    text "[playerName]'s money: $[playersLures.coins:.2f]" size 20 color("#d0ff28")
    frame align (0.2,0.5) xysize (900,800):
        vbox:                    
            text "Available Lures..."
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


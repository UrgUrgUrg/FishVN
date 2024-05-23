label town_menu:
    scene bg market
    with dissolve
    menu:
        "Around you are several market stalls"
        "Go back home":
            $advanceMinutes(10)
            jump hut
        "Visit {color=#d34036}De Bait Club{/color}":
            jump baitShop
        "Visit {color=#b12d2d}Horse Gifts{/color}":
            jump giftShop
        "Visit {color=#53745d}Jam Maker Inn{/color}" if not blackMarketUnlocked:
            jump jamMaker
        "Visit {color=#5a5858}the black market{/color}" if blackMarketUnlocked:
            jump blackMarket
        "Visit {color=#17f021}Hot Rods{/color}":
            jump rodShop
        "Visit {color=#507888}Roro's Roe Repo{/color}":
            jump fishShop
        "Walk to the lake":
            $advanceMinutes(5)
            jump lakeside


### LURES

init:
    $askforrec=False
    $askedaboutref=False


label baitShop:
    show baitshop at top
    with easeinright
    Baitshop "Welcome to 'De Bait Club'. We'll help you catch the fish of your dreams."
    jump baitshopMenu

label baitshopMenu:
    menu:
        "I'd like to buy a new fishing lure":
            $advanceHours(1)
            Baitshop "Let me show you what we've got in stock!"
            jump buying_a_lure  
        "Can you refund unwanted lures here?" if askedaboutref==False:
            Baitshop "Can you guarantee that the product you have purchased has in no way been submerged in unsterilised liquid, been in contact with unwashed and/or unvaccinated wildlife, been exposed to blood or other bodily secretions or been used in any other way that may compromise said products hygiengic integrity thus rendering it unfit for sale at my store?"
            menu:
                "No...":
                    pass
                "You sort of just described 'using a lure for fishing'":
                    pass
                "Yes!":
                    Baitshop "Very well then - I suppose all you'll have to do is show me your receipt..."
                    menu:
                        "You never gave me a receipt...":
                            Baitshop "Aaaaahhh, tut tut. So you didn't think to ask for a receipt."
                            $askforrec=True
            Baitshop "That's such a shame then. In that case all sales are final. Happy fishing, valued customer!"
            $askedaboutref=True
            jump baitshopMenu
        "*Leave De Bait Club*":
            jump town

label buying_a_lure:
    call screen lure_select(shop=True)
    $chosenLure = baitshopsLures.items[_return]
    if (chosenLure.price > playersLures.coins):
        Baitshop "I'm sorry chile, you need to earn more coin before you can be treating yourself here."
        Baitshop "Maybe try selling some catches to the fish stall?"
        jump baitshopMenu
    else:
        Baitshop "Pleasure doing business with you!"
        $playersLures.addItem(chosenLure)
        $baitshopsLures.items.remove(chosenLure)
        $playersLures.coins -= chosenLure.price
        $baitshopsLures.coins += chosenLure.price
    menu:
        "May I please have a receipt for this purchase?" if askforrec:
            Baitshop "Printer's broken."
            $askforrec=False
            jump baitshopMenu
        "Keep shopping":
            jump buying_a_lure
        "Finish up":
            jump baitshopMenu

### SELLING FISH

init:
    $totalFishValue = 0.0

label fishShop:
    show fishshop
    with easeinright
    Fishshop "Fresh fish! You catch 'em we buy 'em!"
    jump fishshop_menu

label get_total_fish_value(list_used):
    python:
        totalFishValue = 0
        if len(list_used)>0:
            for i in list_used:
                totalFishValue += i.price
        totalFishValue = round(totalFishValue,2)
    return

init:
    $sellQuestion=False

label fishshop_menu:
    call get_total_fish_value(playersLures.fish)
    menu:
        "It's weird, you've bought a lot of fish from me but I never see you SELL any to other villagers." if fishShopPurchases > 2000 and not sellQuestion:
            Fishshop "SELL? Oh goodness no, I eat all these myself!"
            $sellQuestion = true
        "Get a bunch of free fish":
            $playersLures.fish.append(Clownfish)
            $playersLures.fish.append(Banana)
            $playersLures.fish.append(Boot)
            $playersLures.fish.append(Clownfish)
            $playersLures.fish.append(Perch)
            jump fishshop_menu
        "Sell your catches":
            jump fishsellscreen
        "Sell all your catches for $[totalFishValue]" if totalFishValue > 0:
            jump sell_all_fish
        "Leave the stall":
            jump town

init:
    $fishShopPurchases=0.00
    $fishShopResponses=0

label fishshop_afterpurchase:
    play sound "SFX/cash.ogg"
    if (fishShopPurchases<100) and fishShopResponses==0:
        Fishshop "Thank you!"
        $fishShopResponses=1
    elif (fishShopPurchases > 500) and fishShopResponses==1:
        Fishshop "Mmmn, you've brought me an especially slippery batch today!"
        $fishShopPurchases=2
    elif (fishShopPurchases > 1500) and fishShopResponses==2:
        Fishshop "I can't wait until next month when these carcasses have fully matured"
        $fishShopResponses=3
    elif (fishShopPurchases > 2500) and fishShopResponses==3:
        Fishshop "Knife goes in, guts come out..."
        $fishShopPurchases=4
    return


label sell_a_fish(thefish):
    if (thefish==-1):
        jump fishshop_menu
    else:
        $playersLures.coins += playersLures.fish[thefish].price
        $fishShopPurchases += playersLures.fish[thefish].price
        $playersLures.fish.remove(playersLures.fish[thefish])
        call fishshop_afterpurchase
    return


label fishsellscreen:
    call get_total_fish_value(playersLures.fish)
    if playersLures.fish:
        call screen sell_fish(playersLures.fish)
        call sell_a_fish(_return)
        if (playersLures.fish):
            jump fishsellscreen
        else:
            jump fishshop_menu

label sell_all_fish:
    $advanceHours(1)
    $playersLures.coins += totalFishValue
    $fishShopPurchases += totalFishValue
    $playersLures.fish = []
    call fishshop_afterpurchase
    jump town

screen sell_fish(list_used):
    dismiss action Return(-2)
    vbox:
        viewport draggable True mousewheel True xysize(1920,850):
                grid 8 999:
                    align(0.5,0.5)
                    for i, numeral index numeral in enumerate(list_used):
                        $currentFish = list_used[i]
                        button action Return(i):
                            frame:
                                vbox:
                                    add "Characters/JunkFish/[currentFish.name].png":
                                        xysize (200,200)
                                    text "$[currentFish.price:.2f]" align(0.5,0.5)
        hbox xalign 0.5:
            if (list_used==playersLures.fish):
                button action Jump("sell_all_fish") xalign 0.5:
                    frame align (0.5,0.5) padding (10,10):
                        text "Sell all for $[totalFishValue:.2f]" size 60
            button action Return(-1) xalign 0.5:
                frame align (0.5,0.5) padding (10,10):
                    text "Exit" size 60


## BLACKMARKET

label blackMarket:
    jump town

##GIFTS

init python:
    def getDailyGifts():
        renpy.random.shuffle(baseGifts)
        return baseGifts[1:10]

label giftShop:
    show giftShop at top
    with easeinright
    Giftshop "Well howdy, lookin' for that special somethin' for that special someone?"
    Giftshop "This here gift industry's a wild one - so my stock changes purty dang regular. Make sure y'come back daily fir new deals!"
    jump gift_menu

label gift_menu:
    menu:
        "Get all the money":
            $playersLures.coins+=1000000
            jump gift_menu
        "Buy gifts":
            jump buygifts
        "Sell gifts":
            jump sellgifts
        "Leave Horse's Gifts":
            hide giftShop
            with easeoutright
            jump town

label sellgifts:
    call get_total_fish_value(playersLures.gifts)
    call screen sell_fish(playersLures.gifts)
    if (_return==-1):
        jump gift_menu
    else:
        $soldGift = playersLures.gifts[_return]
        Giftshop "It's a shame you and this [soldGift.name] couldn't make things work."
        Giftshop "I'll make sure it finds a good home."
    jump gift_menu

init python:

    def applyBulkDiscount(item,quantity):
        price = item.price
        fullPrice = (price*quantity)
        if quantity>1:
            reduction = max(0,quantity/100)
        else:
            reduction=0
        totalCost = fullPrice - min(fullPrice*0.5, fullPrice*reduction)
        return round(min(fullPrice, totalCost),2)

    def itemsInCart(item,quantity):
        i=0
        aList = []
        while i < quantity:
            aList.append(item)
            i += 1
        return aList


label buygifts:
    call screen gift_select
    if _return!=["horace"]:
        $advanceMinutes(10)
        play sound "SFX/cash.ogg"
        $itemsBought = _return
        $amountBought = len(list(_return))
        $playersLures.gifts.extend(itemsBought)
        $discountedAmount = applyBulkDiscount(itemsBought[0],len(itemsBought))
        $playersLures.coins -= discountedAmount
        $giftshopItems.coins += discountedAmount
        "You bought [amountBought]x [itemsBought[0].name]"
    else:
        jump gift_menu
    jump buygifts

init python:
    def getItemName(itemUsed):
        return n.name

    def countDuplicates(list_used):
        new_list=[]
        for i in set(list_used):
                count = list(list_used).count(i)
                new_list.append([i,count])
        return new_list

screen gift_select(inventoryToUse=giftshopItems.gifts,isGiving=False):
    default inventory = countDuplicates(inventoryToUse)
    default currentHovered = inventory[0][0]
    default currentHovverBovver = inventory[0][0]
    default quantity = 1
    default totalCost = currentHovered.price
    default shoppingCart = []
    default maxQuantity = 99
    dismiss action Return(["horace"])
    hbox align (0.5, 0.5) spacing 10:
        viewport draggable True xysize(600,900) mousewheel True:
            vbox spacing 13:
                for i in list(inventory):
                    $theItem = i[0]
                    $theCount = i[1]
                    if (isGiving):
                        $inStock = "("+str(theCount)+")"
                    else:
                        $inStock=""
                    button action SetScreenVariable("currentHovered", theItem), If(isGiving, SetScreenVariable("maxQuantity",theCount),SetScreenVariable("maxQuantity",100)),SetScreenVariable("quantity",1) hovered SetScreenVariable("currentHovverBovver",theItem):
                        fixed ysize 30:
                            frame xfill True:
                                vbox:
                                    if (currentHovered==theItem):
                                        text "[theItem.name] - $[theItem.price] [inStock]" size 25 color "#dfdc2b"
                                    else:
                                        text "[theItem.name] - $[theItem.price] [inStock]" size 20 color "#fff"
                                    if (currentHovverBovver==theItem):
                                        hbox spacing 3:
                                            for y in list(theItem.traits):
                                                if y==theItem.traits[-1]:
                                                    text "[y]" color "#dfdc2b" size 12
                                                else:
                                                    text "[y]," color "#dfdc2b" size 12
        frame xysize(600,900) padding (35,10):
            vbox:
                text "{u}[currentHovered.name]{/u}" xalign 0.5
                null height 10
                viewport ysize 250 draggable True mousewheel True:
                    text "[currentHovered.description]" size 25
                text "Gift traits:" size 20
                vpgrid cols 3 transpose False ysize 250:
                    for t in list(currentHovered.traits):
                        fixed xsize 150 ysize 20:
                            text "  • [t]" size 20 color "#dfdc2b"
                null height 10
                vbox spacing 15:
                    fixed ysize 40:
                        bar value ScreenVariableValue('quantity',maxQuantity,action=SetScreenVariable('totalCost',applyBulkDiscount(currentHovered,quantity)))
                        if (quantity>3) and (not isGiving):
                            text "{s}{size=12}{color=#d62727}$[currentHovered.price*quantity:.2f]{/color}{/size}{/s} $[totalCost:.2f]" xalign 0.5
                        else:
                            text "$[totalCost:.2f]" xalign 0.5
                    if (quantity>3) and (not isGiving):
                        $perc = 100 - round((totalCost/(currentHovered.price*quantity))*100)
                        if (perc>0):
                            text "Bulk Discount: -[perc]%" size 15 xalign 0.5
                    vbox xalign 0.5:
                        if (totalCost <= playersLures.coins):
                            button action Return(itemsInCart(currentHovered,quantity)) xalign(0.5):
                                frame:
                                    if isGiving:
                                        text "Give x [quantity] [currentHovered.name]"
                                    else:
                                        text "Buy x [quantity] [currentHovered.name]"
                        else:
                            text "Over-budget" color "#d62727"
                        button action Return(["horace"]) xalign 0.5:
                                frame:
                                    text "Exit"
                        





default rodneyfixrod=False

label rodShop:
    show rodShop at top
    with easeinright
    if (rodneyfixrod==False):
        call rodney_fix
    else:
        "Rodney gives you a silent nod as your approach."
    jump rodShop_menu

label rodShop_menu:
    menu:
        "Upgrade your fishing rod":
            call screen rod_shop
            if _return == -1:
                pass
            else:
                $selectedUpgrade = rodShopItems.upgrades[_return]
                $playersLures.coins = playersLures.coins - selectedUpgrade.price
                $rodShopItems.coins = rodShopItems.coins + selectedUpgrade.price
                $playersLures.upgrades.append(selectedUpgrade)
                $rodShopItems.upgrades.remove(selectedUpgrade)
                play sound "SFX/upgrade.ogg"
                "Rodney nods and grabs her tools..{w=0.2}.{w=0.2}.{w=0.2}.{w=0.2}."
                $advanceHours(1)
                play sound "victory.ogg"
                "After an hour or so's wait - you have your new upgrade!"
            jump rodShop_menu
        "Leave":
            show rodShop
            with easeoutright
            jump town

label rodney_fix:
    "The strikingly dressed young woman before you narrows her eyes and beckons for you to hand over your fishing rod."
    menu:
        "Um... Okay":
            "The woman takes your fishing rod in hand and, almost quicker than you can register, dismantles it into more pieces than you'd considered such a simple-looking tool could have."
            "You watch in fascination as she picks up each piece and asseses it, weighing some in her hands, holding a few to her ear.\nIt's as if her and the machinery are having a conversation you can't understand."
            "Seemingly satisfied, the woman puts your rod back together and gives the handle a satisfyingly smooth spin - it doesn't seem like the problem with it jamming is ever going to come back."
            "She hands your rod back to you proudly."
            menu:
                "Thanks":
                    "The woman nods. She then points to a sign that lists the fishing rod upgrades she offers and their prices, you guess that's how she actually make her money."
                "Thanks, um... how much do I owe you?":
                    "The woman shakes her head. Clearly she considers such a simple fix unworthy of payment."
                    "She then points to a sign that lists the fishing rod upgrades she offers and their prices, you guess that's how she does make her money."
            $rodneyfixrod=True
        "*Decline giving it to her*":
            "The woman shrugs and goes back to her tinkering"
    return


screen rod_shop:
    default selectedUpgrade = -1
    frame align (0.5,0.5) xysize (1200,750) padding (20,10):
        hbox xalign 0.5:
            vbox yalign 0.5:
                text "Rodney's Rod Upgrades"
                null height 25
                for i, numeral index numeral in enumerate(rodShopItems.upgrades):
                    button hovered SetScreenVariable("selectedUpgrade", i) action SetScreenVariable("selectedUpgrade",i):
                        if (selectedUpgrade==i):
                            text "[rodShopItems.upgrades[i].name] - {b}$[rodShopItems.upgrades[i].price:.2f]{/b}" color "#ffffff" size 20
                        else:
                            text "[rodShopItems.upgrades[i].name] - $[rodShopItems.upgrades[i].price:.2f]" color "#45f04d" size 20
            vbox:
                add "Interface/rod/RodSpin0.png" align (0.5,0.5) at rod_spinning
                if (selectedUpgrade > -1):
                    viewport xysize(500,75) draggable True mousewheel True:
                        vbox:
                            text "[rodShopItems.upgrades[selectedUpgrade].description]" size 15
                            text "REQUIRES:" size 18
                            for y, numeral index numeral in enumerate(rodShopItems.upgrades[selectedUpgrade].requires):
                                if (rodShopItems.upgrades[selectedUpgrade].requires[y] in list(playersLures.upgrades)):
                                    text "[rodShopItems.upgrades[selectedUpgrade].requires[y].name]" color "#45f04d" size 13
                                else:
                                    text "[rodShopItems.upgrades[selectedUpgrade].requires[y].name]" color "#c70b0b" size 13
                    hbox xalign 0.5:
                        if (playersLures.coins >= rodShopItems.upgrades[selectedUpgrade].price):
                            textbutton "Buy Upgrade" action Return(selectedUpgrade)
                        else:
                            textbutton "Buy Upgrade"
                        textbutton "Exit" action Return(-1)

transform rod_spinning:
    "Interface/rod/RodSpin0.png"
    pause 0.1
    "Interface/rod/RodSpin1.png"
    pause 0.1
    "Interface/rod/RodSpin2.png"
    pause 0.1
    "Interface/rod/RodSpin3.png"
    pause 0.1
    "Interface/rod/RodSpin4.png"
    pause 0.1
    "Interface/rod/RodSpin5.png"
    pause 0.1
    "Interface/rod/RodSpin6.png"
    pause 0.1
    "Interface/rod/RodSpin7.png"
    pause 0.1
    "Interface/rod/RodSpin8.png"
    pause 0.1
    "Interface/rod/RodSpin9.png"
    pause 0.1
    repeat        


    

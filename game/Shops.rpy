label town_menu:
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
    dismiss action Return(-1)
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

label giftShop:
    Giftshop "Well howdy, lookin' for that special somethin' for that special someone?"
    Giftshop "This here gift industry's a wild one - so my stock changes purty dang regular. Make sure y'come back daily fir new deals!"
    jump gift_menu

label gift_menu:
    menu:
        "Buy gifts":
            jump buygifts
        "Sell gifts":
            jump sellgifts
        "Leave Horse's Gifts":
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

label buygifts:
    jump town


    

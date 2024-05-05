# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


image bg lake = "BG/lake.jpg"
image bg hut = "BG/hut.jpg"
image bg market = "BG/market.jpg"

define You = Character("You",color="#ffffff")
define Ara = Character("Ara",color="#a81515")
define Baitshop = Character("Trinika",color="#5878e2")
define mystery = Character("???",color="#a81515")

init python:
    def characterCode(st,at):
        stringo=""
        if currentCharacter.dateable:
            stringo = "Characters/[currentCharacter.name]/[currentCharacter.name]"
        else:
            stringo = "Characters/JunkFish/[currentCharacter.name]"
        if currentStage > 0:
            stringo = stringo + "_" + currentStage
            if currentExpression != "":
                stringo = stringo + "_" + currentExpression
        stringo = stringo + ".png"
        return stringo,None

    def setStage(number):
        currentCharacter.stage=number
        currentStage=number

    def setExpression(string):
        currentExpression=string

    def clearExpression():
        currentExpression=""

    def lureCode(st,at):
        if (currentLure):
            return currentLure.image, None
        else:
            return "Lures/hook.jpg", None
    
    
##time of day system
init -6 python:
    seconds = 21560

    def timeCode(sec):
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        #print("seconds value in hours:",hour)
        #print("seconds value in minutes:",min)
        return "%02d:%02d" % (hour, min)

    def advanceMinutes(mins):
        global seconds
        seconds = seconds + (mins*60)

    def advanceHours(hours):
        global seconds
        seconds = seconds + ((hours*60)*60)



image character = DynamicDisplayable(characterCode)

image lure = DynamicDisplayable(lureCode)

screen clock:
    frame:
        align(1.0,0.0)
        xysize (120,60)
        padding(10,10)
        text "[timeCode(seconds)]"
        timer 1.0 action IncrementVariable("seconds", 1)

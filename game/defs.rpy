# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


image bg lake = "BG/lake.jpg"
image bg hut = "BG/hut.jpg"

define You = Character("You",color="#ffffff")
define Ara = Character("Ara",color="#a81515")
define Baitshop = Character("Master Baits",color="#5878e2")
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

    def lureCode(st,at):
        if (currentLure):
            return currentLure.image, None
        else:
            return "Lures/hook.jpg", None



image character = DynamicDisplayable(characterCode)

image lure = DynamicDisplayable(lureCode)

init python:
    MyCoolFish = Fish("My Cool Fish")
    ####  ^  A super barebones definition of a new character

label My_Cool_Fish_Catch:
    "A cool fish appears"
    npc "Hello, I’m a cool fish"
    return

label My_Cool_Fish_Confession:
    npc "You are finally cool enough to date me, the cool fish."
    return

####  ^  Two examples of some labels that will play at certain events.
####  ^  More fleshed out examples can be found in Character_Template.rpy





























init python:
    characters.remove(MyCoolFish)
    ####  ^  The above code removes this character from the game to give the less cool ones a chance
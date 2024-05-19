init python:
  Barbie = Fish(
    name="Barbie",
    height=5.7,
    weight = 140.03,
    max_affection = 30,
    lureTraits = ["normal"],
    giftTraits = ["alcoholic", "beer"],
    creator="UrgUrgUrg",
    creatorUrl="https://crayondrawlings.neocities.org"
  )

  characters.append(Barbie)

label Barbie_Catch:
  npc "Well g'day!"
  npc "Would you mind nipping to the bottleo and picking me up a couple of tinnies? I'd owe ya!"
  return

label Barbie_Catch_revisit:
  npc "Well g'day!"
  return
  
label Barbie_AcceptGift:
  $setExpression("drinking")
  npc "Nice one, mate! You stayin' with me for a swally?"
  menu:
    "No thanks, you go ahead and enjoy though":
      npc "Too right I will! Cheers!"
      "You pass a pleasant afternoon chatting with Barbie as she downs an impressive amount of alcohol"
    "Sure, I'll have some":
      npc "Ripper!"
      "You two of you share a few cold ones and put the world to rights."
  $advanceHours(3)
  "Eventually  her speech starts to slur and she falls asleep on the riverbank. You gently push her back under the  water before she dries out"
  return
    
default Cheerses = ["Cheers","Hooroo","Up the bum no babies!","Cheers me *hic* dears!","You... you me besht mate, mate...*urp* Might throw up in mo..."]
default cheersnum = 0
    
label Barbie_AcceptGift_revisit:
  $setExpression("drinking")
  npc "[Cheerses[cheersnum]]"
  $cheersnum = cheersnum + 1
  if cheersnum >= len(Cheerses):
    $cheersnum = 0
  $setStage(1)
  return

label Barbie_RejectGift:
  ## Character rejects a gift (it does not contain one of their 'giftTraits')
  npc "Eh, pass."
  return

label Barbie_ThrownBack:
  npc "I'll always come baaaack"
  return


default barbchoices=[]
    
label Barbie_Talk:
  npc "What's on ya mind, mate?"
  menu barb_choices:
    "I thought prawns only turned pink when you cooked them?" if not 'pink' in list(barbchoices):
      npc "I sunburn easily, alright. Don't be such a dag about it."
      $barbchoices.append("pink")
    "Why do you need me to buy you beer? Are you underage?" if not 'underage' in list(barbchoices):
      $setExpression("angry")
      npc "I'm 33 you flaming gallah!"
      npc "Bloody oath, you didn't think the bottleo being on DRY LAND might be more of a barrier to me"
      $clearExpression()
      npc "Underage... strewth... Ugh, I guess it shows you're diligent at least."
      $barbchoices.append("underage")
    "Do I detect an antipodean accent?" if not 'aussue' in list(barbchoices):
      npc "Got me bang to rights, mate. True blue Aussie gal over here."
      npc "Moved out here to get away from the 50 percent booze tax. It just makes  you landos so much less likely to share your tinnies"
      $barbchoices.append("aussie")
    "It's been a pleasure":
      npc "Back at ya, mate."
  return
    
label Barbie_Confession:
  npc "Hey, you know you're really solid right?"
  npc "Not to get all mushy on you but you're my top person to wile away an arvo with. I don't even need to be THAT pissed to find your conversation interesting."
  npc "I'm also, like, MAD horny for ya, just so you know. Fully, fukly down to fool around with you any time. Didn't think land-os were my type but what can I say -  you've turned this shrimp into a bit of a simp..."
  menu:
    "I'd prefer to keep things platonic, but I'd love to see more of you!":
      npc "Fair *urp* Dinkum. We'll be mates sans benefits. Can't say I'm not a little crushed but I'll put on some Divinyls and sort meself out. She'll be right."
    "That sounds great.":
      npc "*Oourp* ripper *uurrp*. Oof..."
      "Barbie winces slightly as the belches rattle of her and gives her rounded stomach a rub"
      npc "Oof... maybe I jumped the gun a little saying 'any time'. I think I hit the carbonation a little too hard... *Blp*."
      npc "But promise me as soon as this bloat goes down you'll jump my exiskeketon, hey?"
      menu:
        "It's a date!":
          npc "Ripper. I'll be seeing you around!"
  return
        
        
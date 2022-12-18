import random

# class for UNO card objects
class Card:
    def __init__(self):
        color = random.choice(("red", "blue", "green", "yellow"))
        actions = ("NUMBER_0", "NUMBER_1", "NUMBER_2", "NUMBER_3", "NUMBER_4", "NUMBER_5", "NUMBER_6", "NUMBER_7", "NUMBER_8", "NUMBER_9", "SKIP", "REVERSE", "DRAW_TWO", "WILD", "WILD_DRAW_FOUR")
        action = (random.choices(actions, weights=(8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 3, 2), k=1))[0]
        if "WILD" in action:
            color = "black"
        self.color = color
        self.action = action

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def draw(self, num_cards):
        for _ in range(num_cards):
            self.hand.append(Card())

    def check_for_cards(self, currentColor, currentAction):
        return [card for card in self.hand if card.color == currentColor or card.action == currentAction or "WILD" in card.action]

    def uno_check(self):
        if len(self.hand) == 1:
            print("%s HAS UNO!" % self.name.upper())

    def win_check(self):
        if len(self.hand) == 0:
            print("%s WINS!" % self.name.upper())
            return False
        else:
            return True

def createPlayers(numPlayers):
    players = []
    for i in range(numPlayers):
        if i == 0:
            name = input("Enter your name: ")
        else:
            name = input("Enter player %s's name: " % str(i+1))
        players.append(Player(name))
    return players

# response to player when using the play command
def playResponse(hand):
    print("YOUR HAND:")
    for count, card in enumerate(hand):
        print("%s: %s | %s" % (count, card.color, card.action))

inApp = True
while inApp: # run until exited
    # probably will rework how handMode works, probably also give it a more accurate name
    handMode = input("---------------------------- \n WELCOME TO UNOCMD! \n P- Play UNOCMD. \n Q- Quit UNOCMD. \n")
    if handMode == "Q":
        print("OK then, hope to see you soon!")
        inApp = False
    else:
        numPlayers = int(input("Enter the number of players: "))
        players = createPlayers(numPlayers)
        for player in players:
            player.draw(7)
        currentCard = startingCard = Card()
        currentColor, currentAction = startingColor, startingAction = startingCard.color, startingCard.action
        if startingColor == "black":
          currentColor = startingColor = random.choice(("red", "blue", "green", "yellow"))
        print("The starting card is... %s %s! \n Play a card with the play command. Type ? for a list of commands." % (startingColor, startingAction))
        isPlaying, currentlyPlaying = True, 0
        direction = 1
        while isPlaying:
            cmd = ""
            if currentlyPlaying == 0:
                cmd = input()
            if cmd == "play":
                if currentlyPlaying != 0:
                    print("WAIT YOUR TURN!")
                else:
                    player = players[currentlyPlaying]
                    nextPlayer = players[(currentlyPlaying + direction) % len(players)]
                    previousPlayer = players[(currentlyPlaying - direction) % len(players)]
                    cardPlaying = None
                    possibleCards = player.check_for_cards(currentColor, currentAction)
                    if possibleCards != []:
                        playResponse(player.hand)
                        select = input("Type the corresponding number to select a card. \n")
                        cardPlaying = player.hand[int(select)]
                    else:
                        while possibleCards == []:
                            player.draw(1)
                            print("You draw a card.")
                            possibleCards = player.check_for_cards(currentColor, currentAction)
                        if possibleCards != []:
                            playResponse(player.hand)
                            select = input("Type the corresponding number to select a card. \n")
                            cardPlaying = player.hand[int(select)]
                    if cardPlaying not in possibleCards:
                        print("CAN'T PLAY! Must be a wild, same color, or same action!")
                    else:
                        if "NUMBER_" not in cardPlaying.action:
                            if cardPlaying.action == "SKIP":
                                print("%s was skipped!" % nextPlayer.name)
                                currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                            if cardPlaying.action == "REVERSE":
                                print("The player order was reversed!")
                                direction = -direction
                                currentlyPlaying = (currentlyPlaying + direction) % len(players)
                            if cardPlaying.action == "DRAW_TWO":
                                nextPlayer.draw(2)
                                print("%s draws two cards!" % nextPlayer.name)
                                currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                            if "WILD" in cardPlaying.action:
                                if len(player.hand) == 1:
                                    print("YOU WIN!")
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentColor = input("What color would you like to change it to? (red/blue/green/yellow) \n")
                                print("The current color is now %s!" % currentColor)
                                if cardPlaying.action == "WILD_DRAW_FOUR":
                                    nextPlayer.draw(4)
                                    print("%s draws four cards!" % nextPlayer.name)
                                    currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                                else:
                                    currentlyPlaying = (currentlyPlaying + direction) % len(players)
                            currentCard, currentAction = cardPlaying, cardPlaying.action
                            if "WILD" not in currentAction:
                                currentColor = currentCard.color
                            player.hand.pop(int(select))
                            player.uno_check()
                            if not player.win_check():
                                for PLAYER in players:
                                    PLAYER.hand = []
                                isPlaying = False
                        else:
                            currentCard, currentColor, currentAction = cardPlaying, cardPlaying.color, cardPlaying.action
                            player.hand.pop(int(select))
                            player.uno_check()
                            if not player.win_check():
                                for PLAYER in players:
                                    PLAYER.hand = []
                                isPlaying = False
                            currentlyPlaying = (currentlyPlaying + direction) % len(players)
                    continue

            if cmd == "?":
                print("?: List of commands \n changes: Game change log  \n info: Info about the current game \n play: Play a card \n exit: Exit game \n UNOCMD v0.02")
            if cmd == "changes":
                print("-reworked some things \n -added capability for having more than 2 players \n -some optimizations \n -added info command functionality")
            if cmd == "info":
                for player in players:
                    print("%s: %s cards." % (player.name, len(player.hand)))
            if cmd == "exit":
                print("Thanks for playing!")
                isPlaying = False
            if currentlyPlaying != 0:
                player = players[currentlyPlaying]
                nextPlayer = players[(currentlyPlaying + direction) % numPlayers]
                previousPlayer = players[(currentlyPlaying - direction) % numPlayers]
                possibleCards = player.check_for_cards(currentColor, currentAction)
                if not possibleCards:
                    while not possibleCards:
                        player.hand.append(Card())
                        print("%s draws a card!" % player.name)
                        possibleCards = player.check_for_cards(currentColor, currentAction)
                else:
                    allTheSame = False
                    wilds = drawtwos = skips = reverses = numbers = []
                    cardActions, actionCardArrays = ["WILD", "DRAW", "SKIP", "REVERSE", "NUMBER"], [wilds, drawtwos, skips, reverses, numbers]
                    for card in possibleCards:
                        cardActionStart = (card.action.split("_"))[0]
                        actionCardArrays[cardActions.index(cardActionStart)].append(card)
                    masterList = [wilds, drawtwos, skips, reverses, numbers]
                    for cardCategory in masterList:
                        if len(cardCategory) == len(possibleCards):
                            allTheSame = True
                    for card in possibleCards:
                        if "WILD" in card.action:
                            reds = blues = greens = yellows = []
                            cardColors, colorCardArrays = ["red", "blue", "green", "yellow"], [reds, blues, greens, yellows]
                            for CARD in player.hand:
                              if CARD.color != "black":
                                colorCardArrays[cardColors.index(CARD.color)].append(CARD)
                            colors = ["red", "blue", "green", "yellow"]
                            amountsOfColors = amountsOfColorsSorted = [len(reds), len(blues), len(greens), len(yellows)]
                            amountsOfColorsSorted.sort()
                            majorityColor = colors[amountsOfColors.index(amountsOfColorsSorted[3])]
                            minorityColor = colors[amountsOfColors.index(amountsOfColorsSorted[0])]
                            if currentColor == minorityColor:
                                if len(player.hand) == 1:
                                    print("%s WON!" % player.name.upper())
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentCard, currentColor, currentAction = card, majorityColor, card.action
                                print("The current color is now %s!" % currentColor)
                                player.hand.remove(card)
                                player.uno_check()
                                if not player.win_check():
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                if currentAction == "WILD_DRAW_FOUR":
                                    nextPlayer.draw(4)
                                    print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                    print("%s draws four cards." % nextPlayer.name)
                                    currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                                else:
                                    print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                    currentlyPlaying = (currentlyPlaying + direction) % len(players)
                                break
                            elif allTheSame:
                                if len(player.hand) == 1:
                                    print("THE OPPONENT WON!")
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentCard, currentColor, currentAction = card, majorityColor, card.action
                                print("The current color is now %s!" % currentColor)
                                player.hand.remove(card)
                                player.uno_check()
                                if not player.win_check():
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                if currentAction == "WILD_DRAW_FOUR":
                                    nextPlayer.draw(4)
                                    print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                    print("%s draws four cards." % nextPlayer.name)
                                    currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                                else:
                                    print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                    currentlyPlaying = (currentlyPlaying + direction) % len(players)
                                break
                        elif "DRAW_TWO" in card.action:
                            if len(player.hand) < 3:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                nextPlayer.draw(2)
                                print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                print("%s draws two cards." % nextPlayer.name)
                                player.hand.remove(card)
                                player.uno_check()
                                if not player.win_check():
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                                break
                            elif allTheSame:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                nextPlayer.draw(2)
                                print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                print("%s draws two cards." % nextPlayer.name)
                                player.hand.remove(card)
                                player.uno_check()
                                if not player.win_check():
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                                break
                        elif "SKIP" in card.action:
                            currentCard, currentColor, currentAction = card, card.color, card.action
                            print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                            print("%s was skipped." % nextPlayer.name)
                            player.hand.remove(card)
                            player.uno_check()
                            if not player.win_check():
                                for PLAYER in players:
                                    PLAYER.hand = []
                                isPlaying = False
                            currentlyPlaying = (currentlyPlaying + (direction * 2)) % len(players)
                            break
                        elif "REVERSE" in card.action:
                            currentCard, currentColor, currentAction = card, card.color, card.action
                            direction = -direction
                            print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                            print("The player order was reversed.")
                            player.hand.remove(card)
                            player.uno_check()
                            if not player.win_check():
                                for PLAYER in players:
                                    PLAYER.hand = []
                                isPlaying = False
                            currentlyPlaying = (currentlyPlaying + direction) % len(players)
                            break
                        else:
                            if allTheSame or possibleCards[len(possibleCards) - 1] == card:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                player.hand.remove(card)
                                player.uno_check()
                                if not player.win_check():
                                    for PLAYER in players:
                                        PLAYER.hand = []
                                    isPlaying = False
                                currentlyPlaying = (currentlyPlaying + direction) % len(players)
                                print("%s plays %s | %s." % (player.name, currentColor, currentAction))
                                break

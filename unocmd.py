import random

# class for UNO card objects
class Card:
    def __init__(self, color, action):
        self.color, self.action = color, action

# choosing a color at random
def randomColor():
    colors = ("red", "blue", "green", "yellow")
    color = random.choice(colors)
    return color

# generates card with color and action, returns UNO card object
def newCard():
    color = randomColor()
    actions = ("NUMBER_0", "NUMBER_1", "NUMBER_2", "NUMBER_3", "NUMBER_4", "NUMBER_5", "NUMBER_6", "NUMBER_7", "NUMBER_8", "NUMBER_9", "SKIP", "REVERSE", "DRAW_TWO", "WILD", "WILD_DRAW_FOUR")
    action = random.choices(actions, weights=(8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 3, 2), k=1)
    action = action[0]
    if action == "WILD" or action == "WILD_DRAW_FOUR":
        color = "black"
    return Card(color, action)

# deals the standard 7 cards
def dealHand():
    playerHand = []
    for i in range(7):
        playerHand.append(newCard())
    return playerHand

# mostly for the draw two and draw four cards
def drawCards(hand, amt):
    for i in range(amt):
        hand.append(newCard())

# finds all the cards in a hand that are playable on a given turn
def checkForCards(hand):
    possibleCards = []
    for card in hand:
        if card.color == currentColor or card.action == currentAction or "WILD" in card.action:
            possibleCards.append(card)
    return possibleCards

# when computer is done making moves, it prints this
# might remove this as a function since it only replaces one line of code with a somewhat shorter line of code
def computerFinishMove():
    print("Opponent plays %s | %s." % (currentColor, currentAction))

# response to player when using the play command
def playResponse(hand):
    print("PLAYER'S HAND:")
    for count, card in enumerate(hand):
        print("%s: %s | %s" % (count, card.color, card.action))

def unoCheck(hand, player):
    if len(hand) == 1:
        if player == "player":
            print("YOU HAVE UNO!")
        else:
            print("THE OPPONENT HAS UNO!")

def winCheck(selfHand, opponentHands, player):
    if len(selfHand) == 0:
        if player == "player":
            print("YOU WIN!")
        else:
            print("THE OPPONENT WON!")
        for hand in opponentHands:
            hand = []
        return False
    else:
        return True

inApp = True
while inApp: # run until exited
    # probably will rework how handMode works, probably also give it a more accurate name
    handMode = input("---------------------------- \n WELCOME TO UNOCMD! \n Players? \n 1. COM v COM | 2. COM v COM v COM \n 3. Player v COM | 4. Player v Com v Com \n Type the corresponding number to select. Alternatively, type 0 to exit. \n")
    if handMode == "0":
        print("OK then, hope to see you soon!")
        inApp = False
    if handMode != "0" and handMode != "3":
        print("This mode has yet to be implemented.")
    if handMode == "3":
        playerHand, opponentHand = dealHand(), dealHand()
        startingCard = newCard()
        startingColor, startingAction = startingCard.color, startingCard.action
        currentCard = startingCard
        currentColor, currentAction = currentCard.color, currentCard.action
        if startingCard.color == "black":
            startingColor = randomColor()
            currentColor = startingColor
        print("The starting card is... %s %s!" % (startingColor, startingCard.action))
        print("Play a card with the play command. Type ? for a list of commands.")
        isPlaying, currentlyPlaying = True, "player"
        while isPlaying:
            cmd = ""
            if currentlyPlaying == "player":
                cmd = input()
            if cmd == "play":
                if currentlyPlaying != "player":
                    print("WAIT YOUR TURN!")
                else:
                    cardPlaying = None
                    possibleCards = checkForCards(playerHand)
                    if possibleCards != []:
                        playResponse(playerHand)
                        select = input("Type the corresponding number to select a card. \n")
                        cardPlaying = playerHand[int(select)]
                    else:
                        while possibleCards == []:
                            playerHand.append(newCard())
                            print("You draw a card.")
                            possibleCards = checkForCards(playerHand)
                        if possibleCards != []:
                            playResponse(playerHand)
                            select = input("Type the corresponding number to select a card. \n")
                            cardPlaying = playerHand[int(select)]
                    if cardPlaying not in possibleCards:
                        print("CAN'T PLAY! Must be a wild, same color, or same action!")
                    else:
                        if "NUMBER_" not in cardPlaying.action:
                            if cardPlaying.action == "SKIP":
                                print("The opponent was skipped!")
                            if cardPlaying.action == "REVERSE":
                                print("The player order was reversed!")
                            if cardPlaying.action == "DRAW_TWO":
                                drawCards(opponentHand, 2)
                                print("The opponent draws two cards!")
                            if "WILD" in cardPlaying.action:
                                if len(playerHand) == 1:
                                    print("YOU WIN!")
                                    opponentHand = []
                                    isPlaying = False
                                currentColor = input("What color would you like to change it to? (red/blue/green/yellow) \n")
                                print("The current color is now %s!" % currentColor)
                                if cardPlaying.action == "WILD_DRAW_FOUR":
                                    drawCards(opponentHand, 4)
                                    print("The opponent draws four cards!")
                                else:
                                    currentlyPlaying = "opponent"
                            currentCard = cardPlaying
                            if "WILD" not in cardPlaying.action:
                                currentColor = currentCard.color
                            currentAction = currentCard.action
                            playerHand.pop(int(select))
                            unoCheck(playerHand, "player")
                            isPlaying = winCheck(playerHand, [opponentHand], "player")
                        else:
                            currentCard = cardPlaying
                            currentColor, currentAction = currentCard.color, currentCard.action
                            playerHand.pop(int(select))
                            unoCheck(playerHand, "player")
                            isPlaying, currentlyPlaying = winCheck(playerHand, [opponentHand], "player"), "opponent"
                    continue

            if cmd == "?":
                print("?: List of commands \n changes: Game change log \n info: Info about the current game \n play: Play a card \n exit: Exit game \n UNOCMD v0.01")
            if cmd == "changes":
                print("-added the change log \n -got AI working \n -added win state \n -first release")
            if cmd == "exit":
                print("Thanks for playing!")
                isPlaying = False
            if currentlyPlaying == "opponent":
                possibleCards = checkForCards(opponentHand)
                if not possibleCards:
                    while not possibleCards:
                        opponentHand.append(newCard())
                        print("Opponent draws a card!")
                        possibleCards = checkForCards(opponentHand)
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
                            for CARD in opponentHand:
                                colorCardArrays[cardColors.index(CARD.color)].append(CARD)
                            colors = ["red", "blue", "green", "yellow"]
                            amountsOfColors = amountsOfColorsSorted = [len(reds), len(blues), len(greens), len(yellows)]
                            amountsOfColorsSorted.sort()
                            majorityColor = colors[amountsOfColors.index(amountsOfColorsSorted[3])]
                            minorityColor = colors[amountsOfColors.index(amountsOfColorsSorted[0])]
                            if currentColor == minorityColor:
                                if len(opponentHand) == 1:
                                    print("THE OPPONENT WON!")
                                    opponentHand = []
                                    isPlaying = False
                                currentCard = card
                                currentColor, currentAction = majorityColor, card.action
                                print("The current color is now %s!" % currentColor)
                                opponentHand.remove(card)
                                unoCheck(opponentHand, "opponent")
                                isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                                if currentAction == "WILD_DRAW_FOUR":
                                    drawCards(playerHand, 4)
                                    print("Sorry, you draw 4 cards.")
                                else:
                                    computerFinishMove()
                                    currentlyPlaying = "player"
                                break
                            elif allTheSame:
                                if len(opponentHand) == 1:
                                    print("THE OPPONENT WON!")
                                    opponentHand = []
                                    isPlaying = False
                                currentCard, currentColor, currentAction = card, majorityColor, card.action
                                print("The current color is now %s!" % currentColor)
                                opponentHand.remove(card)
                                unoCheck(opponentHand, "opponent")
                                isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                                if currentAction == "WILD_DRAW_FOUR":
                                    drawCards(playerHand, 4)
                                    print("Sorry, you draw 4 cards.")
                                else:
                                    computerFinishMove()
                                    currentlyPlaying = "player"
                                break
                        elif "DRAW_TWO" in card.action:
                            if len(playerHand) < 3:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                drawCards(playerHand, 2)
                                print("Sorry, you draw 2 cards.")
                                opponentHand.remove(card)
                                unoCheck(opponentHand, "opponent")
                                isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                                break
                            elif allTheSame:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                drawCards(playerHand, 2)
                                print("Sorry, you draw 2 cards.")
                                opponentHand.remove(card)
                                unoCheck(opponentHand, "opponent")
                                isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                                break
                        elif "SKIP" in card.action:
                            currentCard, currentColor, currentAction = card, card.color, card.action
                            print("Sorry, you were skipped.")
                            opponentHand.remove(card)
                            unoCheck(opponentHand, "opponent")
                            isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                            break
                        elif "REVERSE" in card.action:
                            currentCard, currentColor, currentAction = card, card.color, card.action
                            print("Sorry, the player order was reversed.")
                            opponentHand.remove(card)
                            unoCheck(opponentHand, "opponent")
                            isPlaying = winCheck(opponentHand, [playerHand], "opponent")
                            break
                        else:
                            if allTheSame or possibleCards[len(possibleCards) - 1] == card:
                                currentCard, currentColor, currentAction = card, card.color, card.action
                                opponentHand.remove(card)
                                unoCheck(opponentHand, "opponent")
                                isPlaying, currentlyPlaying = winCheck(opponentHand, [playerHand], "opponent"), "player"
                                computerFinishMove()
                                break

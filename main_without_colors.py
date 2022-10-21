import random
import time
import os

#
#   Python 3.10.7
#   Main script
#   Custom number of Players and type of players
#   Made for fun, feel free to copy and modify
#

cards_stack = ['0.r', '0.g', '0.b', '0.y', '1.r', '1.g', '1.b', '1.y', '2.r', '2.g', '2.b', '2.y', '3.r', '3.g', '3.b', '3.y', '4.r', '4.g', '4.b', '4.y', '5.r', '5.g', '5.b', '5.y', '6.r', '6.g', '6.b', '6.y', '7.r', '7.g', '7.b', 
'7.y', '8.r', '8.g', '8.b', '8.y', '9.r', '9.g', '9.b', '9.y', '+2.r', '+2.g', '+2.b', '+2.y', '+4']
cards_stack_legacy = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '+2', '+4']

# super class to merge same function that players have
class Player():
    def __init__(self, number):
        self.cards = []
        self.cards_raw = []
        self.get_cards(number)

    # X.get_cards(1) gives 1 card to a player
    def get_cards(self, number):
        temp_cards = []
        raw_temp_cards = []
        for eachCard in range(number):
            card = random.choice(cards_stack)
            if len(card) == 3:
                cut = slice(1)
                cardRaw = card
                cardCut = cardRaw[cut]
            elif len(card) == 4:
                cut = slice(2)
                cardCut = card[cut]
            else:
                cardCut = card    
            temp_cards.append(cardCut)
            raw_temp_cards.append(card)
        self.cards = self.cards + temp_cards
        self.cards_raw = self.cards_raw + raw_temp_cards 

    # it should be in HumanPlayer cuz only there it is used
    def show_cards(self):    
        Cards = ' '.join(self.cards_raw)
        return Cards

    # simple delete card from cards
    def delCard(self, move):
        del self.cards[move]
        del self.cards_raw[move]

    # moved it from ComputerPlayer after making it multiplayer
    # prints your move
    def printMove(self, card, Players, nid):
        lenght = len(self.cards)
        lenghtFixed = lenght - 1
        if len(card) == 3:
            cut = slice(1)
        elif len(card) == 4:
            cut = slice(2)
        # it could be shorter if worked more on it    
        print(f'\n{Players[nid].id} {nid} has choosen card {card}. He has {lenghtFixed} more cards!')              

# human player subclass
class HumanPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Human'

    # get move from player, choosing card
    def get_move(self):
        lenght = len(self.cards)
        deck = self.show_cards()
        print(f'\n{deck}')
        move = -1
        while move > lenght - 1 or move < 0: # to get card from your range
            if move == 911:
                break
            elif lenght == 1:
                try:
                    move = int(input('Choose your card (0) | Type 911 to take 1 card => ' ))
                except:
                    pass    
            else:
                try:
                    move = int(input(f'Choose your card (0 - {lenght - 1}) | Type 911 to take 1 card => '))
                except:
                    pass        
        if move == 911:
            self.get_cards(1)
            return move, None
        else:                  
            cardCut = self.cards[move] # can be deleted i guess
            cardRaw = self.cards_raw[move]
            return move, cardRaw

# computer player subclass
class ComputerPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Computer'

    # get move from computer
    def get_move(self):
        lenght = len(self.cards)
        move = random.randint(0, lenght - 1)
        cardRaw = self.cards_raw[move]
        if len(cardRaw) == 3:
            cut = slice(1)
        elif len(cardRaw) == 4:
            cut = slice(2)
        else:
            cut = slice(0)
        cardCut = cardRaw[cut]
        return cardCut, cardRaw, move, lenght, cut      

# game class
class Game():
    def __init__(self, playerStart, numberofplayers):
        self.turn = playerStart
        self.winner = None
        self.cardOnTable = random.choice(cards_stack)
        self.numberofplayers = numberofplayers

    # making next turn and printing spaces
    def nextTurn(self):
        if len(self.cardOnTable) == 3:
            cut = slice(1)
        elif len(self.cardOnTable) == 4:
            cut = slice(2)
        print(f'\nCurrent card on top {self.cardOnTable}')
        print(f'\n----------------------------------------------------------')        
        if self.turn == self.numberofplayers:
            self.turn = 1
            time.sleep(0.7) # to make game more natural; not insta moves
        else:
            self.turn += 1
            time.sleep(0.7) # same here    

    # change card on top; CurrentCard -> ChosenCard
    def changeCard(self, cardRaw, Players):
        NextPlayer = 0
        if self.turn < self.numberofplayers:
            NextPlayer = self.turn
        self.cardOnTable = cardRaw
        if '+4' == cardRaw:
            Players[NextPlayer].get_cards(4)
            print(f'\n{Players[NextPlayer].id} {NextPlayer} got 4 more cards!')
        elif cardRaw == '+2.r' or cardRaw == '+2.y' or cardRaw == '+2.g' or cardRaw == '+2.b':
            Players[NextPlayer].get_cards(2)
            print(f'\n{Players[NextPlayer].id} {NextPlayer} got 2 more cards!')

    # checking if chosen card is valid to place by rules
    def isValid(self, cardRaw, id):
        topCard = self.cardOnTable
        if len(topCard) == 2 or len(cardRaw) == 2 or topCard.endswith('r') and cardRaw.endswith('r') or topCard.endswith('y') and cardRaw.endswith('y')or topCard.endswith('g') and cardRaw.endswith('g') or topCard.endswith('b') and cardRaw.endswith('b') or topCard.startswith('0') and cardRaw.startswith('0') or topCard.startswith('1') and cardRaw.startswith('1') or topCard.startswith('2') and cardRaw.startswith('2') or topCard.startswith('3') and cardRaw.startswith('3') or topCard.startswith('4') and cardRaw.startswith('4') or topCard.startswith('5') and cardRaw.startswith('5') or topCard.startswith('6') and cardRaw.startswith('6') or topCard.startswith('7') and cardRaw.startswith('7') or topCard.startswith('8') and cardRaw.startswith('8') or topCard.startswith('9') and cardRaw.startswith('9') or topCard.startswith('+') and cardRaw.startswith('+'):
            #print('True')
            return 'True'
        else:
            if id == 'Human':
                print(f'Wrong Card!')
            return 'False'       

# made it outside loop for cleaner code
# could be inside game class
def HumanTurn(g, Players, nid, NoHP):
    if NoHP > 1: input(f'\nGive computer to {Players[nid].id} {nid}! Then press ENTER!')
    move, cardRaw = Players[nid].get_move()
    if move == 911:
        if NoHP > 1: os.system('CLS')
        print(f'\n{Players[nid].id} {nid} picked 1 card! He has {len(Players[nid].cards)} cards!')
        g.nextTurn()
    else:
        valid = g.isValid(cardRaw, 'Human')
        while valid == 'False':
            move, cardRaw = Players[nid].get_move()
            if move == 911:
                if NoHP > 1: os.system('CLS')
                print(f'\n{Players[nid].id} picked 1 card! He has {len(Players[nid].cards)} cards!')
                g.nextTurn()
                return
            valid = g.isValid(cardRaw, 'Human')
        if move == 911:
            if NoHP > 1: os.system('CLS')
            print(f'\n{Players[nid].id} {nid} picked 1 card! He has {len(Players[nid].cards)} cards!')
            g.nextTurn()
        if NoHP > 1: os.system('CLS')          
        Players[nid].printMove(cardRaw, Players, nid)
        Players[nid].delCard(move)  
        g.changeCard(cardRaw, Players)
        g.nextTurn()

# same as above
def ComputerTurn(g, Players, nid):
    cardRaw = None
    lenght = len(Players[nid].cards)
    pick = -1
    possiblemoves = []
    for eachCard in range(lenght):
        cardRaw = Players[nid].cards_raw[eachCard]
        check = g.isValid(cardRaw, None)
        if check == 'True':
            possiblemoves.append(eachCard)
    if len(possiblemoves) > 0:
        pick = random.choice(possiblemoves)
        cardRaw = Players[nid].cards_raw[pick]        
        Players[nid].printMove(cardRaw, Players, nid)
        Players[nid].delCard(pick)    
        g.changeCard(cardRaw, Players)
        g.nextTurn()
    else:
        Players[nid].get_cards(1)
        lenghtFixed = lenght + 1
        print(f'\n{Players[nid].id} {nid} picked 1 card! He has {lenghtFixed} cards!')
        g.nextTurn()    

# could be inside Init()
# while loop until winner is settled
def game(Players, NoHP):
    g = Game(1, len(Players))

    g.nextTurn()

    while g.winner == None:
        for i in range(g.numberofplayers):
            if len(Players[i].cards) == 0:
                g.winner = f'{Players[i].id} ' + f'{i}'
                break

        if g.winner != None:
            break    

        if Players[g.turn - 1].id == 'Human':
            HumanTurn(g, Players, g.turn - 1, NoHP)
        elif Players[g.turn - 1].id == 'Computer':
            ComputerTurn(g, Players, g.turn - 1)  

    print(f'{g.winner} has won!')
    yesorno = input('\nWanna play again? Y/N => ')
    if yesorno == 'y' or yesorno == 'Y':
        Init()          

# take players from input and passing it into game()
def Init():
    Players = []
    NumberOfPlayers = 0
    while NumberOfPlayers < 1:
        try:
            NumberOfPlayers = int(input('\nEnter number of players => '))
        except:
            pass
    NumberOfHumanPlayers = -1
    while NumberOfHumanPlayers < 0 and NumberOfHumanPlayers < NumberOfPlayers:
        try:
            NumberOfHumanPlayers = int(input('Enter number of human players => '))
        except:
            pass
    NumberOfComputerPlayers = NumberOfPlayers - NumberOfHumanPlayers
    NumberOfStartingCards = 0
    while NumberOfStartingCards < 1:
        try:
            NumberOfStartingCards = int(input('Enter number of staring cards => '))
        except:
            pass
    for i in range(NumberOfHumanPlayers):
        player = HumanPlayer(NumberOfStartingCards)
        Players.append(player)
    for i in range(NumberOfComputerPlayers):
        player = ComputerPlayer(NumberOfStartingCards)
        Players.append(player)            
    game(Players, NumberOfHumanPlayers)

if __name__ == '__main__':
    Init()
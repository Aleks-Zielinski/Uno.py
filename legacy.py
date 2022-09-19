import random
from colorama import Fore, Style, init
import time
import numpy as np

#
#   Legacy code with only Player vs Computer
#   Made for backup before messing up with custom players
#

cards_stack = ['0.r', '0.g', '0.b', '0.y', '1.r', '1.g', '1.b', '1.y', '2.r', '2.g', '2.b', '2.y', '3.r', '3.g', '3.b', '3.y', '4.r', '4.g', '4.b', '4.y', '5.r', '5.g', '5.b', '5.y', '6.r', '6.g', '6.b', '6.y', '7.r', '7.g', '7.b', 
'7.y', '8.r', '8.g', '8.b', '8.y', '9.r', '9.g', '9.b', '9.y', '+2.r', '+2.g', '+2.b', '+2.y', '+4'] #Change color, return move, block move missing
cards_stack_legacy = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '+2', '+4']

init()
# print(f"{Fore.GREEN}{cards_stack[2]}{Fore.YELLOW} {cards_stack[9]}{Fore.RED} {cards_stack[4]}{Style.RESET_ALL}")
# for test

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.BLUE
grey = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL

class Player():
    def __init__(self, number):
        self.cards = []
        self.cards_raw = []
        self.get_cards(number)

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

    def show_cards(self):
        k = int(len(self.cards_raw))
        #y = np.stack(self.cards)
        j = 0
        for eachCard in self.cards_raw:
            if j < k:
                if len(eachCard) == 3:
                    cut = slice(1)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'  
                    j += 1    
                elif len(eachCard) == 4:
                    cut = slice(2)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'
                    j += 1       
                elif eachCard == '+4':
                    self.cards[j] = f'{grey}{eachCard}{reset}' 
                    j += 1
            else:
                break            
        CardsInColor = ' '.join(self.cards)
        return CardsInColor

    def delCard(self, move):
        del self.cards[move]
        del self.cards_raw[move]         

class HumanPlayer(Player):
    def __init__(self, number):
        super().__init__(number)

    def get_move(self):
        lenght = len(self.cards)
        c = self.show_cards()
        print(c)
        move = -1
        while move > lenght - 1 or move < 0:
            if move == 911:
                break
            elif lenght == 1:
                try:
                    move = int(input('Choose your card (0) | Type 911 to take 1 card -> ' ))
                except:
                    pass    
            else:
                try:
                    move = int(input(f'Choose your card (0 - {lenght - 1}) | Type 911 to take 1 card -> '))
                except:
                    pass        
        if move == 911:
            self.get_cards(1)
            return move, None
        else:                  
            cardCut = self.cards[move]
            cardRaw = self.cards_raw[move]
            return move, cardRaw
        #print(move)   

class ComputerPlayer(Player):
    def __init__(self, number):
        super().__init__(number)

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

    def printComputerMove(self, card):
        lenght = len(self.cards)
        lenghtFixed = lenght - 1
        if len(card) == 3:
            cut = slice(1)
        elif len(card) == 4:
            cut = slice(2)
        if card.endswith('r'):
            print(f'\n{green}Computer{reset} has choosen card {red}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('g'):
            print(f'\n{green}Computer{reset} has choosen card {green}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('y'):
            print(f'\n{green}Computer{reset} has choosen card {yellow}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('b'):
            print(f'\n{green}Computer{reset} has choosen card {blue}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')   
        else:
            print(f'\n{green}Computer{reset} has choosen card {grey}{card}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        #print(card)    
           

class Game():
    def __init__(self, playerStart):
        self.turn = playerStart
        self.winner = None
        self.cardOnTable = random.choice(cards_stack)

    def nextTurn(self):
        if len(self.cardOnTable) == 3:
            cut = slice(1)
        elif len(self.cardOnTable) == 4:
            cut = slice(2)
        if self.cardOnTable.endswith('r'):
            print(f'\nCurrent card on top {red}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('g'):
            print(f'\nCurrent card on top {green}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('y'):
            print(f'\nCurrent card on top {yellow}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('b'):
            print(f'\nCurrent card on top {blue}{self.cardOnTable[cut]}{reset}')
        else:
            print(f'\nCurrent card on top {grey}{self.cardOnTable}{reset}')
        print(f'{yellow}----------------------------------------------------------{reset}')    
        if self.turn == 2:
            self.turn = 1
        elif self.turn == 1:
            time.sleep(0.5)
            self.turn = 2    

    def changeCard(self, cardRaw, player1, player2):
        self.cardOnTable = cardRaw
        if '+4' == cardRaw:
            if self.turn == 2:
                player1.get_cards(4)
                #print('p1+4')
                print(f'\n{green}Human{reset} got {red}4{reset} more cards!')
            else:
                player2.get_cards(4)
                #print('p2+4')
                print(f'\n{green}Computer{reset} got {red}4{reset} more cards!')
        elif cardRaw == '+2.r' or cardRaw == '+2.y' or cardRaw == '+2.g' or cardRaw == '+2.b':
            if self.turn == 2:
                player1.get_cards(2)
                #print('p1+2')
                print(f'\n{green}Human{reset} got {red}2{reset} more cards!')
            else:
                player2.get_cards(2)
                #print('p2+2')
                print(f'\n{green}Computer{reset} got {red}2{reset} more cards!')

    def isValid(self, cardRaw, id):
        topCard = self.cardOnTable
        if len(topCard) == 2 or len(cardRaw) == 2 or topCard.endswith('r') and cardRaw.endswith('r') or topCard.endswith('y') and cardRaw.endswith('y')or topCard.endswith('g') and cardRaw.endswith('g') or topCard.endswith('b') and cardRaw.endswith('b') or topCard.startswith('0') and cardRaw.startswith('0') or topCard.startswith('1') and cardRaw.startswith('1') or topCard.startswith('2') and cardRaw.startswith('2') or topCard.startswith('3') and cardRaw.startswith('3') or topCard.startswith('4') and cardRaw.startswith('4') or topCard.startswith('5') and cardRaw.startswith('5') or topCard.startswith('6') and cardRaw.startswith('6') or topCard.startswith('7') and cardRaw.startswith('7') or topCard.startswith('8') and cardRaw.startswith('8') or topCard.startswith('9') and cardRaw.startswith('9') or topCard.startswith('+') and cardRaw.startswith('+'):
            #print('True')
            return 'True'
        else:
            if id == 'Human':
                print(f'{red}Wrong Card!{reset}')
            return 'False'            

def game():
    player1 = HumanPlayer(5)
    player2 = ComputerPlayer(5)
    g = Game(2)

    g.nextTurn()

    while g.winner == None:
        if len(player1.cards) == 0:
            g.winner = 'Human'
            break
        elif len(player2.cards) == 0:
            g.winner = 'Computer'
            break

        if g.turn == 1:
            move, cardRaw = player1.get_move()
            if move == 911:
                g.nextTurn()
            else:
                valid = g.isValid(cardRaw, 'Human')
                while valid == 'False':
                    move, cardRaw = player1.get_move()
                    if move == 911:
                        break
                    valid = g.isValid(cardRaw, 'Human')
                if move == 911:
                    g.nextTurn()
                    continue        
                player1.delCard(move)  
                g.changeCard(cardRaw, player1, player2)
                g.nextTurn()
        else:
            #cardCut, cardRaw, move, lenght, cut = player2.get_move()
            #print(cardRaw, cut, lenght)
            #print(cardCut, cardRaw)
            cardRaw = None
            lenght = len(player2.cards)
            pick = -1
            possiblemoves = []
            for eachCard in range(lenght):
                #move = random.randint(0, lenght - 1)
                cardRaw = player2.cards_raw[eachCard]
                check = g.isValid(cardRaw, None)
                if check == 'True':
                    possiblemoves.append(eachCard)
            if len(possiblemoves) > 0:
                pick = random.choice(possiblemoves)
                cardRaw = player2.cards_raw[pick]        
                player2.printComputerMove(cardRaw)
                player2.delCard(pick)    
                g.changeCard(cardRaw, player1, player2)
                g.nextTurn()
            else:
                player2.get_cards(1)
                lenghtFixed = lenght + 1
                print(f'{red}Computer picked 1 card!{reset}. He has {red}{lenghtFixed}{reset} cards!')
                g.nextTurn()    
    print(f'{green}{g.winner}{reset} {blue}has{reset} {yellow}won{reset}{red}!{reset}')           

game()

#####################################################################################################################

import random
from colorama import Fore, Style, init
import time
import numpy as np

cards_stack = ['0.r', '0.g', '0.b', '0.y', '1.r', '1.g', '1.b', '1.y', '2.r', '2.g', '2.b', '2.y', '3.r', '3.g', '3.b', '3.y', '4.r', '4.g', '4.b', '4.y', '5.r', '5.g', '5.b', '5.y', '6.r', '6.g', '6.b', '6.y', '7.r', '7.g', '7.b', 
'7.y', '8.r', '8.g', '8.b', '8.y', '9.r', '9.g', '9.b', '9.y', '+2.r', '+2.g', '+2.b', '+2.y', '+4'] #Change color, return move, block move missing
cards_stack_legacy = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '+2', '+4']

init()
# print(f"{Fore.GREEN}{cards_stack[2]}{Fore.YELLOW} {cards_stack[9]}{Fore.RED} {cards_stack[4]}{Style.RESET_ALL}")
# for test

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.BLUE
grey = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL

class Player():
    def __init__(self, number):
        self.cards = []
        self.cards_raw = []
        self.get_cards(number)

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

    def show_cards(self):
        k = int(len(self.cards_raw))
        j = 0
        for eachCard in self.cards_raw:
            if j < k:
                if len(eachCard) == 3:
                    cut = slice(1)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'  
                    j += 1    
                elif len(eachCard) == 4:
                    cut = slice(2)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'
                    j += 1       
                elif eachCard == '+4':
                    self.cards[j] = f'{grey}{eachCard}{reset}' 
                    j += 1
            else:
                break            
        CardsInColor = ' '.join(self.cards)
        return CardsInColor

    def delCard(self, move):
        del self.cards[move]
        del self.cards_raw[move]         

class HumanPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Human'

    def get_move(self):
        lenght = len(self.cards)
        deck = self.show_cards()
        print(f'\n{deck}')
        move = -1
        while move > lenght - 1 or move < 0:
            if move == 911:
                break
            elif lenght == 1:
                try:
                    move = int(input('Choose your card (0) | Type 911 to take 1 card -> ' ))
                except:
                    pass    
            else:
                try:
                    move = int(input(f'Choose your card (0 - {lenght - 1}) | Type 911 to take 1 card -> '))
                except:
                    pass        
        if move == 911:
            self.get_cards(1)
            return move, None
        else:                  
            cardCut = self.cards[move]
            cardRaw = self.cards_raw[move]
            return move, cardRaw
        #print(move)   

class ComputerPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Computer'

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

    def printComputerMove(self, card):
        lenght = len(self.cards)
        lenghtFixed = lenght - 1
        if len(card) == 3:
            cut = slice(1)
        elif len(card) == 4:
            cut = slice(2)
        if card.endswith('r'):
            print(f'\n{green}Computer{reset} has choosen card {red}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('g'):
            print(f'\n{green}Computer{reset} has choosen card {green}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('y'):
            print(f'\n{green}Computer{reset} has choosen card {yellow}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('b'):
            print(f'\n{green}Computer{reset} has choosen card {blue}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')   
        else:
            print(f'\n{green}Computer{reset} has choosen card {grey}{card}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        #print(card)    
           

class Game():
    def __init__(self, playerStart):
        self.turn = playerStart
        self.winner = None
        self.cardOnTable = random.choice(cards_stack)

    def nextTurn(self):
        if len(self.cardOnTable) == 3:
            cut = slice(1)
        elif len(self.cardOnTable) == 4:
            cut = slice(2)
        if self.cardOnTable.endswith('r'):
            print(f'\nCurrent card on top {red}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('g'):
            print(f'\nCurrent card on top {green}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('y'):
            print(f'\nCurrent card on top {yellow}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('b'):
            print(f'\nCurrent card on top {blue}{self.cardOnTable[cut]}{reset}')
        else:
            print(f'\nCurrent card on top {grey}{self.cardOnTable}{reset}')
        print(f'\n{yellow}----------------------------------------------------------{reset}')        
        if self.turn == 2:
            self.turn = 1
        elif self.turn == 1:
            time.sleep(0.7)
            self.turn = 2    

    def changeCard(self, cardRaw, player1, player2):
        self.cardOnTable = cardRaw
        if '+4' == cardRaw:
            if self.turn == 2:
                player1.get_cards(4)
                print(f'\n{green}{player1.id}{reset} got {red}4{reset} more cards!')
            else:
                player2.get_cards(4)
                print(f'\n{green}{player2.id}{reset} got {red}4{reset} more cards!')
        elif cardRaw == '+2.r' or cardRaw == '+2.y' or cardRaw == '+2.g' or cardRaw == '+2.b':
            if self.turn == 2:
                player1.get_cards(2)
                print(f'\n{green}{player1.id}{reset} got {red}2{reset} more cards!')
            else:
                player2.get_cards(2)
                print(f'\n{green}{player2.id}{reset} got {red}2{reset} more cards!')

    def isValid(self, cardRaw, id):
        topCard = self.cardOnTable
        if len(topCard) == 2 or len(cardRaw) == 2 or topCard.endswith('r') and cardRaw.endswith('r') or topCard.endswith('y') and cardRaw.endswith('y')or topCard.endswith('g') and cardRaw.endswith('g') or topCard.endswith('b') and cardRaw.endswith('b') or topCard.startswith('0') and cardRaw.startswith('0') or topCard.startswith('1') and cardRaw.startswith('1') or topCard.startswith('2') and cardRaw.startswith('2') or topCard.startswith('3') and cardRaw.startswith('3') or topCard.startswith('4') and cardRaw.startswith('4') or topCard.startswith('5') and cardRaw.startswith('5') or topCard.startswith('6') and cardRaw.startswith('6') or topCard.startswith('7') and cardRaw.startswith('7') or topCard.startswith('8') and cardRaw.startswith('8') or topCard.startswith('9') and cardRaw.startswith('9') or topCard.startswith('+') and cardRaw.startswith('+'):
            #print('True')
            return 'True'
        else:
            if id == 'Human':
                print(f'{red}Wrong Card!{reset}')
            return 'False'

def HumanTurn(g, player1, player2):
    move, cardRaw = player1.get_move()
    if move == 911:
        print(f'\n{green}Human picked 1 card!{reset}')
        g.nextTurn()
    else:
        valid = g.isValid(cardRaw, 'Human')
        while valid == 'False':
            move, cardRaw = player1.get_move()
            if move == 911:
                print(f'\n{green}Human picked 1 card!{reset}')
                g.nextTurn()
                return
            valid = g.isValid(cardRaw, 'Human')
        if move == 911:
            print(f'\n{green}Human picked 1 card!{reset}')
            g.nextTurn()      
        player1.delCard(move)  
        g.changeCard(cardRaw, player1, player2)
        g.nextTurn()

def ComputerTurn(g, player1, player2):
    cardRaw = None
    lenght = len(player2.cards)
    pick = -1
    possiblemoves = []
    for eachCard in range(lenght):
        cardRaw = player2.cards_raw[eachCard]
        check = g.isValid(cardRaw, None)
        if check == 'True':
            possiblemoves.append(eachCard)
    if len(possiblemoves) > 0:
        pick = random.choice(possiblemoves)
        cardRaw = player2.cards_raw[pick]        
        player2.printComputerMove(cardRaw)
        player2.delCard(pick)    
        g.changeCard(cardRaw, player1, player2)
        g.nextTurn()
    else:
        player2.get_cards(1)
        lenghtFixed = lenght + 1
        print(f'\n{red}Computer picked 1 card!{reset}. He has {red}{lenghtFixed}{reset} cards!')
        g.nextTurn()    

def game():
    player1 = HumanPlayer(5)
    player2 = ComputerPlayer(5)
    g = Game(2)

    g.nextTurn()

    while g.winner == None:
        if len(player1.cards) == 0:
            g.winner = player1.id
            break
        elif len(player2.cards) == 0:
            g.winner = player2.id
            break

        if g.turn == 1 and player1.id == 'Human':
            HumanTurn(g, player1, player2)
        elif g.turn == 1 and player1.id == 'Computer':
            ComputerTurn(g, player1, player2)    
        elif g.turn == 2 and player2.id == 'Human':
            HumanTurn(g, player1, player2)
        elif g.turn == 2 and player2.id == 'Computer':
            ComputerTurn(g, player1, player2)    
    print(f'{green}{g.winner}{reset} {blue}has{reset} {yellow}won{reset}{red}!{reset}')           

game()

# umozliwic customowanie liczby graczy i typ graczy prosto (id playera computera) (input?)
# nowe karty?
# uproscic kod

################################################################################################################################################

import random
from colorama import Fore, Style, init
import time
import os

cards_stack = ['0.r', '0.g', '0.b', '0.y', '1.r', '1.g', '1.b', '1.y', '2.r', '2.g', '2.b', '2.y', '3.r', '3.g', '3.b', '3.y', '4.r', '4.g', '4.b', '4.y', '5.r', '5.g', '5.b', '5.y', '6.r', '6.g', '6.b', '6.y', '7.r', '7.g', '7.b', 
'7.y', '8.r', '8.g', '8.b', '8.y', '9.r', '9.g', '9.b', '9.y', '+2.r', '+2.g', '+2.b', '+2.y', '+4'] #Change color, return move, block move missing
cards_stack_legacy = ['0', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '+2', '+4']

init()
# print(f"{Fore.GREEN}{cards_stack[2]}{Fore.YELLOW} {cards_stack[9]}{Fore.RED} {cards_stack[4]}{Style.RESET_ALL}")
# for test

green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.BLUE
grey = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL

class Player():
    def __init__(self, number):
        self.cards = []
        self.cards_raw = []
        self.get_cards(number)

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

    def show_cards(self):
        k = int(len(self.cards_raw))
        j = 0
        for eachCard in self.cards_raw:
            if j < k:
                if len(eachCard) == 3:
                    cut = slice(1)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'  
                    j += 1    
                elif len(eachCard) == 4:
                    cut = slice(2)
                    cardCut = eachCard[cut]
                    if eachCard.endswith('r'):
                        self.cards[j] = f'{red}{cardCut}{reset}'
                    elif eachCard.endswith('g'):
                        self.cards[j] = f'{green}{cardCut}{reset}'
                    elif eachCard.endswith('y'):
                        self.cards[j] = f'{yellow}{cardCut}{reset}'
                    elif eachCard.endswith('b'):
                        self.cards[j] = f'{blue}{cardCut}{reset}'
                    j += 1       
                elif eachCard == '+4':
                    self.cards[j] = f'{grey}{eachCard}{reset}' 
                    j += 1
            else:
                break            
        CardsInColor = ' '.join(self.cards)
        return CardsInColor

    def delCard(self, move):
        del self.cards[move]
        del self.cards_raw[move]

    def printMove(self, card, Players, nid):
        lenght = len(self.cards)
        lenghtFixed = lenght - 1
        if len(card) == 3:
            cut = slice(1)
        elif len(card) == 4:
            cut = slice(2)
        if card.endswith('r'):
            print(f'\n{green}{Players[nid].id} {nid}{reset} has choosen card {red}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('g'):
            print(f'\n{green}{Players[nid].id} {nid}{reset} has choosen card {green}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('y'):
            print(f'\n{green}{Players[nid].id} {nid}{reset} has choosen card {yellow}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')
        elif card.endswith('b'):
            print(f'\n{green}{Players[nid].id} {nid}{reset} has choosen card {blue}{card[cut]}{reset}. He has {red}{lenghtFixed}{reset} more cards!')   
        else:
            print(f'\n{green}{Players[nid].id} {nid}{reset} has choosen card {grey}{card}{reset}. He has {red}{lenghtFixed}{reset} more cards!')              

class HumanPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Human'

    def get_move(self):
        lenght = len(self.cards)
        deck = self.show_cards()
        print(f'\n{deck}')
        move = -1
        while move > lenght - 1 or move < 0:
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
            cardCut = self.cards[move]
            cardRaw = self.cards_raw[move]
            return move, cardRaw

class ComputerPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        self.id = 'Computer'

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

class Game():
    def __init__(self, playerStart, numberofplayers):
        self.turn = playerStart
        self.winner = None
        self.cardOnTable = random.choice(cards_stack)
        self.numberofplayers = numberofplayers

    def nextTurn(self):
        if len(self.cardOnTable) == 3:
            cut = slice(1)
        elif len(self.cardOnTable) == 4:
            cut = slice(2)
        if self.cardOnTable.endswith('r'):
            print(f'\nCurrent card on top {red}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('g'):
            print(f'\nCurrent card on top {green}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('y'):
            print(f'\nCurrent card on top {yellow}{self.cardOnTable[cut]}{reset}')
        elif self.cardOnTable.endswith('b'):
            print(f'\nCurrent card on top {blue}{self.cardOnTable[cut]}{reset}')
        else:
            print(f'\nCurrent card on top {grey}{self.cardOnTable}{reset}')
        print(f'\n{yellow}----------------------------------------------------------{reset}')        
        if self.turn == self.numberofplayers:
            self.turn = 1
            time.sleep(0.7)
        else:
            self.turn += 1
            time.sleep(0.7)      

    def changeCard(self, cardRaw, Players):
        NextPlayer = 0
        if self.turn < self.numberofplayers:
            NextPlayer = self.turn
        self.cardOnTable = cardRaw
        if '+4' == cardRaw:
            Players[NextPlayer].get_cards(4)
            print(f'\n{green}{Players[NextPlayer].id} {NextPlayer}{reset} got {red}4{reset} more cards!')
        elif cardRaw == '+2.r' or cardRaw == '+2.y' or cardRaw == '+2.g' or cardRaw == '+2.b':
            Players[NextPlayer].get_cards(2)
            print(f'\n{green}{Players[NextPlayer].id} {NextPlayer}{reset} got {red}2{reset} more cards!')

    def isValid(self, cardRaw, id):
        topCard = self.cardOnTable
        if len(topCard) == 2 or len(cardRaw) == 2 or topCard.endswith('r') and cardRaw.endswith('r') or topCard.endswith('y') and cardRaw.endswith('y')or topCard.endswith('g') and cardRaw.endswith('g') or topCard.endswith('b') and cardRaw.endswith('b') or topCard.startswith('0') and cardRaw.startswith('0') or topCard.startswith('1') and cardRaw.startswith('1') or topCard.startswith('2') and cardRaw.startswith('2') or topCard.startswith('3') and cardRaw.startswith('3') or topCard.startswith('4') and cardRaw.startswith('4') or topCard.startswith('5') and cardRaw.startswith('5') or topCard.startswith('6') and cardRaw.startswith('6') or topCard.startswith('7') and cardRaw.startswith('7') or topCard.startswith('8') and cardRaw.startswith('8') or topCard.startswith('9') and cardRaw.startswith('9') or topCard.startswith('+') and cardRaw.startswith('+'):
            #print('True')
            return 'True'
        else:
            if id == 'Human':
                print(f'{red}Wrong Card!{reset}')
            return 'False'       

def HumanTurn(g, Players, nid):
    input(f'\n{red}Give computer to {Players[nid].id} {nid}! Then press ENTER!{reset}')
    move, cardRaw = Players[nid].get_move()
    if move == 911:
        os.system('CLS')
        print(f'\n{green}{Players[nid].id} {nid} picked 1 card!{reset} He has {red}{len(Players[nid].cards)}{reset} cards!')
        g.nextTurn()
    else:
        valid = g.isValid(cardRaw, 'Human')
        while valid == 'False':
            move, cardRaw = Players[nid].get_move()
            if move == 911:
                os.system('CLS')
                print(f'\n{green}{Players[nid].id} picked 1 card!{reset} He has {red}{len(Players[nid].cards)}{reset} cards!')
                g.nextTurn()
                return
            valid = g.isValid(cardRaw, 'Human')
        if move == 911:
            os.system('CLS')
            print(f'\n{green}{Players[nid].id} {nid} picked 1 card!{reset} He has {red}{len(Players[nid].cards)}{reset} cards!')
            g.nextTurn()
        os.system('CLS')          
        Players[nid].printMove(cardRaw, Players, nid)
        Players[nid].delCard(move)  
        g.changeCard(cardRaw, Players)
        g.nextTurn()

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
        print(f'\n{red}{Players[nid].id} {nid} picked 1 card!{reset} He has {red}{lenghtFixed}{reset} cards!')
        g.nextTurn()    

def game(Players):
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
            HumanTurn(g, Players, g.turn - 1)
        elif Players[g.turn - 1].id == 'Computer':
            ComputerTurn(g, Players, g.turn - 1)  

    print(f'{green}{g.winner}{reset} {blue}has{reset} {yellow}won{reset}{red}!{reset}')           

def Init():
    Players = []
    NumberOfPlayers = 0
    while NumberOfPlayers < 1:
        try:
            NumberOfPlayers = int(input('Enter number of players => '))
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
    game(Players)

Init()
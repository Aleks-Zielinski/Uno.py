cardstack = ['1.r', '1.b', '5.r', '3']

#
# Test for adding checking if card is a valid move in game
#

def game():
    mystack = cardstack
    compstack = cardstack
    cardontop = '1'
    while True:
        print(mystack)
        choice = int(input(f'Choose your card '))
        card = mystack[choice]
        print(card)
        if cardontop == card or cardontop.endswith('r') and card.endswith('r') or len(card) == 1 or len(cardontop) == 1:
            print('True')    

game()            
# Mini-project #6 - Blackjack
# Ashutosh Narayan
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (CARD_SIZE[0] / 2, CARD_SIZE[1] / 2)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (CARD_BACK_SIZE[0] /2 , CARD_BACK_SIZE[1] / 2)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# Positions of title and scores
TITLE_POS = (100,40)
SCORE_POS = (480, 30)
MESSAGE_POS = (100,80)
MY_HAND_POS = (60,410)
DEALER_HAND_POS = (60,210)

# initialize some useful global variables
in_play = False
outcome = "Hit or Stand ?"
score = 0
uncover_dealer_card = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, flipped):
        if not flipped:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self,owner):
        #Create Hand object
        self.cards = []
        self.cover_second = False

    def __str__(self):
        # return a string representation of a hand
        s = ''
        for c in self.cards:
            s = s + " " + str(c)
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)
    
    def get_card(self,pos):
        # Given a position, get the rank and suit of card
        return self.cards[pos]
    
    def set_cover_second(self,cover):
        # Cover the second card
        self.cover_second = cover
    
    def second_covered(self):
        return self.cover_second

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
        # counting values of Aces, two Aces can't be counted as 22, so bust
        if self.count_aces == 0:
            return value
        else:
            if value + 10 > 21: # is no Aces
                return value
            else:
                return value + 10 # when one Ace is counted as 1, we need to add 10
    
    def number_of_cards(self):
        # how many cards are there in hand
        number = 0 
        for c in self.cards:
            number += 1
        return number
    
    def busted(self):
        # if hand is busted
        if self.get_value() > 21:
            return True
        else:
            return False
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for c in self.cards:
            if self.cover_second and i == 1:
                c.draw(canvas, [pos[0] + i * (CARD_SIZE[0] + 20), pos[1]], True)
            else:
                c.draw(canvas, [pos[0] + i * (CARD_SIZE[0] + 20), pos[1]], False)
            i += 1
     
    def hit(self,deck):
        # Fetch the card from the end of the Deck and draw it to Hand
        card = deck.deal_card()
        self.add_card(card)
    
    def count_aces(self):
        # count Aces in Hand
        aces = 0
        for c in self.cards:
            if c.get_rank() == 'A':
                aces += 1
        return aces     
 
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit,rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        print "[",
        for c in self.deck:
            print c,
        print "]"
        



#define event handlers for buttons
def deal():
    global in_play, my_hand, dealer_hand, score, deck, outcome
    # your code goes here
    init()
    # clicking DEAL in the middle of the play causes player to loose
    if in_play:
        score -= 1
    #Game in ON
    in_play = True
    # get cards from the deck, each for dealer and player
    my_hand.hit(deck)
    my_hand.hit(deck)
    dealer_hand.hit(deck)
    dealer_hand.hit(deck)
    outcome = "In Play.. Hit or Stand ?"
    dealer_hand.set_cover_second(True)   

def hit():
    # replace with your code below
    global in_play , outcome, score
    # if the hand is in play, hit the player
    if not my_hand.busted() and in_play:
        my_hand.hit(deck)
        if my_hand.busted():
            dealer_hand.set_cover_second(False)
            #Stop the game
            in_play = False
            # if busted, assign a message to outcome, update in_play and score
            outcome = "You have Busted!! DEAL ?"
            score -= 1
       
def stand():
    # replace with your code below
    global outcome, dealer_hand, score, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if not my_hand.busted():
            dealer_hand.set_cover_second(False)
            while dealer_hand.get_value() < 17:
                dealer_hand.hit(deck)
            # if Dealer has busted?
            if dealer_hand.busted():
                outcome = "Dealer busted. You Won.. New DEAL ?"
                score += 1
            else:
                # no body busts, Dealer ties !
                if dealer_hand.get_value() >= my_hand.get_value():
                    outcome = "Dealer Wins! New DEAL ?"
                    score -= 1
                else:
                    outcome = "You won! New DEAL ?"
                    score += 1
            # Stop the game
            in_play = False
            # assign a message to outcome, update in_play and score
        else:
            outcome = "You have already busted. New DEAL ?"
            
    else:
        outcome = "New DEAL ?"


def init():
    global in_play, my_hand, dealer_hand, deck
    deck = Deck()
    my_hand = Hand("player")
    dealer_hand = Hand("dealer")
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BlackJack", TITLE_POS, 36, "Yellow")
    canvas.draw_text("score " + str(score), SCORE_POS, 24, "Black")
    canvas.draw_text(outcome, MESSAGE_POS, 24, "Black")
    canvas.draw_text("Dealer", (60, 200), 24, "Black")
    canvas.draw_text("Player", (60, 400), 24, "Black")
    my_hand.draw(canvas, MY_HAND_POS)
    dealer_hand.draw(canvas, DEALER_HAND_POS)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

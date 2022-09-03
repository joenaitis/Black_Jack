# Simple Blackjack, done as a project for the online course "An Introduction to Interactive Programming in Python"

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
outcome_special = ""

losses = 0
ties = 0
wins = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.list_of_cards = []

    def __str__(self):
        read_out_of_hand = ""
        for i in range(len(self.list_of_cards)):
            read_out_of_hand += " " + str(self.list_of_cards[i])
        return "hand consists of" + read_out_of_hand

    def add_card(self, card):
        self.list_of_cards.append(card)

    def get_value(self):
        hand_value = 0

        for card in self.list_of_cards:
            hand_value += VALUES[card.get_rank()]
        for card in self.list_of_cards:
            if card.get_rank() == 'A':
                if hand_value < 12:
                    hand_value += 10

        return hand_value

    def draw(self, canvas, pos):
        i = 0
        for cards in self.list_of_cards:
            cards.draw(canvas, [pos[0] + CARD_SIZE[0] * i, pos[1]])
            i += 1


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        dealt_card = self.deck.pop(-1)
        return dealt_card

    def __str__(self):
        read_out_of_deck = ""
        for i in range(len(self.deck)):
            read_out_of_deck += " " + str(self.deck[i])
        return "Your deck consists of" + read_out_of_deck


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, losses, outcome_special
    deck = Deck()
    deck.shuffle()

    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    outcome = "You may Hit or Stand."

    if in_play:
        losses += 1
        outcome_special = "You dealt another game too soon and lost."

    #print
    #""
    #print
    #"Dealer %s" % dealer_hand
    #print
    #"Player %s" % player_hand
    #print
    #deck
    in_play = True


def hit():
    global outcome, in_play, deck, player_hand, losses, wins, ties, outcome_special

    outcome_special = ""

    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())

        if player_hand.get_value() > 21:
            in_play = False
            outcome = "You busted."
            losses += 1
    elif not in_play and len(outcome) < 28:
        outcome = "The game is over silly. " + outcome

    #print
    #""
    #print
    #"Dealer %s" % dealer_hand
    #print
    #"Player %s" % player_hand
    #print
    #outcome
    #if not in_play:
        #print
        #"You have " + str(losses) + " losses, " + str(ties) + "ties, and " + str(wins) + " wins."


def stand():
    global outcome, in_play, deck, dealer_hand, player_hand, wins, losses, outcome_special, ties

    outcome_special = ""

    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "The dealer busted. You won."
            in_play = False
            wins += 1
        elif dealer_hand.get_value() < player_hand.get_value():
            outcome = "You beat the dealer."
            in_play = False
            wins += 1
        elif dealer_hand.get_value() == player_hand.get_value():
            outcome = "Tie!"
            in_play = False
            ties += 1
        elif dealer_hand.get_value() > player_hand.get_value():
            outcome = "The dealer beat you."
            in_play = False
            losses += 1
    elif not in_play and len(outcome) < 28:
        outcome = "The game is over silly. " + outcome

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    #print
    #""
    #print
    #"Dealer %s" % dealer_hand
    #print
    #"Player %s" % player_hand
    #print
    #outcome
    #print
    #"You have " + str(losses) + " losses, " + str(ties) + "ties, and " + str(wins) + " wins."


# draw handler
def draw(canvas):
    global in_play

    dealer_pos = [100, 100]
    dealer_hand.draw(canvas, dealer_pos)

    player_pos = [100, 300]
    player_hand.draw(canvas, player_pos)

    canvas.draw_text("Black Jack", [200, 50], 26, 'Black')

    if outcome_special != "":
        canvas.draw_text(outcome_special, [100, 225], 17, 'Black')
    canvas.draw_text(outcome, [100, 255], 17, 'Black')
    if not in_play:
        canvas.draw_text("Would you like to play again?  Click Deal.", [100, 285], 17, 'Black')
    canvas.draw_text(("Wins: " + str(wins)), [100, 450], 17, 'Black')
    canvas.draw_text(("Losses: " + str(losses)), [100, 480], 17, 'Black')
    canvas.draw_text(("Ties: " + str(ties)), [100, 510], 17, 'Black')

    if in_play:
        dealer_first_card_pos = [dealer_pos[0] + .5 * CARD_BACK_SIZE[0], dealer_pos[1] + .5 * CARD_BACK_SIZE[1]]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, dealer_first_card_pos, CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

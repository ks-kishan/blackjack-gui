from random import shuffle
from decimal import Decimal

class Card():
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank

  def __str__(self):
    return f'{self.rank} of {self.suit}'

class Deck():
  def __init__(self):
    self.suits = ['clubs', 'hearts', 'diamonds', 'spades']
    self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    self._deck = []
    self.rebuild_deck()

  def rebuild_deck(self):
    self._deck.clear()
    for rank in self.ranks:
      for suit in self.suits:
        self._deck.append(Card(suit=suit, rank=rank))
    self.shuffle_deck()
  
  def shuffle_deck(self):
    shuffle(self._deck)

  def draw(self):
    if not self._deck:
      raise ValueError('Deck Empty')
    
    return self._deck.pop(-1)
  
  def peek_top(self):
    if not self._deck:
      raise ValueError('Deck Empty')
    
    return self._deck[-1]
  
class Hand():
  def __init__(self):
    self._hand: list[Card] = []
    self.value: int = 0
    self.values = {rank: int(rank) for rank in '23456789'}
    self.values.update({'A': 11, '10': 10, 'J': 10, 'Q': 10, 'K': 10})
    self.reducible_aces = 0
    
  def add(self, card: Card):
    if card.rank == 'A':
      self.reducible_aces += 1
    self._hand.append(card)
    self.value += self.values[card.rank]
    if self.value > 21 and self.reducible_aces > 0:
      self.value -= 10
      self.reducible_aces -= 1

    assert self.value == self.calculate_value()

  def is_blackjack(self):
    return (self.value == 21 and len(self._hand) == 2)

  def is_bust(self):
    return self.value > 21
  
  def calculate_value(self):
    total = 0
    aces = 0
    for card in self._hand:
      total = total + self.values[card.rank]
      if card.rank == 'A':
        aces += 1
    while total > 21 and aces > 0:
      total -= 10
      aces -= 1
    return total

  def __str__(self):
    l = []
    for card in self._hand:
      l.append(str(card))
    return ' ; '.join(l)
  
  def reset(self):
    self._hand.clear()
    self.value = 0
    self.reducible_aces = 0

class Game():
  def __init__(self):
    self.deck = Deck()
    self.player_hand = Hand()
    self.dealer_hand = Hand()
    self.state = 'betting' # player_turn / dealer_turn / round_over / betting
    self.result = None
    self.events = []
    self.balance: Decimal = Decimal('1000')
    self.current_bet: int = 0
    self.minimum_bet: int = 10


  def reset_bankroll(self):
    if self.balance < self.minimum_bet:
      self.balance = Decimal('1000')
      self.events.append('Reset Bankroll')
      return True
    return False

  def place_bet(self, bet: int):
    if self.state != 'betting':
      return
    if bet >= self.minimum_bet and bet <= self.balance:
      self.current_bet = bet
      self.balance -= bet
      return True
    return False
  
  def start_round(self):
    self.events.clear()
    if len(self.deck._deck) < 15:
      self.deck.rebuild_deck()
      self.events.append('deck_reshuffled')
    self.player_hand.reset()
    self.dealer_hand.reset()
    self.state = 'player_turn'
    self.result = None
    self.player_draw()
    self.player_draw()
    self.dealer_draw()
    self.dealer_draw()
    if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
      self.state = 'round_over'

      if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
        self.result = ('push', 'both_blackjack')
        self.balance += self.current_bet
      elif self.player_hand.is_blackjack():
        self.result = ('win', 'blackjack')
        self.balance += (self.current_bet + self.current_bet * Decimal('1.5'))
      elif self.dealer_hand.is_blackjack():
        self.result = ('lose', 'dealer_blackjack')

  def player_draw(self):
    self.player_hand.add(self.deck.draw())

  def dealer_draw(self):
    self.dealer_hand.add(self.deck.draw())

  def player_hit(self):
    if self.state != 'player_turn':
      return
    self.player_draw()
    if self.player_hand.is_bust():
      self.state = 'round_over'
      self.result = ('lose', 'busted')
    
  def player_stand(self):
    if self.state != 'player_turn':
      return
    self.state = 'dealer_turn'
    self.dealer_play()
    self._finalize_result()

  def dealer_play(self):
    if self.state != 'dealer_turn':
      return
    while self.dealer_hand.value < 17:
      self.dealer_draw()

  def _finalize_result(self):
    self.state = 'round_over'

    if self.dealer_hand.is_bust():
      self.result = ('win', 'dealer_busted')
      self.balance += (2 * self.current_bet)
    elif self.player_hand.value > self.dealer_hand.value:
      self.result = ('win', 'high_value')
      self.balance += (2 * self.current_bet)
    elif self.player_hand.value < self.dealer_hand.value:
      self.result = ('lose', 'low_value')
    elif self.player_hand.value == self.dealer_hand.value:
      self.result = ('push', 'equal_value')
      self.balance += self.current_bet

  def get_result(self):
    if self.state != 'round_over':
      return None
    
    return self.result
  
  def get_player_cards(self):
    return self.player_hand._hand

  def get_dealer_cards(self):
    return self.dealer_hand._hand

  def get_deck_length(self):
    return len(self.deck._deck)
  
  def reset_for_bet(self):
    self.state = 'betting'
    self.current_bet = 0
  
  def get_current_balance(self):
    return self.balance

if __name__ == '__main__':

  game = Game()
  print('length of original deck: ', len(game.deck._deck))

  while True:
    print("\n=== New Round ===")
    if game.reset_bankroll():
      print('balance reset to ₹1000')
      print(f'current balance: ₹{game.get_current_balance()}')
    else:
      print(f'current balance: ₹{game.get_current_balance()}')
    while True:
      bet = int(input('Enter bet: ₹'))
      if game.place_bet(bet=bet):
        break
      else:
        print('invalid bet or low balance')
    game.start_round()
    for event in game.events:
      if event == "deck_reshuffled":
        print("Deck reshuffled")
    print(f"Dealer: {game.dealer_hand._hand[0]} ; [Hidden]")
    print(f"Player: {game.player_hand} (value: {game.player_hand.value})")
    print('\nlength of deck', len(game.deck._deck))

    while game.state == 'player_turn':
      move = input('hit or stand (h/s): ')
      if move == 'h':
        game.player_hit()
        print(f"Dealer: {game.dealer_hand._hand[0]} ; [Hidden]")
        print(f"Player: {game.player_hand} (value: {game.player_hand.value})")
      else:
        game.player_stand()

    print(f"Dealer: {game.dealer_hand} (value: {game.dealer_hand.value})")
    print(f"Player: {game.player_hand} (value: {game.player_hand.value})")

    print()
    print(game.get_result())
    print(f'current balance: ₹{game.get_current_balance()}')
    print('\nlength of deck', len(game.deck._deck), '\n')

    if input('play again (y/n)') != 'y':
      break
      

    
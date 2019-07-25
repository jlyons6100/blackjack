# Wove Assignment - 
# Create command line blackjack
# Don't implement surrendering or insurance
from random import shuffle
from collections import defaultdict


class Card():
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
	def __str__(self):
		return self.rank + " of " + self.suit

class Player():
	def __init__(self, player_id):
		self.id = player_id
		self.cash = 1000 # in dollars
		self.hands = []
		self.moves = set() 

	def add_hand(self, bet_amount, optional_card = None):
		new_hand = Hand(bet_amount)
		if optional_card != None:
			new_hand.add_card(optional_card)
		self.hands.append(new_hand)

class Hand():
	def __init__(self, bet_amount):
		self.bet_amount = bet_amount
		self.cards = [] 
		self.score = 0
		self.soft = False # Contains an ace

	def get_score(self):
		if self.soft == True:
			if self.score + 10 <= 21:
				return self.score + 10
		return self.score

	def add_card(self, card): # Cards are (rank, suit) tuples
		self.cards.append(card)
		# rank = card[0]

		self.score += self.get_val_from_rank(card.rank)
		if card.rank == 'Ace':
			self.soft = True

	def delete_card(self, card):
		for ind in range(len(self.cards)):
			hand_card = self.cards[ind]
			if card.rank == hand_card.rank and card.suit == hand_card.suit:
				del  self.cards[ind]
				break
		self.score -= self.get_val_from_rank(card.rank)
		self.soft = False
		for hand_card in self.cards:
			if hand_card.rank == 'Ace':
				self.soft = True

	def get_val_from_rank(self, rank):
 		if rank == 'Jack' or rank == 'Queen' or rank == 'King':
 			return 10
 		elif rank == 'Ace':
 			return 1
 		else:
 			return int(rank)

	def get_move(self, avail_cash): # 1 for Hit, 2 for Stand, 3 for Double, 4 for Split
		moves = '1 for Hit, '+ '2 for Stand' 
		can_split = False
		can_double = False
		card_list = self.cards
		if len(card_list) == 2:
				if avail_cash - self.bet_amount >= 0:
					moves += ', 3 for Double'
					can_double = True
				val1 = self.get_val_from_rank(card_list[0].rank)
				val2 = self.get_val_from_rank(card_list[1].rank)
				if val1 == val2 and avail_cash > 0:
					moves += ', 4 for Split'
					can_split = True
		while True:
			try:
				move_int = int(input("Press " + moves + "\n:"))
				if move_int < 1 or move_int > 4:
					print("Invalid Move, Press " + moves)
				elif move_int == 3 and avail_cash - self.bet_amount < 0:
					print("Invalid Move, not enough money left to double.")
				elif move_int == 3 and can_double == False:
					print("Invalid Move, can only double on first move.")
				elif move_int == 4 and avail_cash == 0:
					print("Invalid Move, not enough money to split.")
				elif move_int == 4 and can_split == False:
					print("Invalid Move, can only split with equal cards.")
				else:
					return move_int
			except:
				print("Invalid Move, Press " + moves)
 
class Game:
	def __init__(self):
		self.players = []
		self.max_cash = defaultdict(int) 
		self.round_eliminated = defaultdict(int)
		self.wins = defaultdict(int) 
		self.losses = defaultdict(int) 
		for player_id in range(self.get_num_players()):
			self.players.append(Player(player_id + 1))
			self.max_cash[player_id + 1] = 1000
		
		self.cards = self.initialize_cards() 
		self.dealer_hand = Hand(0)
		
	def get_num_players(self):
		print()
		self.dash_output("Blackjack")
		while True:
			try:
				n_players = int(input('Enter number of players: '))
				if n_players < 1:
					print("Number of players must be greater than 0!")
				else:
					print()
					return n_players
			except:
				print("Number of players must be an integer!")

	# Initialize deck
	def initialize_cards(self, n_decks = 6): # 6 decks as Vegas Default
		suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
		ranks = ['Ace', '2', '3', '4','5', '6', '7', '8', '9','10','Jack','Queen','King']
		return [Card(rank,suit) for rank in ranks for suit in suits] * n_decks

	# Gets bet for new hand
	def get_bet(self, avail_cash):
		while True:
			try:
				bet_amount = int(input("$"))
				if bet_amount < 1:
					print("Bet amount must be greater than $0!")
				elif bet_amount > avail_cash:
					print("You cannot bet more money than you have!")
				else:			
					return bet_amount
			except:
				print("Bet amount must be an integer!")

	def get_inital_bets(self):
		for player in self.players:
			print('Place bet for Player ' + str(player.id) + ' (Max bet: $ ' + str(player.cash) + ')')
			bet_amount = self.get_bet(player.cash)
			player.add_hand(bet_amount)
			player.cash -= bet_amount

	def handle_dealer_turn(self):
		while((self.dealer_hand.get_score() < 17)): # soft 17 rule for dealer
			self.dealer_hand.add_card(self.cards.pop())
		self.dash_output('Dealer Hand: ' + str([str(card) for card in self.dealer_hand.cards]) + ' (' + str(self.dealer_hand.get_score()) + ')')
		for player in self.players:
			print("Player " + str(player.id) + " Results")
			for hand in player.hands:
				card_list = hand.cards
				print('Hand: ' + str([str(card) for card in card_list]) + ' (' + str(hand.get_score()) + ')')
				if self.dealer_hand.get_score() == 21 and len(self.dealer_hand.cards) == 2:
					if len(card_list) == 2 and hand.get_score() == 21:
						print("Blackjack Push")
						player.cash += (hand.bet_amount)
					else:
						self.losses[player.id] += 1
						print("Dealer Blackjack")
						pass
				elif self.dealer_hand.get_score() == hand.get_score() and hand.score <= 21:
					print("Normal Push")
					player.cash += (hand.bet_amount)
				elif len(card_list) == 2 and hand.get_score() == 21:
					self.wins[player.id] += 1
					print("Blackjack win!")
					player.cash += (int(hand.bet_amount * (3/2)) + int(hand.bet_amount))
				elif hand.get_score() > 21:
					self.losses[player.id] += 1
					print("Bust!")
					pass
				elif self.dealer_hand.get_score() > 21:
					self.wins[player.id] += 1
					print("Dealer bust!")
					player.cash += (hand.bet_amount * 2)
				elif (hand.get_score() < self.dealer_hand.get_score()):
					self.losses[player.id] += 1
					print("Score loss!")
					pass
				elif hand.get_score() > self.dealer_hand.get_score():
					self.wins[player.id] += 1
					print("Score win!")
					player.cash += (hand.bet_amount * 2)

	def handle_player_turn(self, player):
		self.dash_output("Player " + str(player.id) + " Turn")
		hand_i = 0
		while (hand_i < len(player.hands)):
			incr = True
			hand = player.hands[hand_i]
			while(len(hand.cards) < 2):
				hand.add_card(self.cards.pop())
			print("Bet: $" + str(hand.bet_amount))
			while(True):
				card_list = hand.cards
				print('Hand: ' + str([str(card) for card in card_list]) + ' (' + str(hand.get_score()) + ')')
				if hand.get_score() > 21:
					print ("Bust!")
					break
				elif hand.get_score() == 21:
					break
				else:
					move_int = hand.get_move(player.cash) 
					if move_int == 1: # Hit
						hand.add_card(self.cards.pop())
					elif move_int == 2: # Stand
						break
					elif move_int == 3: # Double
						hand.add_card(self.cards.pop())
						player.cash -= hand.bet_amount
						hand.bet_amount += hand.bet_amount
						break
					elif move_int == 4: # Unlimited splits 
						del_card = hand.cards[1]
						hand.delete_card(del_card)
						print("New Hand bet:")
						new_bet = self.get_bet(player.cash)
						player.cash -= new_bet
						player.add_hand(new_bet, del_card)
						incr = False
						break
			if incr == True:
				self.dash_output('Final Hand: ' + str([str(card) for card in card_list]) + ' (' + str(hand.get_score()) + ')')
				hand_i += 1

	def reset(self):
		self.cards = self.initialize_cards()
		ind = 0
		while (ind < len(self.players)):
			player = self.players[ind]
			# Statistics
			if self.max_cash[player.id] < player.cash:
				self.max_cash[player.id] = player.cash
			self.round_eliminated[player.id] += 1 
			# Reset
			player.hands.clear()
			if player.cash < 1:
				del self.players[ind]
			else:
				ind += 1
		self.dealer_hand = Hand(0)

	def play(self):
		# Have to show one of the dealers cards at the beginning
		while(len(self.players) != 0): # Exit condition - all players have gone broke!
			shuffle(self.cards)
			self.get_inital_bets()
			self.dash_output()
			dealer_face_up_card = self.cards.pop()
			self.dealer_hand.add_card(dealer_face_up_card)
			self.dash_output("Dealer face up card: " + str(dealer_face_up_card))
			for player in self.players:
				self.handle_player_turn(player)
			self.handle_dealer_turn()
			self.reset()
			if self.continue_playing() == False or len(self.players) == 0:
				break
		self.dash_output("Thanks for playing!")
		self.dash_output("Statistics:")
		print("Max Cash earned: ")
		for p_id in self.max_cash:
			print( 'Player ' + str(p_id) + ' $' + str(self.max_cash[p_id]) )
		print("Last Round survived: ")
		for p_id in self.round_eliminated:
			print( 'Player ' + str(p_id) + ' Round ' + str(self.round_eliminated[p_id]) )
		print("Hand Win Percentage: ")
		for p_id in self.max_cash:
			percent = 0
			try:
				percent = str( 100 * (self.wins[p_id] / (self.wins[p_id] + self.losses[p_id])) )
			except:
				pass
			print( 'Player ' + str(p_id) + ' %: ' + percent )

	# Exit condition for players to end the game early
	def continue_playing(self):
		self.dash_output('End of round. Enter c to continue / q to quit:')
		while True:
			stop = input()
			if stop.lower() == 'c':
				return True
			elif stop.lower() == 'q':
				return False
			else:
				print("Enter c to continue or q to quit.")

	# Formatted output for better readability
	def dash_output(self, string = ""):
		print(string)
		lenn = len(string) if len(string) != 0 else 20 
		for _ in range(lenn):
			print('-' , end = "")
		print()

myGame = Game()
myGame.play()
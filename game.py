# Wove Assignment - 
# Create command line blackjack
# Don't implement surrendering or insurance
from random import shuffle
class Player():
	def __init__(self, player_id):
		self.id = player_id
		self.cash = 1000 # $ in dollars
		self.hands = []
		self.moves = set() 

	def __str__(self):
		str_id = "Player " + str(self.id) + ' '
		str_hands = "Hands: "
		for hand in self.hands:
			str_hands += (str(hand))
		str_hands += '\n'
		str_cash = "Cash: $" + str(self.cash) + ' '
		str_moves = 'Moves: ' + str(self.moves) + '\n'
		return str_id + str_cash + str_moves + str_hands

	def add_hand(self, bet_amount):
		self.hands.append(Hand(bet_amount))

class Hand():
	def __init__(self, bet_amount):
		self.bet_amount = bet_amount
		self.cards = set()  # Ordering does not matter
		self.score = 0
		self.soft = False # Soft hand contains an ace, which means value can be 1 or 11

	def __str__(self):
		str_bet_amount = '(Bet: $' + str(self.bet_amount) + ' '
		str_score = 'Score: ' + str(self.score) + ' '
		str_cards = str(self.cards) + " "
		str_soft = 'Is soft?: ' + str(self.soft) + ')'
		return str_bet_amount + str_score + str_cards + str_soft

	def add_card(self, card): # Cards are (rank, suit) tuples
		self.cards.add(card)
		rank = card[0]
		self.score += self.get_val_from_rank(rank)
		if rank == 'Ace':
			self.soft = True
	def get_val_from_rank(self, rank):
		if rank == 'Jack' or rank == 'Queen' or rank == 'King':
			return 10
		elif rank == 'Ace':
			return 1
		else:
			return int(rank)

	def get_move(self): # 1 for Hit, 2 for Stand, 3 for double, 4 for split
		moves = '1 - Hit, '+ '2 - Stand' 
		can_split = False
		can_double = False
		card_list = list(self.cards)
		if len(card_list) == 2:
				moves += ', 3 - Double'
				can_double = True
				val1 = self.get_val_from_rank(card_list[0][0])
				val2 = self.get_val_from_rank(card_list[1][0])
				if val1 == val2:
					moves += ', 4 - Split'
					can_split = True
		while True:
			try:
				move_int = int(input("Choose Move(" + moves + ")" + "\n:"))
				if move_int < 1 or move_int > 4:
					print("Invalid Move, choose one of the following: (" + moves + ")")
				elif move_int == 3 and can_double == False:
					print("Invalid Move, can only double on first move.")
				elif move_int == 4 and can_split == False:
					print("Invalid Move, can only split with equal cards.")
				else:
					return move_int
			except:
				print("Invalid Move, choose one of the following: (" + moves + ")")
 
class Game:
	def __init__(self):
		self.players = []
		for player_id in range(self.get_num_players()):
			self.players.append(Player(player_id + 1))
		self.cards = self.initialize_cards() # 6 - 8 decks as Vegas default
		self.dealer_hand = Hand(0)

	def dash_output(self, string = ""):
		print(string)
		lenn = len(string) if len(string) != 0 else 20 
		for _ in range(lenn):
			print('-' , end = "")
		print()

	def get_num_players(self):
		print()
		self.dash_output("Blackjack")
		while True:
			try:
				n_players = int(input('Enter number of players:'))
				if n_players < 1:
					print("Number of players must be greater than 0!")
				else:
					self.dash_output()
					return n_players
					break
			except:
				print("Number of players must be an integer!")

	def initialize_cards(self, n_decks = 1): # should default to 6
		suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
		ranks = ['Ace', '2', '3', '4','5', '6', '7', '8', '9','10','Jack','Queen','King']
		return [(rank,suit) for rank in ranks for suit in suits] * n_decks

	def get_bet(self, player, avail_cash):
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


	def play(self):
		while(len(self.players) != 0):
			shuffle(self.cards)
			for player in self.players:
				self.dash_output('Player ' + str(player.id) + ' place bet. Available cash: $ ' + str(player.cash))
				bet_amount = self.get_bet(player, player.cash)
				player.add_hand(bet_amount)
				player.cash -= bet_amount
			for player in self.players:
				self.dash_output("Player " + str(player.id) + " Hands")
				for hand in player.hands:
					hand.add_card(self.cards.pop())
					hand.add_card(self.cards.pop())
					print("Bet amount: $" + str(hand.bet_amount))
					while(True):
						card_list = list(hand.cards)
						print("Score: " + str(hand.score))
						print("Cards: " + str(card_list))
						if hand.score > 21:
							print ("Bust!")
							break
						elif hand.score == 21 or hand.score == 11 and hand.soft == True:
							print ("Blackjack!")
							break
						else:
							move_int = hand.get_move()
							if move_int == 1: # Hit
								hand.add_card(self.cards.pop())
							elif move_int == 2: # Stand
								break
							elif move_int == 3: # Double
								hand.add_card(self.cards.pop())
								player.cash -= hand.bet_amount
								break
							elif move_int == 4: # Split
								print("HANDLE SPLIT")
								pass
					print("Final Sum " + str(hand.score))
					print("Final Cards " + str(card_list))
			while(self.dealer_hand.score < 17): # HANDLE ACES
				self.dealer_hand.add_card(self.cards.pop())
			print("Dealer score: " + str(self.dealer_hand.score))
			print("Dealer cards: " + str(self.dealer_hand.cards))
			for player in self.players:
				print("Player " + str(player.id) + " Results")
				for hand in player.hands:
					print("Score: " + str(hand.score))
					print("Cards: " + str(card_list))
					# Check these rules for what you get paid
					if self.dealer_hand.score > 21:
						print("Win from dealer bust")
						player.cash += (hand.bet_amount * 2)
					elif hand.score > 21:
						print("Bust!")
						pass
					elif hand.score == self.dealer_hand.score:
						print("Tie!")
						player.cash += hand.bet_amount
					elif hand.score < self.dealer_hand.score:
						print("Loss!")
						pass
					elif hand.score > self.dealer_hand.score:
						print("Win!")
						player.cash += (hand.bet_amount * 2)


			self.cards = self.initialize_cards()
			for player in self.players:
				player.hands.clear()
			self.dealer_hand = Hand(0)
			if self.continue_playing() == False:
				break

			
			# print(self.cards)
		self.dash_output("Thanks for playing!")

	def continue_playing(self):
		print('End of round. Enter c to continue / q to quit')
		while True:
			stop = input()
			if stop.lower() == 'c':
				return True
			elif stop.lower() == 'q':
				return False
			else:
				print("Please enter either c to continue or q to quit")
myGame = Game()
myGame.play()
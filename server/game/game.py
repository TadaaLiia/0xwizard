class WizardGame:
    """
    Implements the Wizard card game logic.
    
    Attributes:
        players (list[str]): List of player names
        current_round (int): Current round number (1-60)
        trump_card (tuple|None): Current trump card as (suit, value) or None
        current_player (str|None): Name of the current player
        scores (dict): Dictionary mapping player names to their total scores
        predictions (dict): Dictionary mapping player names to their round predictions
        hands (dict): Dictionary mapping player names to their current hand of cards
        tricks_won (dict): Dictionary mapping player names to number of tricks won in current round
        current_trick (list): List of cards played in the current trick
        deck (list): List of remaining cards in the deck
    """
    
    SUITS = ['BLUE', 'GREEN', 'RED', 'YELLOW', 'WHITE']  
    VALUES = list(range(1, 14)) + ['WIZARD', 'JESTER']
    
    def __init__(self, players: list[str]):
        """
        Initialize a new game of Wizard.
        
        Args:
            players (list[str]): List of player names
            
        Raises:
            AssertionError: If number of players is not between 3 and 6
        """
        assert 3 <= len(players) <= 6, "Number of players must be between 3 and 6"
        
        self.players = players
        self.current_round = 0
        self.trump_card = None
        self.current_player = None
        self.scores = {player: 0 for player in players}
        self.predictions = {}
        self.hands = {player: [] for player in players}
        self.tricks_won = {player: 0 for player in players}
        self.current_trick = []
        self.deck = self._create_deck()
        
    def _create_deck(self) -> list:
        """
        Create a new deck of cards.
        
        Returns:
            list: List of (suit, value) tuples representing cards
        """
        deck = []
        # Add regular cards
        for suit in self.SUITS[:-1]:  # Exclude Z
            for value in self.VALUES[:-2]:  # Exclude W and J
                deck.append((suit, value))
        
        # Add Wizards and Jesters
        for _ in range(4):
            deck.append(('WHITE', 'WIZARD'))
            deck.append(('WHITE', 'JESTER'))
            
        return deck
    
    def start_round(self):
        """
        Start a new round of the game.
        
        Raises:
            AssertionError: If trying to start more rounds than possible
        """
        self.current_round += 1
        max_rounds = 60 // len(self.players)
        assert self.current_round <= max_rounds, f"Game cannot exceed {max_rounds} rounds"
        
        # Reset round-specific variables
        self.tricks_won = {player: 0 for player in self.players}
        self.predictions = {}
        self.current_trick = []
        self.deck = self._create_deck()
        self.hands = {player: [] for player in self.players}
        
        # Deal cards
        self._deal_cards()
        
        # Set trump card (except in last round)
        if self.current_round < max_rounds:
            self.trump_card = self.deck.pop() if self.deck else None
            
        # Set first player (rotate with each round)
        self.current_player = self.players[(self.current_round - 1) % len(self.players)]
    
    def _deal_cards(self):
        """Deal cards to all players based on the current round number."""
        import random
        random.shuffle(self.deck)
        
        for player in self.players:
            self.hands[player] = [self.deck.pop() for _ in range(self.current_round)]
    
    def make_prediction(self, player: str, tricks: int):
        """
        Record a player's prediction for the current round.
        
        Args:
            player (str): Player making the prediction
            tricks (int): Number of tricks predicted
            
        Raises:
            AssertionError: If invalid player or prediction
        """
        assert player in self.players, "Invalid player"
        assert 0 <= tricks <= self.current_round, "Invalid prediction"
        assert player not in self.predictions, "Player already made a prediction"
        
        self.predictions[player] = tricks
    
    def play_card(self, player: str, card: tuple):
        """
        Play a card from a player's hand.
        
        Args:
            player (str): Player playing the card
            card (tuple): Card to play as (suit, value)
            
        Raises:
            AssertionError: Various validation checks
        """
        assert player == self.current_player, "Not this player's turn"
        assert card in self.hands[player], "Card not in player's hand"
        
        # Validate following suit if possible
        if self.current_trick and card[0] != 'WHITE':  # Not a Wizard/Jester
            lead_suit = self.current_trick[0][0]
            if lead_suit != 'WHITE':  # Lead card isn't a Wizard/Jester
                can_follow = any(c[0] == lead_suit for c in self.hands[player])
                assert not can_follow or card[0] == lead_suit, "Must follow suit if possible"
        
        # Play the card
        self.hands[player].remove(card)
        self.current_trick.append(card)
        
        # If trick is complete, determine winner
        if len(self.current_trick) == len(self.players):
            winner = self._determine_trick_winner()
            self.tricks_won[winner] += 1
            self.current_trick = []
            self.current_player = winner
        else:
            # Move to next player
            next_index = (self.players.index(player) + 1) % len(self.players)
            self.current_player = self.players[next_index]
    
    def _determine_trick_winner(self) -> str:
        """
        Determine the winner of the current trick.
        
        Returns:
            str: Name of the winning player
        """
        lead_card = self.current_trick[0]
        lead_suit = lead_card[0]
        
        # Handle special cases first
        wizards = [(i, card) for i, card in enumerate(self.current_trick) 
                  if card[0] == 'WHITE' and card[1] == 'WIZARD']
        if wizards:
            # First Wizard played wins
            winner_index = wizards[0][0]
            return self.players[winner_index]
        
        # If no Wizards, check if all cards are Jesters
        if all(card[0] == 'WHITE' and card[1] == 'JESTER' for card in self.current_trick):
            # First Jester played wins
            return self.players[0]
        
        # Filter out Jesters and evaluate remaining cards
        valid_cards = [(i, card) for i, card in enumerate(self.current_trick) 
                      if not (card[0] == 'WHITE' and card[1] == 'JESTER')]
        
        # Find highest card of lead suit or trump suit
        winning_card = None
        winning_index = None
        
        for i, card in valid_cards:
            if winning_card is None:
                winning_card = card
                winning_index = i
                continue
                
            # Compare cards
            if card[0] == self.trump_card[0] and winning_card[0] != self.trump_card[0]:
                winning_card = card
                winning_index = i
            elif card[0] == winning_card[0] and card[1] > winning_card[1]:
                winning_card = card
                winning_index = i
                
        return self.players[winning_index]
    
    def calculate_round_scores(self):
        """
        Calculate and update scores for the current round.
        
        Raises:
            AssertionError: If round is not complete
        """
        assert all(len(hand) == 0 for hand in self.hands.values()), "Round not complete"
        
        for player in self.players:
            if self.predictions[player] == self.tricks_won[player]:
                # 20 points for correct prediction plus 10 points per trick
                self.scores[player] += 20 + (10 * self.tricks_won[player])
            else:
                # Subtract 10 points per incorrect trick
                difference = abs(self.predictions[player] - self.tricks_won[player])
                self.scores[player] -= 10 * difference
    
    def get_game_state(self) -> dict:
        """
        Get the current game state.
        
        Returns:
            dict: Current game state including scores, predictions, and current trick
        """
        return {
            'current_round': self.current_round,
            'trump_card': self.trump_card,
            'current_player': self.current_player,
            'scores': self.scores.copy(),
            'predictions': self.predictions.copy(),
            'tricks_won': self.tricks_won.copy(),
            'current_trick': self.current_trick.copy(),
            'hands': {player: hand.copy() for player, hand in self.hands.items()}
        }
    
    def is_round_complete(self) -> bool:
        """
        Check if the current round is complete.
        
        Returns:
            bool: True if round is complete, False otherwise
        """
        return all(len(hand) == 0 for hand in self.hands.values())
    
    def is_game_complete(self) -> bool:
        """
        Check if the game is complete.
        
        Returns:
            bool: True if game is complete, False otherwise
        """
        max_rounds = 60 // len(self.players)
        return self.current_round == max_rounds and self.is_round_complete()
from server.game.game import WizardGame

def main():
    # Get player names
    players = []
    while len(players) < 3 or len(players) > 6:
        try:
            player_count = int(input("Enter number of players (3-6): "))
            if 3 <= player_count <= 6:
                players = [input(f"Enter name for player {i+1}: ") for i in range(player_count)]
            else:
                print("Please enter a number between 3 and 6")
        except ValueError:
            print("Please enter a valid number")
    
    # Create and start game
    game = WizardGame(players)
    
    while not game.is_game_complete():
        game.start_round()
        print(f"\n=== Round {game.current_round} ===")
        print(f"Trump card: {game.trump_card}")
        
        # Get predictions
        for player in players:
            print(f"\n{player}'s hand: {game.hands[player]}")
            while True:
                try:
                    prediction = int(input(f"Enter prediction for {player} (0-{game.current_round}): "))
                    if 0 <= prediction <= game.current_round:
                        game.make_prediction(player, prediction)
                        break
                    else:
                        print(f"Prediction must be between 0 and {game.current_round}")
                except ValueError:
                    print("Please enter a valid number")
                except AssertionError as e:
                    print(f"Error: {e}")
        
        # Play tricks
        while not game.is_round_complete():
            print(f"\nCurrent trick: {game.current_trick}")
            print(f"Current player: {game.current_player}")
            print(f"Your hand: {game.hands[game.current_player]}")
            
            # Get card choice
            while True:
                try:
                    print("Available cards:")
                    for i, card in enumerate(game.hands[game.current_player]):
                        print(f"{i}: {card}")
                    card_index = int(input("Enter card index to play: "))
                    if 0 <= card_index < len(game.hands[game.current_player]):
                        card = game.hands[game.current_player][card_index]
                        game.play_card(game.current_player, card)
                        break
                    else:
                        print("Invalid card index")
                except ValueError:
                    print("Please enter a valid number")
                except AssertionError as e:
                    print(f"Error: {e}")
            
            # Show trick result
            if len(game.current_trick) == len(players):
                print(f"\nTrick complete! Winner: {game.current_player}")
                print(f"Tricks won this round: {game.tricks_won}")
        
        # Score the round
        game.calculate_round_scores()
        print("\n=== Round Complete ===")
        print("Predictions:", game.predictions)
        print("Tricks won:", game.tricks_won)
        print("Current scores:", game.scores)
    
    # Game complete
    print("\n=== Game Complete ===")
    print("Final scores:", game.scores)
    winner = max(game.scores.items(), key=lambda x: x[1])[0]
    print(f"Winner: {winner} with {game.scores[winner]} points!")

if __name__ == "__main__":
    main()
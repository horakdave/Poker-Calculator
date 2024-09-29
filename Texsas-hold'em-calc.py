import tkinter as tk
from treys import Card, Evaluator
import random

evaluator = Evaluator()

def get_deck():
    deck = []
    for rank in '23456789TJQKA':
        for suit in 'cdhs':  # clubs, diamonds, hearts, spades
            deck.append(Card.new(rank + suit))
    return deck

def simulate_hand(player_hand, community_cards, num_players, num_simulations=1000):
    wins = 0
    deck = get_deck()
    player_hand_cards = [Card.new(card) for card in player_hand]
    community_cards_cards = [Card.new(card) for card in community_cards]
    possible_cards = set(deck) - set(player_hand_cards) - set(community_cards_cards)
    possible_cards = list(possible_cards)

    for _ in range(num_simulations):
        random.shuffle(possible_cards)

        # Deal remaining community cards
        num_community_needed = 5 - len(community_cards_cards)
        simulated_community = community_cards_cards + possible_cards[:num_community_needed]
        remaining_deck = possible_cards[num_community_needed:]

        # Deal other players' hands
        opponents_hands = [remaining_deck[i*2:(i+1)*2] for i in range(num_players - 1)]

        # Evaluate hands
        player_score = evaluator.evaluate(player_hand_cards, simulated_community)
        opponents_scores = [evaluator.evaluate(hand, simulated_community) for hand in opponents_hands]

        if all(player_score < opponent_score for opponent_score in opponents_scores):
            wins += 1

    return wins / num_simulations

def run_simulation():
    def format_card(card):
        rank, suit = card[:-1], card[-1]
        if rank == '10':  # Convert '10' to 'T'
            rank = 'T'
        return f"{rank}{suit.lower()}"

    player_hand = [format_card(card.strip()) for card in player_hand_entry.get().split(',')]
    community_cards = [format_card(card.strip()) for card in community_cards_entry.get().split(',')]
    num_players = int(num_players_entry.get())

    win_probability = simulate_hand(player_hand, community_cards, num_players)
    result_label.config(text=f"Estimated probability of winning: {win_probability:.2%}")

root = tk.Tk()
root.title("Poker Odds Calculator")

root.attributes('-topmost', True)

tk.Label(root, text="Your Hand (e.g., AD, 3S):").pack()
player_hand_entry = tk.Entry(root)
player_hand_entry.pack()

tk.Label(root, text="Table Cards (e.g., 4S, 7D, 8D):").pack()
community_cards_entry = tk.Entry(root)
community_cards_entry.pack()

tk.Label(root, text="Number of Players:").pack()
num_players_entry = tk.Entry(root)
num_players_entry.pack()

calculate_button = tk.Button(root, text="Calculate Odds", command=run_simulation)
calculate_button.pack()

result_label = tk.Label(root, text="Estimated probability of winning: ")
result_label.pack()

root.mainloop()
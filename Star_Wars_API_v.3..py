

# 1.Import Statements:
import requests
import random



# 2. Global Variables: 
# Define global variables like urls and any other configurations at the top.
# Define URL for Star Wars API (SWAPI) using a dictionary
urls = {
    "people": {"url": "https://swapi.dev/api/people/", "max_value": 82},
    "planets": {"url": "https://swapi.dev/api/planets/", "max_value": 60},
    "species": {"url": "https://swapi.dev/api/species/", "max_value": 37},
    "starships": {"url": "https://swapi.dev/api/starships/", "max_value": 36},
    "vehicles": {"url": "https://swapi.dev/api/vehicles/", "max_value": 39},
}

# 3. Function Definitions: 
# Define all your functions next. 
# This includes the functions for API requests, comparing stats, 
# Function to retrieve cards from the SWAPI

def cards_category(cards_type):
    url = urls[cards_type]['url']
    cards = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cards.extend(data['results'])
            url = data.get('next')  # Get the next page URL if available
        else:
            print("Failed to retrieve data.")
            return None
    return cards


# Function to compare stats between player's and opponent's cards
def compare_stats(player_card, opponent_card, stat):
    try:
        player_stat = float(player_card[stat].replace(",", ""))
        opponent_stat = float(opponent_card[stat].replace(",", ""))
    except (ValueError, KeyError):
        return 'draw'  # Treat any issue as a draw

    if player_stat > opponent_stat:
        return 'win'
    elif player_stat < opponent_stat:
        return 'lose'
    else:
        return 'draw'



# 5. Game loop to play multiple rounds
def play_game():
    player_score = 0
    opponent_score = 0

    print(
        'Hello there! Welcome to Star Wars Top Trumps. \n'
        'May the Force be with you.'
    )

    while True:
        player_choice = input('What category would you like to choose: planets, starships, vehicles, people, species: ').lower()

        if player_choice not in urls.keys():
            print("Invalid choice. Please select a valid category.")
            continue

        player_cards = cards_category(player_choice)
        if not player_cards:
            print("Failed to retrieve cards. Please try again.")
            continue

        print(f"Always remember, your focus determines your reality. You chose {player_choice}.")
        player_card = random.choice(player_cards)
        print(f"Your card: {player_card['name']}")

        opponent_card = random.choice(player_cards)  # Opponent chooses from the same category
        print(f"Opponent's card: {opponent_card['name']}")

        # Determine the stat to compare based on the category
        if player_choice == 'planets':
            stat = 'population'
        elif player_choice == 'starships':
            stat = 'cargo_capacity'
        elif player_choice == 'vehicles':
            stat = 'length'
        elif player_choice == 'people':
            stat = 'height'
        elif player_choice == 'species':
            stat = 'average_height'

        result = compare_stats(player_card, opponent_card, stat)
        print(result)

        if result == 'win':
            player_score += 1
            print('This is the way. The force is with you! You Win!')
        elif result == 'lose':
            opponent_score += 1
            print('It is a trap! You will never defeat the dark side...You Lose!')
        else:
            print('You cannot stop change any more than you can stop the suns from setting. \nIt is a Draw!')

        # Ask if players want to play another round
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print(f"Final Score: You {player_score}, Opponent {opponent_score}")
            with open("Star_Wars_scores.txt", "a") as text_file:
                text_file.write(f"Player Score: {player_score}, Opponent Score: {opponent_score}\n")
            print("Thank you for playing! May the Force be with you.")
            break

play_game()


































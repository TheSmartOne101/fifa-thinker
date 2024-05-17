import csv
import random
import webbrowser
import time
import sqlite3
from tkinter import Tk, Text, Button, Scrollbar, messagebox

# Define the Player class
class Player:
    def __init__(self, name, full_name, birth_date, age, height_cm, weight_kgs, positions, nationality, overall_rating, potential, value_euro, wage_euro):
        self.name = name
        self.full_name = full_name
        self.birth_date = birth_date
        self.age = age
        self.height_cm = height_cm
        self.weight_kgs = weight_kgs
        self.positions = positions.split(',')
        self.nationality = nationality
        self.overall_rating = int(overall_rating) if overall_rating.isdigit() else 0
        self.potential = potential
        self.value_euro = value_euro
        self.wage_euro = wage_euro

# Function to read player data from a CSV file
def read_players(filename):
    players = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Player(row['name'], row['full_name'], row['birth_date'], row['age'], row['height_cm'], row['weight_kgs'], row['positions'], row['nationality'], row['overall_rating'], row['potential'], row['value_euro'], row['wage_euro'])
            players.append(player)
    return players

# Function to distribute players to two teams
def distribute_players(players, team_size=10):
    random.shuffle(players)
    teams = [players[:team_size], players[team_size:team_size*2]]
    return teams

# Function to calculate the average rating of a team
def calculate_team_rating(team):
    total_rating = sum(player.overall_rating for player in team)
    return total_rating / len(team)

# Function to simulate a match based on team ratings
def simulate_match(team1, team2, text_area):
    team1_score = 0
    team2_score = 0

    team1_rating = calculate_team_rating(team1)
    team2_rating = calculate_team_rating(team2)

    for _ in range(9):
        # Adjust the probabilities based on team ratings
        if random.uniform(0, team1_rating + team2_rating) < team1_rating:
            team1_score += 1
        else:
            team2_score += 1

        text_area.insert('end', f"Spielstand: {team1_score} - {team2_score}\n")
        text_area.see('end')
        text_area.update()
        time.sleep(0.5)

    return team1_score, team2_score

# Function to save the match result to a SQLite database
def save_result_to_db(team1, team2, team1_score, team2_score):
    conn = sqlite3.connect('ergebnisse.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                      (id INTEGER PRIMARY KEY, winner TEXT, loser TEXT, team1_score INTEGER, team2_score INTEGER)''')

    if team1_score > team2_score:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    winner_names = ','.join([player.name for player in winner])
    loser_names = ','.join([player.name for player in loser])

    cursor.execute('INSERT INTO results (winner, loser, team1_score, team2_score) VALUES (?, ?, ?, ?)',
                   (winner_names, loser_names, team1_score, team2_score))

    conn.commit()
    conn.close()

# Function for betting
def bet_on_team(text_area, team1, team2):
    bet = messagebox.askquestion("Wette platzieren", "Möchten Sie auf ein Team wetten?")
    if bet == 'yes':
        team_choice = messagebox.askyesno("Wette platzieren", "Auf welches Team möchten Sie wetten? (Ja für Team 1, Nein für Team 2)")
        chosen_team = team1 if team_choice else team2
        text_area.insert('end', f"Sie haben auf Team {chosen_team[0].name} gewettet.\n")
        return chosen_team
    else:
        text_area.insert('end', "Keine Wette platziert.\n")
        return None

# Main function to execute the program
def main():
    root = Tk()
    root.title("Fußballspiel-Simulator")

    text_area = Text(root, wrap='word', height=20, width=50)
    text_area.pack(side='left', fill='both', expand=True)

    scroll_bar = Scrollbar(root, command=text_area.yview)
    scroll_bar.pack(side='right', fill='y')

    text_area.config(yscrollcommand=scroll_bar.set)

    def play_game():
        text_area.delete('1.0', 'end')
        text_area.insert('end', "Willkommen zum Fußballspiel-Simulator!\n")

        players = read_players('Fifa_Players_2018_reduziert.csv')
        team1, team2 = distribute_players(players)

        text_area.insert('end', "\nTeam 1:\n")
        for player in team1:
            text_area.insert('end', f"  {player.name} ({', '.join(player.positions)})\n")
        text_area.update()
        time.sleep(0.5)

        text_area.insert('end', "\nTeam 2:\n")
        for player in team2:
            text_area.insert('end', f"  {player.name} ({', '.join(player.positions)})\n")
        text_area.update()
        time.sleep(0.5)

        chosen_team = bet_on_team(text_area, team1, team2)

        text_area.insert('end', "\nSpielstand: 0 - 0\n")
        team1_score, team2_score = simulate_match(team1, team2, text_area)
        text_area.insert('end', f"\nEndstand: Team 1, {team1_score} - {team2_score}, Team 2\n")

        # Save match results to the database
        save_result_to_db(team1, team2, team1_score, team2_score)

        if chosen_team:
            if (team1_score > team2_score and chosen_team == team1) or (team1_score < team2_score and chosen_team == team2):
                text_area.insert('end', "Glückwunsch, Sie haben gewonnen!\n")
                webbrowser.open("https://t3.ftcdn.net/jpg/02/82/23/94/360_F_282239447_9JUkxLmUPzBvOrEAXVEx2GpNd1EkPOSO.jpg")
            else:
                text_area.insert('end', "Ups, Sie haben verloren.\n")
                webbrowser.open("https://i1.sndcdn.com/artworks-BBMnwmO6ymZ90v3V-zYlw4g-t500x500.jpg")

        play_again = messagebox.askquestion("Noch eine Runde?", "Möchten Sie noch eine Runde spielen?")
        if play_again == 'yes':
            play_game()
        else:
            text_area.insert('end', "Vielen Dank fürs Spielen! Bis später!\n")

    play_button = Button(root, text='Spiel spielen', command=play_game)
    play_button.pack(side='bottom', pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

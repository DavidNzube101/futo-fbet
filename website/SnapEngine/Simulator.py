import json
import random
import snap_game_engine as SGE

with open("SnapMarket.json", "r") as market_file:
	SnapMarket = json.load(market_file)

def start_game(game, t, market, team1, team2):
	print("Game started!")
	print(f"{game['home_team'][1]} vs {game['away_team'][1]}")
	print(f"0'")
	print("---------------------------------------------------------------------------")
	print(f"|                                 0\t:\t0                                 |")
	print("---------------------------------------------------------------------------")
	SGE.allocate_odds(market, 0, 0, team1, team2, t)
	print("---------------------------------------------------------------------------")
	print("|")
	print("|")
	print("|")
	print(f"{t}'")
	print("---------------------------------------------------------------------------")
	print(f"|                                 {game['home_team_score']}\t:\t{game['away_team_score']}                                 |")
	print("---------------------------------------------------------------------------")
	SGE.allocate_odds(market, game['home_team_score'], game['away_team_score'], team1, team2, t)
	print("---------------------------------------------------------------------------")

with open("SnapTeams/Team1872.json", "r") as team_file:
	Team1872 = json.load(team_file)

with open("SnapTeams/TeamGemini.json", "r") as team_file:
	TeamGemini = json.load(team_file)

with open("SnapTeams/TeamMars.json", "r") as team_file:
	TeamMars = json.load(team_file)

t1 = TeamGemini
t2 = TeamMars

game1 = {	
	"home_team": [t1['name'], t1['abbreviation'], t1['form'], t1['last_five_goals']],
	"away_team": [t2['name'], t2['abbreviation'], t2['form'], t2['last_five_goals']],
	"home_team_score": 5,#random.randrange(1, 5, 1),
	"away_team_score": 1#random.randrange(1, 5, 1)
}

start_game(game1, 74, "1X2", TeamGemini, TeamMars)
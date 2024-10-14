import random
r = ['K', 'I', 'L', 'L']
print(str(r).replace(", ", "").replace("[", "").replace("]", "").replace("'", ""))
print("3".upper())


def factorial(num):
	if num == 0:
		return 1
	else:
		return num * factorial(num - 1)

def avgGoals(goal_list):
	return sum(goal_list) / len(goal_list)

def p(y, k):
	e = 2.718
	return ((e * (0 - y)) * (y * k)) / factorial(k)

t1 = 2# random.randrange(1, 5, 1)
t2 = random.randrange(1, 5, 1)

p1 = p(avgGoals([4, 2, 1, 0, 0, 3, 1]), t1)
p2 = p(avgGoals([1, 2, 2, 2, 2, 1, 2]), t2)
print(p1, p2)

# p(k) = (e^(-y) * (y^k)) / k!

# p(k) = probability of k goals scored
# y = average rate of goals scored
# e = 2.718(natural logarithm)
# k = number of goals scored



















































































































































































import random

game = {	
	"home_team": ["CSC", "WWWWW"],
	"away_team": ["SOE", "WWWWW"],
	"home_team_score": 1,
	"away_team_score": 2,
	"market" : {
		"1X2": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"1X2 2UP": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"Over/Under": {
			"Over": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			},
			"Under": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			}
		},
		"Asian Over/Under": {
			"Over": {
				2: 0.0,
				3: 0.0,
				4: 0.0,
				5: 0.0,
				6: 0.0,
			},
			"Under": {
				2: 0.0,
				3: 0.0,
				4: 0.0,
				5: 0.0,
				6: 0.0,
			}
		},
		"Double Chance": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"First Goal": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"Home Over/Under": {
			"Over": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			},
			"Under": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			}
		},
		"Away Over/Under": {
			"Over": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			},
			"Under": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			}
		},
		"GG/NG": {
			"Yes": 0.0,
			"No": 0.0
		},
		"GG/NG 2+": {
			"Yes": 0.0,
			"No": 0.0
		},
		"1st Half 1X2": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"1st Half Over/Under": {
			"Over": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			},
			"Under": {
				0.5: 0.0,
				1.5: 0.0,
				2.5: 0.0,
				3.5: 0.0,
				4.5: 0.0,
				5.5: 0.0,
			}
		},
		"1st Half Double Chance": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		},
		"1st Half First Goal": {
			"Home": 0.0,
			"Away": 0.0,
			"Draw": 0.0,
		}
	}
}
numbers = []
for i in range(3):
	numbers.append(i)

def getOdds(ht_form, at_form):
	def getFormPoints(form):
		_bucket = []
		form_point = 0
		for game_outcome in form:
			_bucket.append(game_outcome)

		for game_outcome in _bucket:
			if "W" == game_outcome:
				form_point = form_point + 1
			elif "D" == game_outcome:
				form_point = form_point + 0.5
			elif "L" == game_outcome:
				form_point = form_point + 0

		return form_point

	def getFormCount(form):
		_bucket = []
		form_point = 0
		for game_outcome in form:
			_bucket.append(game_outcome)

		W = 0
		D = 0
		L = 0

		for game_outcome in _bucket:
			if "W" == game_outcome:
				W = W + 1
			elif "D" == game_outcome:
				D = D + 1
			elif "L" == game_outcome:
				L = L + 1

		return [W, D, L]

	ht_form_point = getFormPoints(ht_form)
	at_form_point = getFormPoints(at_form)

	def getTeamsOdds(team_form_point):
		_ = []
		n1 = random.randrange(30, 50, 7)
		n2 = random.randrange(51, 70, 7)
		for n in range(10):
			_.append(float(random.randrange(n1, n2, 1)))

		if team_form_point >= 3.5 and team_form_point <= 5:
			odd = float(random.randrange(1, 2, 1)) + (team_form_point / random.choice(_))
		elif team_form_point >= 2 and team_form_point < 3.5:
			odd = float(random.randrange(2, 5, 1)) + (team_form_point / random.choice(_))
		elif team_form_point >= 0 and team_form_point < 2:
			odd = float(random.randrange(10, 20, 2))

		return round(odd, 2)

	total_draw_count = getFormCount(ht_form)[1] + getFormCount(at_form)[1]

	return [getTeamsOdds(ht_form_point), getTeamsOdds(total_draw_count), getTeamsOdds(at_form_point)] # Home To Win, Draw Game, Away To Win

def updateOdds(ht_goal, at_goal):
	goal_difference = int(str(ht_goal - at_goal).replace("-", ""))
	def get_new_odds(goal):
		_ = []
		n1 = random.randrange(30, 50, 7)
		n2 = random.randrange(51, 70, 7)
		for n in range(10):
			_.append(float(random.randrange(n1, n2, 1)))
		if goal == 0 or goal == 1 and goal_difference == 0 or goal_difference == 1:
			odd = float(random.randrange(2, 3, 1)) + random.choice(_)
		
		elif goal == 2 or goal == 3 and goal_difference == 2 or goal_difference == 3:
			odd = float(random.randrange(4, 5, 1)) + random.choice(_)

		elif goal == 4 or goal == 5 and goal_difference == 4 or goal_difference == 5:
			odd = float(random.randrange(6, 7, 1)) + random.choice(_)
			
		elif goal > 5 or goal_difference > 5:
			odd = float(random.randrange(40, 50, 1)) + random.choice(_)

		try:
			return odd
		except:
			print(f"Goal: {goal}\nGoal Differeence: {goal_difference}")
			return 0.0

	def updateForm(winner, side, game_outcome):
		def changeGameForm(form, game_outcome_):
			_ = []
			for go in form:
				_.append(go)

			_.remove(_[0])
			_.append(game_outcome_)

			return str(_).replace(", ", "").replace("[", "").replace("]", "").replace("'", "")

		loser = game['home_team'][0] if winner == game['away_team'][1] else game['away_team'][0]
		winner = winner if winner != "None" else ""


		if loser == game['home_team'][0]:
			game['home_team'][1] = changeGameForm(game['home_team'][1], "L")
		
		if loser == game['away_team'][0]:
			game['away_team'][1] = changeGameForm(game['away_team'][1], "L")

		if winner == game['home_team'][0]:
			game['home_team'][1] = changeGameForm(game['home_team'][1], "W")
		
		if winner == game['away_team'][0]:
			game['away_team'][1] = changeGameForm(game['away_team'][1], "W")

		
		if winner == "None" and side == "None":
			game['home_team'][1] = changeGameForm(game['home_team'][1], "D")
			game['away_team'][1] = changeGameForm(game['away_team'][1], "D")


	if ht_goal > at_goal:
		current_winner = game['home_team']
		updateForm(current_winner, "home", "W")

	elif at_goal > ht_goal:
		current_winner = game['away_team']
		updateForm(current_winner, "away", "W")

	else:
		updateForm("None", "None", "D")
		return getOdds(game['home_team'][1], game['away_team'][1])



	return [get_new_odds(ht_goal), 0, get_new_odds(at_goal)]

def populate_scoreboard():
	if game['home_team_score'] == 0 and game['away_team_score'] == 0:
		game['home_team_score'] = random.choice(numbers)
		game['away_team_score'] = random.choice(numbers)
	else:
		game['home_team_score'] = game['home_team_score'] + 1
		game['away_team_score'] = game['away_team_score'] + 1

def update_market(game, market_name):
	# Market 1X2
	def update(n, s, y):
		game['market'][n][s] = y
		pass

	theMarket = game['market'][market_name]
	if 1:
		GetOdds = getOdds(game['home_team'][1], game['away_team'][1])

		update("1X2", "Home", GetOdds[0])
		update("1X2", "Draw", GetOdds[1])
		update("1X2", "Away", GetOdds[2])

def start_game():
	print("-------------------------------------------")
	print("Game started!")
	print(f"{game['home_team'][0]} vs {game['away_team'][0]}")
	print("---------------------------------------------------------------------------")
	print(f"|                                 {game['home_team_score']}\t:\t{game['away_team_score']}                                   |")
	print("---------------------------------------------------------------------------")
	for x, y in game['market']['1X2'].items():
		
		# print(f"|> {x}")
		# print("---------------------------------------------------------------------------")
		# for y1, y2 in y.items():
		# 	print(f"{y1} - {y2}")

		# print("---------------------------------------------------------------------------")
		print(f"|> {x} - {y}")

	
	populate_scoreboard()
	update_market(game, "1X2")
	updateOdds(game['home_team_score'], game['away_team_score'])

# for t in range(6):
	# while t != 5400:
start_game()
	# print(game)











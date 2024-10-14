import random, json

with open("SnapMarket.json", "r") as market_file:
	SnapMarket_json = json.load(market_file)

class MarketLogic:
	def __init__(self):
		self.init = True
		self.SnapMarket = SnapMarket_json

	def Display_Error(self, e):
		# raise(e)
		print(f"> Error Encountered\n-------------------\n{e}\n-------------------")

	def Update_Game_Market(self, new_market):
		try:
			self.SnapMarket = new_market
			return "Updated SnapMarket"
		except Exception as e:
			self.Display_Error(e)

	def Display_Market(self, market):
		try:
			for item, value in self.SnapMarket[market].items():
				if str(type(value)) == "<class 'dict'>":
					print(item + ":")
					for v1, v2 in value.items():
						print(f">\t{v1} - {v2}")
				else:
					print(f"{item} - {value}")
		except Exception as e:
			self.Display_Error(e)

		return market

	def getFormPoints(self, form):
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

	def getFormCount(self, form):
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

	def getTeamsOdds(self, team_form_point, team, score1, score2, time, is_draw=[False, None]):
		_ = []
		n1 = random.randrange(30, 50, 7)
		n2 = random.randrange(51, 70, 7)
		for n in range(10):
			_.append(float(random.randrange(n1, n2, 1)))

		print(team_form_point)
		goal_difference = abs(score1 - score2)
		if is_draw[0] == True:
			odd = float(goal_difference * (self.getFormCount(team['form'])[1] + self.getFormCount(is_draw[1]['form'])[1]))
			if odd == 0.0:
				odd = team_form_point * (self.getFormCount(team['form'])[1] + self.getFormCount(is_draw[1]['form'])[1])

		else:
			if score1 == score2:
				if team_form_point >= 3.5 and team_form_point <= 5:
					odd = float(random.randrange(1, 2, 1)) + (team_form_point / random.choice(_))
				elif team_form_point >= 2 and team_form_point < 3.5:
					odd = float(random.randrange(2, 5, 1)) + (team_form_point / random.choice(_))
				elif team_form_point >= 0 and team_form_point < 2:
					odd = float(random.randrange(10, 20, 2))

			elif score1 > score2:
				odd = (score1 + score2) / ((score1 + score2) - team_form_point)
				print(True, True)

			elif score1 < score2:
				odd = ((self.getFormCount(team['form'])[0] * 1) * score1) * (time / team_form_point) 
				print(True, False)



		return round(odd, 2)

	def Market_1X2(self, s1, t1, s2, t2, current_time):
		market = "1X2"
		_market = self.Display_Market(market)
		team1_last_five_goals = eval(t1['last_five_goals'])
		team2_last_five_goals = eval(t2['last_five_goals'])
		g_a1 = sum(team1_last_five_goals) / len(team1_last_five_goals)
		g_a2 = sum(team2_last_five_goals) / len(team2_last_five_goals)


		t1_form_point = self.getFormPoints(t1['form'])
		t2_form_point = self.getFormPoints(t2['form'])		

		total_draw_count = self.getFormCount(t1['form'])[1] + self.getFormCount(t2['form'])[1]

		the_market = self.SnapMarket
		the_market[market]['Home'] = self.getTeamsOdds(t1_form_point, t1, s1, s2, current_time) # Home To Win
		the_market[market]['Draw'] = self.getTeamsOdds(total_draw_count, t1, s1, s2, current_time, [True, t2]) # Draw Game
		the_market[market]['Away'] = self.getTeamsOdds(t2_form_point, t2, s2, s1, current_time) # Away To Win

		self.Update_Game_Market(new_market=the_market)

	def Market_1X2_2UP(self, s1, t1, s2, t2, current_time):
		market = "1X2 2UP"
		self.Display_Market(market)
		self.Market_1X2(s1=s1, t1=t1, s2=s2, t2=t2)

	def Market_Over_Under(self, s1, t1, s2, t2, current_time):
		market = "Over/Under"
		self.Display_Market(market)

	def Market_Asian_Over_Under(self, s1, t1, s2, t2, current_time):
		market = "Asian Over/Under"
		self.Display_Market(market)

	def Market_Double_Chance(self, s1, t1, s2, t2, current_time):
		market = "Double Chance"
		self.Display_Market(market)

	def Market_First_Goal(self, s1, t1, s2, t2, current_time):
		market = "First Goal"
		self.Display_Market(market)

	def Market_Home_Over_Under(self, s1, t1, s2, t2, current_time):
		market = "Home Over/Under"
		self.Display_Market(market)

	def Market_Away_Over_Under(self, s1, t1, s2, t2, current_time):
		market = "Away Over/Under"
		self.Display_Market(market)

	def Market_GG_NG(self, s1, t1, s2, t2, current_time):
		market = "GG/NG"
		self.Display_Market(market)

	def Market_GG_NG_2(self, s1, t1, s2, t2, current_time):
		market = "GG/NG 2+"
		self.Display_Market(market)

	def Market_1H_1X2(self, s1, t1, s2, t2, current_time):
		market = "1st Half 1X2"
		self.Display_Market(market)

	def Market_1H_Over_Under(self, s1, t1, s2, t2, current_time):
		market = "1st Half Over/Under"
		self.Display_Market(market)

	def Market_1H_Double_Chance(self, s1, t1, s2, t2, current_time):
		market = "1st Half Double Chance"
		self.Display_Market(market)

	def Market_1H_First_Goal(self, s1, t1, s2, t2, current_time):
		market = "1st Half First Goal"
		self.Display_Market(market)

	


def allocate_odds(market, score1, score2, team1, team2, time):

	ML = MarketLogic()

	if market == "1X2":
		ML.Market_1X2(score1, team1, score2, team2, time)

	elif market == "1X2 2UP":
		ML.Market_1X2_2UP(score1, team1, score2, team2, time)

	elif market == "Over/Under":
		ML.Market_Over_Under(score1, team1, score2, team2, time)

	elif market == "Asian Over/Under":
		ML.Market_Asian_Over_Under(score1, team1, score2, team2, time)

	elif market == "Double Chance":
		ML.Market_Double_Chance(score1, team1, score2, team2, time)

	elif market == "First Goal":
		ML.Market_First_Goal(score1, team1, score2, team2, time)
		
	elif market == "Home Over/Under":
		ML.Market_Home_Over_Under(score1, team1, score2, team2, time)
		
	elif market == "Away Over/Under":
		ML.Market_Away_Over_Under(score1, team1, score2, team2, time)
		
	elif market == "GG/NG":
		ML.Market_GG_NG(score1, team1, score2, team2, time)

	elif market == "GG/NG 2+":
		ML.Market_GG_NG_2(score1, team1, score2, team2, time)

	elif market == "1st Half 1X2":
		ML.Market_1H_1X2(score1, team1, score2, team2, time)

	elif market == "1st Half Over/Under":
		ML.Market_1H_Over_Under(score1, team1, score2, team2, time)

	elif market == "1st Half Double Chance":
		ML.Market_1H_Double_Chance(score1, team1, score2, team2, time)

	elif market == "1st Half First Goal":
		ML.Market_1H_First_Goal(score1, team1, score2, team2, time)

	else:
		ML.Display_Error("Market Not Found")





# print(ML.Market_1X2("1X2"))
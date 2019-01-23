import random
import sav
import time
import sys
import pickle

debugm = pickle.load(open("sys_info_d.kpak", "rb"))

save = sav.data
savw = open("sav.py", "w")

currentwars = []

class NoValidEnding(Exception):
	pass

class QuestionIndexingError(Exception):
	pass	

		
print("Reading save file...\n")
if save["started"]:
	print("Save detected!\n")
	savw.write("data = " + str(save))
	savw.close()
	
if not save["started"]:
	print(" It appears that you are starting a new game.\n")
	save["pname"] = input("Please choose a name.")
	if save["pname"] == "Brendon":
		print("...\n")
		time.sleep(3)
		print("...?\n")
		time.sleep(3)
		print("Okay?")
	if save["pname"] == "Brooke":
		time.sleep(4)
		print("?????????????????????????")
	else:
		print("Excellent.\nTruly excellent.\n")
	print("Registering save index...\n")
	save["ansques"] = []
	save["stats"] = {
		"popularity": 1,
		"militarystrength": 1,
		"money": 1
	}
	save["started"] = True
	save["eventchoice"] = {}
	save["eventchoice"]["y"] = []
	save["eventchoice"]["n"] = []
	savw.write( "data =" + " " + str(save))
	print("Created base save!\n")
	savw.close()
	
		
	
military = save["stats"]["militarystrength"]
money = save["stats"]["money"]
popularity = save["stats"]["popularity"]

def savenow():
	savwr = open(savw.name, "w")
	save["stats"]["militarystrength"] = military
	save["stats"]["money"] = money
	save["stats"]["popularity"] = popularity
	savwr.write("data = " + str(save))
	savwr.close()
	if debugm:
		print("File saved.")
	else:
		pass

def debug_run(command):
	exec(command)



class question:
	def __init__(self, questi, answer, popularityval, militaryval, moneyval):
		self.answ = answer
		self.questionp = questi
		self.popul = popularityval
		self.milit = militaryval
		self.money = moneyval
	def ask(self):
		global military, money, popularity
		self.useranswer = input(self.questionp + "\n")
		self.useranswer = str(self.useranswer)
		if self.useranswer == str(self.answ):
			print("You are correct!\n")
			self.correct = True
			military += self.milit
			popularity += self.popul
			money += self.money
		else:
			print("You are incorrect...\n")
			self.correct = False
			military -= self.milit
			popularity -= self.popul
			money -= self.money
		save["ansques"].append(self.questionp)
			

def addq(id, que):
	try:
		quesdict = pickle.load(open("question_data.kpak", "rb"))
	except EOFError:
		fw = open("question_data.kpak", "wb")
		quesdict = {1: "placeholder"}
		pickle.dump(quesdict, fw)
		fw.close()
	quesdict = pickle.load(open("question_data.kpak", "rb"))
	quesdict[id] = que
	fwe = open("question_data.kpak", "wb")
	pickle.dump(quesdict, fwe)
	fwe.close()

questionindex = []	

def getq(id):
	global questionindex
	try:
		qro = open("question_data.kpak", "rb")
		qr = pickle.load(qro)
		c = qr[id]
		questionindex.append(id)
		return question(c[0], c[1], c[2], c[3], c[4])
	except:
		return question("Big error down the lane", 0, 0, 0, 0)

questions = {
	1: getq(1),
	2: getq(2),
	3: getq(3),
	4: getq(4),
	5: getq(5),
	6: getq(6),
	7: getq(7),
	8: getq(8),
	9: getq(9),
	10: getq(10),
	11: getq(11),
	12: getq(12),
	13: getq(13),
	14: getq(14),
	15: getq(15),
	16: getq(16),
	17: getq(17),
	18: getq(18),
	19: getq(19),
	20: getq(20),
	21: getq(21),
	22: getq(22),
	23: getq(23),
	24: getq(24),
	25: getq(25)
}

warcurrentlyon = False

class revolution:
	def __init__(self, reason):
		global warcurrentlyon
		self.reason = reason
		self.winmeter = 0
		self.ended = False
		warcurrentlyon = True
		print("A revolution started because your " + self.reason + " reached zero.")
	def end(self, winner):
		global warcurrentlyon
		self.ended = True
		self.winner = winner
		warcurrentlyon = False
	def cont(self, plw):
		global military, money, popularity
		if self.ended:
			pass
		elif self.winmeter >= 10:
			self.end("Government")
		elif self.winmeter <= 0:
			self.end("Rebels")
		elif plw:
			self.winmeter = self.winmeter + 1
		elif not plw:
			self.winmeter = self.winmeter - 1
		if self.reason == "Popularity":
			military = military - 0.5
			money = money - 0.5
		elif self.reason == "Money":
			military = military - 0.5
			popularity = popularity - 0.5


						
class ChoiceEvent:
	def __init__(self, text, popul, milit, money):
		self.prompt = text
		self.popul = popul
		self.milit = milit
		self.money = money
		self.useranswer = ""
	def start(self):
		global popularity, money, military
		self.useranswer = input(self.prompt)
		self.useranswer = self.useranswer.lower()
		if self.useranswer == "y":
			popularity += self.popul
			military += self.milit
			money += self.money
		else:
			popularity -= self.popul
			military -= self.milit
			money -= self.money
		savenow()
			

choiceevents = {
	"test": ChoiceEvent("test", 5, -5, 5),
	#Format: Popularity, Military, Money
	1: ChoiceEvent("You have a chance to trade with a new foreign nation, but your people do not like them. Do it?",  
	-0.5, 
	0, 
	1),
	
	2: ChoiceEvent("Your people are pushing you to lower taxes. Do it?", 1, 0, -1),
	
	3: ChoiceEvent("Your military seems worse than usual. Spend extra money on it?",
	0,
	1,
	-0.5),
	
	
	"tutorial_0": ChoiceEvent("Would you like to go through the tutorial?(Y/N)", 0, 0, 0)
}

test_question = question("0", "0", 5, 5, 5)

choiceeventindex = [1, 2, 3]

def test_func():
	test_question.ask()
	choiceevents["test"].start()
	save["ansques"].append("test")
	savenow()
	


def endgame():
	totalstat = military + popularity + money
	print("The game is over.\n")
	if totalstat == 30:
		print("You were a successful King. You got every stat to go up to ten!\n")
		save["started"] = False
		savenow()
		time.sleep(5)
		sys.exit()
	if totalstat == 0:
		print("You failed as a king, and Israel has fallen thanks to you.\n")
		save["started"] = False
		savenow()
		time.sleep(5)
		sys.exit()
	if len(questionindex) == 0:
		if totalstat >= 15:
			print("You did fine as a king, but not that well.\n")
		elif totalstat >= 10:
			print("You did pretty bad. Everybody is slowly losing faith in you, and Israel.\n")
		elif totalstat < 10:
			print("You did so bad. You were exiled and are not welcome back.")
		save["started"] = False
		savenow()
		time.sleep(5)
		sys.exit()
	else:
		raise NoValidEnding("No valid ending found. save dict contents: " + str(save))
		

def play():
	global money, military, popularity
	dot = choiceevents["tutorial_0"]
	ischoiceevent = random.choice([True, False, False])
	dot.start()
	if dot.useranswer == "y":
		print("\n\nWelcome to the game prototype! In this game, you, " + save["pname"] + " are a new king.\n")
		print ("\nIt is your job to keep Israel at its best in three statistics: military, money, and your popularity.")
		print("\nYou do this by answering questions and making choices.\n")
		print("Read INSTRUCTIONS.txt for more info.\n")
	else:
		print("Starting game...\n")
	while save["started"]:
		if military > 10:
			military = 10
		if money > 10:
			money = 10
		if popularity > 10:
			popularity = 10
		if military < 0:
			military = 0
		if money < 0:
			money = 0
		if popularity < 0:
			popularity = 0
		if money + popularity + military >= 30:
			endgame()
		if len(questionindex) == 0:
			endgame()
		if money + popularity + military <= 0:
			endgame()
		else:
			questionpl = random.choice(questionindex)
			if questions[questionpl].questionp in save["ansques"]:
				questionindex.remove(questionpl)
				questionpl = random.choice(questionindex)
			questions[questionpl].ask()
			questionindex.remove(questionpl)
			if questions[questionpl].useranswer == "debug":
				if debugm:
					debug_comm = input()
					debug_run(debug_comm)
					questions[questionpl].ask()
				else:
					questions[questionpl].ask()
			savenow()
			if ischoiceevent:
				try:
					choicepl = random.choice(choiceeventindex)
					cpla = choiceevents[choicepl]
					cpla.start()
					save["eventchoice"][cpla.useranswer].append(choicepl)
					choiceeventindex.remove(choicepl)
				except IndexError:
					print("")
				savenow()
			if money == 0:
				if not warcurrentlyon:
					rv = revolution("Money")
				else:
					pass
			if popularity == 0:
				if not warcurrentlyon:
					rv = revolution("Popularity")
				else:
					pass
			if warcurrentlyon:
				if rv.ended:
					if rv.winner == "Rebels":
						print("You were taken down in the revolution!\n")
						endgame()
					else:
						print("You stopped the revolution!\n")
				elif questions[questionpl].correct:
					plwtemp = True
				else:
					plwtemp = False
				rv.cont(plwtemp)
			else:
				savenow()
			print("\n\nYou current stats are:\nMilitary:")
			print(str(military) + "\nPopularity:")
			print(str(popularity) + "\nMoney:")
			print(str(money))
			savenow()
			print("\n")
			
if __name__ == "__main__":
	play()


# -*- coding: utf-8 -*-
import random
import csv
import sys

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

#----------------------Setting variables-------------------------

# Question: Do single leading underscores make sense for those variables?
openQuestions = [] # Holds UIDs of open Questions
QuizOn = 1
GlobalDict = {} # Holds a Dict with UID as key and rest as dict in value.
today = datetime.today()
chosenSubject = ""
mode = ""

#----------------------Defining functions-------------------------

def setUp():
	global mode
	global GlobalDict

	# Open CSV file
	with open('sample.csv', 'r') as csv_file:
		database = csv.DictReader(csv_file, delimiter=';')

		# Make the csv data available in GlobalDict
		for line in database :
			GlobalDict[line['UID']] = {'Question': line['Question'], 
				'Answer': line['Answer'],
				'DueDate': line['DueDate'],
				'Phase': line['Phase'],
				'Subject': line['Subject'],
				'Swapped': line['Swapped'],
				'DateCreated': line['DateCreated'],
			}
	
	print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	print("Welcome to the Terminal Vocabulary Trainer!")

	# If database is empty, automatically start with inserting vocabulary.
	if len(GlobalDict.keys()) == 0:
		mode = "a"
	else:
		print("Do you want to quiz 'q' or add vocabulary 'a'?")
		mode = raw_input("Enter your choice: ")

def setUpAdd():
	global chosenSubject
	global GlobalDict

	if len(GlobalDict.keys()) == 0:
		print("In order to start, let's first add some new vocabulary.")
		chosenSubject = raw_input("Which subject do you want to start with?")
		print("The vocabulary you enter will be added this subject.")
	else:
		print("This are your current subjects. Choose one or type the name of a new one.")
		ListofSubjects = {}
		for key, value in GlobalDict.items():
			if value["Subject"] in ListofSubjects.keys() :
				ListofSubjects[value["Subject"]] += 1
			else: 
				ListofSubjects[value["Subject"]] = 1
		for key, value in ListofSubjects.items() :
			print(key, value)
		chosenSubject = raw_input("Choose subject:")

def setUpQuiz():	
	global chosenSubject
	global openQuestions
	global GlobalDict

	# Generate the list of subjects to choose from
	ListofSubjects = {}
	for key, value in GlobalDict.items():
		if (value['DueDate'] == ''):
			pass
		elif (today >= datetime.strptime((value["DueDate"]),"%d.%m.%y")):
			if value["Subject"] in ListofSubjects.keys() :
				ListofSubjects[value["Subject"]] += 1
			else: 
				ListofSubjects[value["Subject"]] = 1

	# Check if any items are due
	if len(ListofSubjects.keys()) == 0:
		print('You are all good - no due items today!')
	else:
		print("Subject overview:")
		for key, value in ListofSubjects.items() :
			print(key, value)
		
		chosenSubject = raw_input('Which subject do you want to learn: ') #Wie kann man Auswahlmöglichkeiten geben?
		message = "Alright, let's start with {}!".format(chosenSubject)
		print (message)

		# Generate list of openQuestions
		for key, value in GlobalDict.items():
			if (value['DueDate'] == ''):
				pass
			elif (value['Subject'] == chosenSubject) and (today >= datetime.strptime((value["DueDate"]+' 00:00:00'),"%d.%m.%y %H:%M:%S")):
				openQuestions.append(key)
		message = "Quiz with {} items is generated.".format(len(openQuestions))
		print(message)


def askRandomQuestion():
	global openQuestions
	global GlobalDict
	global QuizOn

	def updateDueDate(currentPhase):
		if currentPhase == 1:
			return datetime.now() + timedelta(days=3)
		elif currentPhase == 2:
			return datetime.now() + timedelta(days=10)
		elif currentPhase == 3:
			return datetime.now() + timedelta(days=30)
		elif currentPhase == 4:
			return datetime.now() + timedelta(days=30)
		elif currentPhase == 5:
			return datetime.now() + timedelta(days=90)
		elif currentPhase == 6:
			return ''

	currentQuestion = openQuestions[random.randint(0,len(openQuestions)-1)]
	print("---------------------------------------------------------------------")
	if GlobalDict[currentQuestion]["Swapped"] == "" :
		print GlobalDict[currentQuestion]["Question"]
		raw_input('Your answer: ')
		print 'Correct answer: ' + GlobalDict[currentQuestion]["Answer"]
	else:
		print GlobalDict[currentQuestion]["Answer"]
		raw_input('Your answer: ')
		print 'Correct answer: ' + GlobalDict[currentQuestion]["Question"]
	
	Check = raw_input('Was your answer correct? Type "y" for Yes, "e" for exit: ')
	
	if Check == "y" :
		GlobalDict[currentQuestion].update({'DueDate': updateDueDate(int(GlobalDict[currentQuestion]["Phase"])).strftime("%d.%m.%y")}) #["Phase"]).strptime("%d.%m.%y")
		newPhase = int(GlobalDict[currentQuestion]['Phase'])+1
		GlobalDict[currentQuestion].update({'Phase': newPhase})
		openQuestions.remove(currentQuestion)
		message = 'Nice, new due date is {}'.format(GlobalDict[currentQuestion]["DueDate"])
		print(message)
		# Needs to delete right items from openQuestions and update the GlobalDict
	elif Check == "e":
		QuizOn = 0
	else:
		GlobalDict[currentQuestion]['Phase'] = 1
		print 'Oops, item returned to phase 1.'


def saveNewCSV ():
	with open('test_writer.csv', 'w') as new_file:
		fieldnames = ['UID', 'Question','Subject', 'Answer', 'DueDate', 'Phase', 'Swapped', 'DateCreated']

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
		csv_writer.writeheader()

		for key, value in GlobalDict.items() : # Potential problem: When empty it still prints an empty raw in csv for some reason
		 	value['UID'] = key
		 	csv_writer.writerow(value)


def main(): # In the future it could use the csv-name as argument.
	global QuizOn
	global mode
	while QuizOn == 1:
		setUp()
		if mode == "q" :
			setUpQuiz()
			while len(openQuestions)>0:
				askRandomQuestion()
				if QuizOn == 0:
					break
			print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
			if QuizOn == 0:
				print 'Okay, quiz canceled.'
			else:
				print('Nice, you are done with %s!' %chosenSubject)
			saveNewCSV()
			print('Your progress is saved in CSV.')
			QuizOn = input('Enter 1 to continue with another subject, or 0 to end: ')
		elif mode == "a" :
			setUpAdd()
			print("Sorry, adding vocabulary is still under construction.")
			QuizOn = 0
		else:
			print("Oops, this went wrong. Try 'a' to add vocabulary, or 'q' for quiz.")


#----------------------Running it-------------------------
if __name__ == '__main__' :
	sys.exit(main())


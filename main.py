# -*- coding: utf-8 -*-
import random
import csv
import sys

from datetime import date, time, datetime, timedelta

#----------------------Setting variables-------------------------

# Question: Do single leading underscores make sense for those variables?
openQuestions = [] # Holds UIDs of open Questions
QuizOn = 1
GlobalDict = {} # Holds a Dict with UID as key and rest as dict in value.
today = datetime.today()
chosenSubject = ""
mode = ""
SubjectList = {}

#----------------------Defining functions-------------------------

def setUp():
	global mode
	global GlobalDict
	global SujectList
	global chosenSubject

	chosenSubject = ""
	GlobalDict = {}
	SubjectList = {}

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

			# Create subject list to replace ListofSubjects
			if line["Subject"] not in SubjectList.keys() :
				SubjectList[line["Subject"]] = {"Total": 0, "Due": 0}
			SubjectList[line["Subject"]]["Total"] += 1
			if (line["DueDate"] != "") :
				if (today >= datetime.strptime((line["DueDate"]),"%d.%m.%y")) :
					SubjectList[line["Subject"]]["Due"] += 1
	
	#Printing the introduction
	print("x x x x x x x x x x x x x x x x x x x x x x x x x x ")
	print("WELCOME to the Terminal Vocabulary Trainer!")
	print("x x x x x x x x x x x x x x x x x x x x x x x x x x ")

	# If database is empty, automatically start with inserting vocabulary.
	if len(GlobalDict.keys()) == 0:
		print("Your vocabulary database seems to be empty :0")
		mode = "a"
	else:
		print("OVERVIEW of your database")
		for key, value in SubjectList.items() :
			print key, value
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
		print("Choose one of your subjects or type the name of a new one.")
		chosenSubject = raw_input("Choose subject: ")
	print("Good to know: Every item will be added also with swapped question/answer-pair.")

def setUpQuiz():	
	global chosenSubject
	global openQuestions
	global GlobalDict
	global SubjectList
	
	openQuestions = []
	chosenSubject = raw_input('Which subject do you want to learn: ')

	# Generate list of openQuestions
	for key, value in GlobalDict.items():
		if (value['DueDate'] == ''):
			pass
		elif (value['Subject'] == chosenSubject) and (today >= datetime.strptime(value["DueDate"],"%d.%m.%y")):
			openQuestions.append(key)
	if len(openQuestions) == 0:
		print("The subject doesn't exist, or there are no due items.")
	else:
		message = "Alright, Quiz with {} items is generated.".format(len(openQuestions))
		print(message)


def askRandomQuestion():
	global openQuestions
	global GlobalDict
	global QuizOn

	def updateDueDate(currentPhase):
		if currentPhase == 1:
			return datetime.now() + timedelta(days=1)
		elif currentPhase == 2:
			return datetime.now() + timedelta(days=3)
		elif currentPhase == 3:
			return datetime.now() + timedelta(days=10)
		elif currentPhase == 4:
			return datetime.now() + timedelta(days=30)
		elif currentPhase == 5:
			return datetime.now() + timedelta(days=90)
		elif currentPhase == 6:
			return ''

	currentQuestion = openQuestions[random.randint(0,len(openQuestions)-1)]
	print("---------------------------------------------------------------------")
	if GlobalDict[currentQuestion]["Swapped"] == "" :
		print 'QUESTION: ' + GlobalDict[currentQuestion]["Question"]
		raw_input('YOUR ANSWER: ')
		print 'CORRECT ANSWER: ' + GlobalDict[currentQuestion]["Answer"]
	else:
		print 'QUESTION: ' + GlobalDict[currentQuestion]["Answer"]
		raw_input('YOUR ANSWER: ')
		print 'CORRECT ANSWER: ' + GlobalDict[currentQuestion]["Question"]
	print("Was your answer correct?")
	Check = raw_input("Type 'y' if Yes, 'e' for exit: ")
	
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
		print 'Practice makes perfect.'
		raw_input('Type the right answer again: ')

def AddItem ():
	global chosenSubject
	global GlobalDict
	global QuizOn

	input1 = raw_input("Insert NEW QUESTION (or 0 to end): ")
	if input1 == "0":
		QuizOn = 0
	else:
		input2 = raw_input('Insert the answer: ')

		nextUID = int(max(GlobalDict, key=int)) + 1
		GlobalDict[nextUID] = {'Question': input1, 
					'Answer': input2,
					'DueDate': today.strftime('%d.%m.%y'),
					'Phase': 1,
					'Subject': chosenSubject,
					'Swapped': "",
					'DateCreated': today.strftime('%d.%m.%y'),
				}
		nextUID += 1
		GlobalDict[nextUID] = {'Question': input1, 
					'Answer': input2,
					'DueDate': today.strftime('%d.%m.%y'),
					'Phase': 1,
					'Subject': chosenSubject,
					'Swapped': 'swapped',
					'DateCreated': today.strftime('%d.%m.%y'),
				}
		message = 'Nice, new item added to {}'.format(chosenSubject)
		print message

def saveNewCSV ():
	with open('sample.csv', 'w') as new_file:
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
			QuizOn = input('Enter 1 to return to start or 0 to end: ')
		elif mode == "a" :
			setUpAdd()
			while QuizOn != 0:
				AddItem()
			saveNewCSV()
			print('Your progress is saved in CSV.')
			QuizOn = input('Enter 1 to return to start or 0 to end: ')
		else:
			print("Oops, this went wrong. Try 'a' to add vocabulary, or 'q' for quiz.")


#----------------------Running it-------------------------
if __name__ == '__main__' :
	sys.exit(main())


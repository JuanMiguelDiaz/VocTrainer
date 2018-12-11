
# -*- coding: utf-8 -*-
import random
import csv
import sys

from datetime import date
from datetime import time
from datetime import datetime

#----------------------Setting variables-------------------------

# Question: Do single leading underscores make sense for those variables?
openQuestions = [] # Holds UIDs of open Questions
QuizOn = 1
GlobalDict = {} # Holds a Dict with UID as key and rest as dict in value.
today = datetime.today()
chosenSubject = ""


#----------------------Defining functions-------------------------

def setUp():
	global openQuestions
	global ListofSubjects
	global chosenSubject

	# Open CSV file
	with open('./backup/backup.csv', 'r') as csv_file:
		database = csv.DictReader(csv_file, delimiter=';')

		# Make the csv data available in GlobalDict
		for line in database :
			GlobalDict[line['UID']] = {'Frage': line['Frage'], 
				'Antwort': line['Antwort'],
				'DueDate': line['DueDate'],
				'Phase': line['Phase'],
				'Subject': line['Subject'],
				'Tausch': line['Tausch'],
				'Zusatzangaben': line['Zusatzangaben'],
				'Eingabedatum': line['Eingabedatum'],
			}

	# Generate the list of subjects to choose from
	ListofSubjects = {}
	for key, value in GlobalDict.items():
		if (value['DueDate'] == ''):
			pass
		elif (today >= datetime.strptime((value["DueDate"]+' 00:00:00'),"%d.%m.%y %H:%M:%S")):
			if value["Subject"] in ListofSubjects.keys() :
				ListofSubjects[value["Subject"]] += 1
			else: 
				ListofSubjects[value["Subject"]] = 1

	# Get user input
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

	currentQuestion = openQuestions[random.randint(0,len(openQuestions)-1)]
	print("---------------------------------------------------------------------")
	print GlobalDict[currentQuestion]["Frage"]
	raw_input('Your answer: ')
	print 'Correct answer: ' + GlobalDict[currentQuestion]["Antwort"]
	Check = raw_input('Was your answer correct? Type "y" for Yes, "e" for exit: ')
	
	if Check == "y" :
		openQuestions.remove(currentQuestion)
		# Needs to delete right items from openQuestions and update the GlobalDict
	elif Check == "e":
		QuizOn = 0
	else:
		GlobalDict[currentQuestion]['Phase'] = 1


def saveNewCSV ():
	with open('test_writer.csv', 'w') as new_file:
		fieldnames = ['UID', 'Frage','Subject', 'Antwort', 'DueDate', 'Phase', 'Tausch', 'Eingabedatum', 'Zusatzangaben']

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
		csv_writer.writeheader()

		for key, value in GlobalDict.items() :
		 	value['UID'] = key
		 	csv_writer.writerow(value)


def main(): # In the future it could use the csv-name as argument.
	global QuizOn
	while QuizOn == 1:
		setUp()
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


#----------------------Running it-------------------------
if __name__ == '__main__' :
	sys.exit(main())


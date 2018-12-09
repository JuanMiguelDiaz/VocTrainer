
# -*- coding: utf-8 -*-
import random
import csv

from datetime import date
from datetime import time
from datetime import datetime

#----------------------Setting variables-------------------------

openQuestions = {}
QuizOn = 1
GlobalDict = {}
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
	
	chosenSubject = input('Which subject do you want to learn: ') #Wie kann man Auswahlmöglichkeiten geben?
	print ("Alright, let's start with "  + chosenSubject + "!")

	# Generate list of openQuestions


def askQuestion():
	global openQuestions
	
	# Print a (random) question from openQuestions

	# Proposes if the answer is right, lets user decide, and returns Boolean

	# Needs to delete right items from openQuestions and update the GlobalDict


def saveNewCSV ():
	with open('test_writer.csv', 'w') as new_file:
		fieldnames = ['UID', 'Frage','Subject', 'Antwort', 'DueDate', 'Phase', 'Tausch', 'Eingabedatum', 'Zusatzangaben']

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
		csv_writer.writeheader()

		for key, value in GlobalDict.items() :
		 	value['UID'] = key
		 	csv_writer.writerow(value)



#----------------------Running it-------------------------
while QuizOn == 1:
	setUp()
	while openQuestions.length()>0:
		askQuestion()
	print('Nice, you are done with %s!' %chosenSubject)
	saveNewCSV()
	print('Your progress is saved in CSV.')
	QuizOn = input('Enter 1 to continue with another subject, or 0 to end: ')



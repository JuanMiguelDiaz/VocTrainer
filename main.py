
# -*- coding: utf-8 -*-
import random
import csv

from datetime import date
from datetime import time
from datetime import datetime

#----------------------Setting variables-------------------------

openQuestions = {}
keepLearning = 1
GlobalDict = {}
today = datetime.today()



#----------------------Open CSV File-------------------------
with open('./backup/backup.csv', 'r') as csv_file:
	database = csv.DictReader(csv_file, delimiter=';')

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

# Reads in due items per subject
	ListofSubjects = {}
	for key, value in GlobalDict.items():
		if (value['DueDate'] == ''):
			pass
		elif (today >= datetime.strptime((value["DueDate"]+' 00:00:00'),"%d.%m.%y %H:%M:%S")):
			if value["Subject"] in ListofSubjects.keys() :
				ListofSubjects[value["Subject"]] += 1
			else: 
				ListofSubjects[value["Subject"]] = 1

# Writing a new file
	with open('test_writer.csv', 'w') as new_file:
		fieldnames = ['UID', 'Frage','Subject', 'Antwort', 'DueDate', 'Phase', 'Tausch', 'Eingabedatum', 'Zusatzangaben']

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
		csv_writer.writeheader()

		for key, value in GlobalDict.items() :
		 	value['UID'] = key
		 	csv_writer.writerow(value)


#----------------------Defining functions-------------------------
def setUp():
	global openQuestions
	global ListofSubjects

	chosenLibrary = ""

	print("Subject overview:")

	for key, value in ListofSubjects.items() :
		print(key, value)

	def askForLibrary():
		global chosenLibrary
		chosenLibrary = input('Which subject do you want to learn: ') #Wie kann man Auswahlmöglichkeiten geben?
		print ('you entered ' + chosenLibrary)
	
	def LoadLibrary():
		global openQuestions
		global chosenLibrary
		pass
	
	askForLibrary()
	LoadLibrary()

def askQuestion():
	global openQuestions
	
	def printQuestion():
		pass

	def compareResult():
		pass

	def sortBack():
		pass

#----------------------Running it-------------------------
while keepLearning == 1:
	setUp()
	while openQuestions.length()>0:
		askQuestion()
	keepLearning = input('1 for continue, 0 for end: ')



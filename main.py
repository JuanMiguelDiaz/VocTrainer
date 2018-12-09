
# -*- coding: utf-8 -*-
import random
import csv

#----------------------Setting variables-------------------------

chosenLibrary = ""
openQuestions = {}
keepLearning = 1
GlobalDict = {}


#----------------------Open CSV File-------------------------
with open('./backup/backup.csv', 'r') as csv_file:
	database = csv.DictReader(csv_file, delimiter=';')

	for line in database :
		GlobalDict[line['UID']] = {'Frage': line['Frage'], 
			'Antwort': line['Antwort'],
			'DueDate': line['DueDate'],
			'Phase': line['Phase'],
			'Fach': line['Fach'],
			'Tausch': line['Tausch'],
			'Zusatzangaben': line['Zusatzangaben'],
			'Eingabedatum': line['Eingabedatum'],
		}

# Reads in the Anzahl pro Fach
	ListofFach = {}
	for key, value in GlobalDict.items():
		if value["Fach"] in ListofFach.keys() :
			ListofFach[value["Fach"]] += 1
		else: 
			ListofFach[value["Fach"]] = 1

	for key, value in ListofFach.items() :
		print(key, value)

# Writing a new file
	with open('test_writer.csv', 'w') as new_file:
		fieldnames = ['UID', 'Frage','Fach', 'Antwort', 'DueDate', 'Phase', 'Tausch', 'Eingabedatum', 'Zusatzangaben']

		csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
		csv_writer.writeheader()

		for key, value in GlobalDict.items() :
		 	value['UID'] = key
		 	csv_writer.writerow(value)

# Got it from here https://youtu.be/q5uM4VKywbA?t=754

#----------------------Defining functions-------------------------
def setUp():
	global openQuestions
	global chosenLibrary

	def askForLibrary():
		global chosenLibrary
		chosenLibrary = input('Which libarary do you want to learn: ') #Wie kann man Auswahlmöglichkeiten geben?
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



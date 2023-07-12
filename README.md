# VocTrainer
Basically, Python reads a csv-file and creates a vocabulary quiz for your command-line. 

The tool allows you not only to quiz, but also to add new vocabulary in individual subject-folders. When quitting the quiz, your progress is saved in the csv-file. New vocabulary is always added with a reversed card-pair as well. 


## Prerequisites
To use VocTrainer you need... 
* Python3 installed
* Basic command-line skills. If you never used your Terminal, check out the basic commands [here](https://github.com/0nn0/terminal-mac-cheatsheet#core-commands) and your are good to go.

## How to start it
1. Download this folder.
2. Open your Terminal (or any other command-line tool) and navigate to the downloaded folder.
3. Start the main.py using `python3 main.py`

## Set up your libary
The project comes with a sample file called 'sample.csv'. If you want to start using VocTrainer from scratch, simply replace the reference to the 'sample.csv' in line 30 and 183 of 'main.py' to the 'empty.csv', which is an empty template that you can fill with your own vocabulary.

## The interval-systmatic
The quiz is based on a phase-based interval-systematic. In short, every item starts in phase 1 and enters the next phase, when answered right. The interval depends on the current phase of the item:

Learning Phase* | Days until next quiz
--- | ---
1 | 1
2 | 3
3 | 10
4 | 30
5 | 90
6 | Long-term memory :-)

See explanation and scientific background [here](https://www.phase-6.de/service/wissenschaftlicher_hintergrund.html). Don't worry: The summary and linked articles are in English, even though the website is German.

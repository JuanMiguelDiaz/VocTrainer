# VocTrainer
A simple, open-source vocabulary trainer that runs in your terminal.

Basically, the Python script turns a CSV-file with "learning cards" into a learning quiz.

The tool allows you not only to quiz, but also to add new vocabulary in customizable subject-folders. When quitting the quiz, your progress is saved in the CSV-file as well. New quiz items are always added with a reversed card-pair as well.

## The interval-based learning: From Phase 1 to Phase 6 (= Long-term memory)
VocTrainer's quiz is based on intervals to optimize the long-term learning effectiveness.

Every quiz item starts in phase 1 and enters the next phase, when you answered correctly. You will get the question again for repetition after the interval ended.

The duration of each interval depends on the phase of the quiz item:

Learning Phase* | Days until next quiz
--- | ---
1 | 1
2 | 3
3 | 10
4 | 30
5 | 90
6 | Long-term memory :-)

See explanation and scientific background [here](https://www.phase-6.de/service/wissenschaftlicher_hintergrund.html). Don't worry: The summary and linked articles are in English, even though the website is German.


## Prerequisites
To use VocTrainer you need...
* Python3 installed
* Basic command-line skills. If you never used your Terminal, check out the basic commands [here](https://github.com/0nn0/terminal-mac-cheatsheet#core-commands) and your are good to go.

## How to start it
1. Download this folder.
2. Open your Terminal (or any other command-line tool) and navigate to the downloaded folder.
3. Start the main.py using `python3 main.py`

## Set up your library
The project comes with a sample file called 'sample.csv'. If you want to start using VocTrainer from scratch, simply replace the reference to the 'sample.csv' in line 30 and 183 of 'main.py' to the 'empty.csv', which is an empty template that you can fill with your own vocabulary.

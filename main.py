import random
import csv
from datetime import datetime, timedelta

def load_data_from_csv(filename):
    try:
        data = {}
        subject_list = {}

        with open(filename, 'r') as csv_file:
            database = csv.DictReader(csv_file, delimiter=';')

            for line in database:
                uid = int(line['UID'])
                data[uid] = {
                    'Question': line['Question'],
                    'Answer': line['Answer'],
                    'DueDate': line['DueDate'],
                    'Phase': int(line['Phase']),
                    'Subject': line['Subject'],
                    'Swapped': line['Swapped'],
                    'DateCreated': line['DateCreated'],
                }

                subject = line['Subject']
                subject_list.setdefault(subject, {"Total": 0, "Due": 0})
                subject_list[subject]["Total"] += 1
                if line["DueDate"] != "" and datetime.today() >= datetime.strptime(line["DueDate"], "%Y-%m-%d"):
                    subject_list[subject]["Due"] += 1

        return data, subject_list
    except FileNotFoundError:
        print(f"Error: CSV file '{filename}' not found.")
        return {}, {}
    except csv.Error:
        print(f"Error: Malformed CSV file '{filename}'.")
        return {}, {}

def update_due_date(current_phase):
    due_dates = [1, 3, 10, 30, 90]
    if current_phase <= len(due_dates):
        return datetime.now() + timedelta(days=due_dates[current_phase - 1])
    return ''

def ask_random_question(open_questions, global_dict):
    if not open_questions:
        print("The subject doesn't exist, or there are no due items.")
        return False

    current_question = random.choice(open_questions)
    print("---------------------------------------------------------------------")
    question_key = "Answer" if global_dict[current_question]["Swapped"] else "Question"
    print('QUESTION: ' + global_dict[current_question][question_key])
    user_answer = input('YOUR ANSWER: ')
    print('CORRECT ANSWER: ' + global_dict[current_question]["Answer"] if question_key == "Question" else global_dict[current_question]["Question"])
    print("Was your answer correct?")
    check = input("Type 'y' if your answer is correct, 'e' for exit \nType any other key if your answer was wrong: ")

    if check.lower() == "y":
        current_phase = global_dict[current_question]["Phase"]
        if current_phase >= 5:
            print("Congratulations! You have mastered this item and have it in your long-term memory.")
            global_dict[current_question]["DueDate"] = ""
        else:
            global_dict[current_question]["DueDate"] = update_due_date(current_phase).strftime("%Y-%m-%d")
            global_dict[current_question]["Phase"] += 1

        open_questions.remove(current_question)
        if global_dict[current_question]["DueDate"]:
            print(f'Nice, new due date is {global_dict[current_question]["DueDate"]}')
    elif check.lower() == "e":
        return False
    else:
        global_dict[current_question]["Phase"] = 1
        print('Oops, item returned to phase 1. We will try this later today.')
        input('Type the right answer again to practice: ')

    return True


def add_item(chosen_subject, global_dict):
    try:
        input1 = input("Insert NEW QUESTION (or 0 to end): ")
        if input1 == "0":
            return False

        input2 = input('Insert the answer: ')

        next_uid = max(global_dict, default=0) + 1
        global_dict[next_uid] = {
            'Question': input1,
            'Answer': input2,
            'DueDate': datetime.today().strftime('%Y-%m-%d'),
            'Phase': 1,
            'Subject': chosen_subject,
            'Swapped': "",
            'DateCreated': datetime.today().strftime('%Y-%m-%d'),
        }
        next_uid += 1
        global_dict[next_uid] = {
            'Question': input1,
            'Answer': input2,
            'DueDate': datetime.today().strftime('%Y-%m-%d'),
            'Phase': 1,
            'Subject': chosen_subject,
            'Swapped': 'swapped',
            'DateCreated': datetime.today().strftime('%Y-%m-%d'),
        }
        print(f'Nice, new item added to {chosen_subject}')
        return True
    except ValueError:
        print("Error: Invalid input. Please enter a valid question and answer.")
        return True

def save_to_csv(filename, global_dict):
    with open(filename, 'w') as new_file:
        fieldnames = ['UID', 'Question', 'Subject', 'Answer', 'DueDate', 'Phase', 'Swapped', 'DateCreated']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=';')
        csv_writer.writeheader()

        for key, value in global_dict.items():
            value['UID'] = key
            csv_writer.writerow(value)

def main():
    quiz_on = 1

    while quiz_on == 1:
        chosen_subject = ""
        global_dict, subject_list = load_data_from_csv('sample.csv')

        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")
        print("WELCOME to the Terminal Vocabulary Trainer!")
        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")

        if not global_dict:
            print("Your vocabulary database seems to be empty 😮")
            mode = "a"
        else:
            print("OVERVIEW of your quiz items by subject")
            for key, value in subject_list.items():
                print(key, value)
            print("Do you want to quiz 'q' or add vocabulary 'a'?")
            mode = input("Enter your choice: ")

        if mode == "q":
            chosen_subject = input('Which subject do you want to practice (pick one from the list above or create a new one): ')

            open_questions = [key for key, value in global_dict.items() if value["DueDate"] != "" and value["Subject"] == chosen_subject and datetime.today() >= datetime.strptime(value["DueDate"], "%Y-%m-%d")]

            if not open_questions:
                print("The subject doesn't exist, or there are no due items.")
            else:
                message = f"Alright, Quiz with {len(open_questions)} items is generated."
                print(message)

            while len(open_questions) > 0:
                quiz_on = ask_random_question(open_questions, global_dict)
                if not quiz_on:
                    break

            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            if not quiz_on:
                print('Okay, quiz canceled.')
            else:
                print(f'Nice, you are done with your {chosen_subject} quiz for today!🎉')
            save_to_csv('sample.csv', global_dict)
            print('Your progress is saved in CSV.')
            quiz_on = int(input('Enter 1 to return to start or 0 to end: '))

        elif mode == "a":
            if not global_dict:
                print("In order to start, let's first add some new vocabulary.")
            else:
                print("Choose one of your subjects or type the name of a new one.")
            chosen_subject = input("Choose subject: ")

            while quiz_on != 0:
                quiz_on = add_item(chosen_subject, global_dict)

            save_to_csv('sample.csv', global_dict)
            print('Your progress is saved in CSV.')
            quiz_on = int(input('Enter 1 to return to start or 0 to end: '))

        else:
            print("Oops, this went wrong. Try 'a' to add vocabulary, or 'q' for quiz.")

if __name__ == '__main__':
    main()

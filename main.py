import re
from functools import partial
from operator import is_not


def read_file(file_name, output_file_name):
    result_lines = []
    with open(file_name) as file:
        datafile = file.readlines()
    for line in datafile:
        result = journal_line_handler(line)
        if result:
            result_lines.append(result)
    save_file(output_file_name, result_lines)


def save_file(file_name, lines):
    with open(file_name, 'w') as file:
        for line in lines:
            file.write(line)
            file.write("\n")


def journal_line_handler(line):
    time_race = re.search(r'(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9]', line)
    if time_race:
        time_race = time_race[0]

        race_number = re.search(r'\d\d\d', line)
        if race_number:
            race_number = race_number[0]

            if line.__contains__("прибыл"):
                found = re.search(r'(?<=прибыл).+', line)
            if line.__contains__("отправился"):
                found = re.search(r'(?<=отправился).+', line)
            if found:
                destination_words_array = found[0].replace(time_race, "").split()
                destination = destination_words_array[0] + " " + destination_words_array[1]
                return f"[{time_race}] - Поезд № {race_number} {destination}"


read_file("journal.txt", "handled_journal.txt")

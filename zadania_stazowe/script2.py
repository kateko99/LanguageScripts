import argparse
from num2words import num2words
import re

femm_dec = {'nom': 'a', 'gen': 'ej', 'dat': 'ej', 'acc': 'ą', 
'loc': 'ą', 'inst': 'ej', 'voc': 'a'}


parser = argparse.ArgumentParser(description = 'Change number to words')
parser.add_argument('input_file', type = str, help = 'Path to the file with text to change')
parser.add_argument('output_file', type = str, help = "Path to write the output file")
args = parser.parse_args()


# Function to check the case of the word 'godzina'
# # inst = the same form as dat! So it has the same name here
def check_case(text):
    result = 'nom'
    if(text == 'godziny'):
        result = 'gen'
    elif(text == 'godzinie'):
        result = 'dat'
    elif(text == 'godzinę'):
        result = 'acc'
    elif(text == 'godziną'):
        result = 'loc'
    elif(text == 'godzino'):
        result = 'voc'
    return result

# Function to generate femminile ordinal text from number
def num_to_ordinal(hours, case):
    text = num2words(hours, to='ordinal', lang='pl')
    if(hours != 3):
        text = text[:-1]
    if(hours == 2 and (case == 'gen' or case == 'dat')):
        result = text + 'i' + femm_dec[case]
    else:
        result = text + femm_dec[case]
    return result

# Function to separate hours and minutes from digital regex
def separate_time(time):
    hours = minutes = '0'

    # cut hours and minutes
    if(':' in time):
        hours = time.split(':')[0]
        minutes = time.split(':')[1]
    elif('.' in time):
        hours = time.split('.')[0]
        minutes = time.split('.')[1]
    else:
        hours = time

    # process midnight and reduce zero at the beginning
    if(hours == '00'):
        hours = '24'
    elif(hours[0] == '0'):
        hours = hours[1]
    if(len(minutes)>1 and minutes[0] == '0'):
        minutes = minutes[1]

    time_sep = [int(hours), int(minutes)]
    return time_sep


# Function to generate text from separate time depending on case
def number_to_text(time_object, case):
    hours = time_object[0]
    minutes = time_object[1]
    part1 = part2 = ''
    if(hours < 21):
        part1 = num_to_ordinal(hours, case)
    else:
        unit = hours % 10
        decimal = hours - unit
        part1 = num_to_ordinal(decimal, case) + ' ' + num_to_ordinal(unit, case)
    if(minutes != 0):
        part2 = ' ' + num2words(minutes, lang='pl')
    result = part1 + part2
    return result

# Main function to change string like 'godzina 2:34', 'godzinę 1.30' into text
def match_to_text(match):

    # check the declination (name regex)
    pattern_name = re.compile(r'(godzin)[a-ząę]+')
    x = re.search(pattern_name, match)
    name = x.group()
    case_dec = check_case(name)

    # check the number (digital regex) and separate hours/minutes
    pattern_number = re.compile(r'[0-9\.\:]+')
    y = re.search(pattern_number, match)
    number = y.group()
    time = separate_time(number)

    # create text
    result_text = number_to_text(time, case_dec)
    return result_text


# Main function to process text in files
file = open(args.input_file) 
content = file.read()
file.close()
pattern = re.compile(r'(godzin)[a-ząę]+\s+[0-9\.\:]+')
pattern_hour = re.compile(r'(godzin)[a-ząę]+')
content2 = ''

while(len(content) > 0):
    # find main pattern
    x = re.search(pattern, content)
    if x is None:
        content2 = content2 + content
        break
    match = x.group()
    lines = x.span()
    end_line = lines[0]
    start_line = lines[1]

    # check the last character and cut if is not digit
    is_digit = match[-1].isdigit()
    if not is_digit:
        start_line = start_line -1
        match = match[:-1]

    # process and save in variable
    result_fin = match_to_text(match)
    hour = re.search(pattern_hour, match)
    match_hour = hour.group()
    save_cont = content[:end_line] + match_hour + ' ' + result_fin
    content2 = content2 + save_cont
    content = content[start_line:]

file2 = open(args.output_file, 'w')
file2.write(content2)
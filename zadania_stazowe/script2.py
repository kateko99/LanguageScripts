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
# inst = the same form as dat! So it has the same name here.
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

# Function that gets a number and case, and generate femminal ordinal text
def num_to_ordinal(hour, case):
    text = num2words(hour, to='ordinal', lang='pl')
    if(hour != 3):
        text = text[:-1]
    if(hour == 2 and (case == 'gen' or case == 'dat')):
        result = text + 'i' + femm_dec[case]
    else:
        result = text + femm_dec[case]
    return result

# Function to separate hour and minutes from digital regex
def separate_time(time):
    hour = minute = '0'

    # cut hours and minutes
    if(':' in time):
        hour = time.split(':')[0]
        minute = time.split(':')[1]
    elif('.' in time):
        hour = time.split('.')[0]
        minute = time.split('.')[1]
    else:
        hour = time

    # reduce zero at the begining
    if(hour[0] == '0'):
        hour = hour[1]
    if(len(minute)>1 and minute[0] == '0'):
        minute = minute[1]

    time_sep = [int(hour), int(minute)]
    return time_sep


# Function to generate text from separate time, in base of case
def number_to_text(time_object, case):
    part1 = part2 = ''
    hour = time_object[0]
    minute = time_object[1]
    if(hour < 21):
        part1 = num_to_ordinal(hour, case)
    else:
        unit = hour % 10
        decimal = hour-unit
        part1 = num_to_ordinal(decimal, case) + ' ' + num_to_ordinal(unit, case)
    if(minute != 0):
        part2 = num2words(minute, lang='pl')
    result = part1 + ' ' + part2
    return result

# Main function to change string like 'godzina 2:34', 'godzinę 1.30' into text
def match_to_text(match):

    # Check the declination (name regex)
    pattern_name = re.compile(r'(godzin)[a-ząę]+')
    z = re.search(pattern_name, match)
    name = z.group()
    case_dec = check_case(name)

    # Check the number (digital regex) and separate hour/minutes
    pattern_number = re.compile(r'[0-9\.\:]+')
    y = re.search(pattern_number, match)
    if(y is not None):
        number = y.group()
        time = separate_time(number)

    # Create text
    result_text = number_to_text(time, case_dec)
    return result_text


# Main function to process text in files
file = open(args.input_file) 
content = file.read()
file.close()
print('Start TEST OPEN FILE')
pattern = re.compile(r'(godzin)[a-ząę]+\s+[0-9\.\:]+')
pattern_hour = re.compile(r'(godzin)[a-ząę]+')
content2 = ''

while(len(content) > 0):
    print("START INTERATION")
    x = re.search(pattern, content)
    if x is None:
        content2 = content2 + content
        break
    match = x.group()
    lines = x.span()
    end_line = lines[0]
    start_line = lines[1]
    # check the last character and cut if not digit
    is_digit = match[-1].isdigit()
    if not is_digit:
        start_line = start_line -1
        match = match[:-1]
    print(match[-1])
    result_fin = match_to_text(match)
    print("WYNIK: " + result_fin)

    # Save to variable
    p_hour = re.search(pattern_hour, match)
    match_h = p_hour.group()
    save_cont = content[:end_line] + match_h + ' ' + result_fin
    print('WYNIK: ' + save_cont)
    content2 = content2 + save_cont
    content = content[start_line:]
        
print(content2)

file2 = open(args.output_file, 'w')
file2.write(content2)
from urllib.request import urlopen
import dateutil.parser as dparser
from datetime import datetime
import re
import itertools
import math
import sys

nr_of_elements_per_row = 10
nr_of_chars_per_element = 8

def get_file():
    """Ask the user for a winsplit url and open the text version of the results"""
    link = input("Winsplit URL: ")
    if not link:
        # Just for debugging purpose, so that I don't need to write a link every time
        # link = "http://obasen.orientering.se/winsplits/online/sv/default.asp?page=table&databaseId=80953&categoryId=31"
        return

    link = link.replace("default.asp?page=table&", "export_text.asp?")
    return urlopen(link)


def get_title_and_date(first_line):
    """Parse race title and date"""
    regexp = re.compile("<TITLE>WinSplits Online - .+<\/TITLE>")
    m = regexp.search(str(first_line))
    if m:
        title = m.group(0)[26:-8]
    else:
        print(first_line)
        raise Exception("Race title not found :(")
        
    try:
        date = dparser.parse(title, fuzzy=True)
    except:
        # Sometimes the class interferes with finding the date
        regexp2 = re.compile("\[.+\]")
        m = regexp2.search(title)
        if m:
            date = dparser.parse(m.group(0), fuzzy=True)
        else:
            raise Exception("Can't find date in title")
    return title, date.strftime("%y%m%d")


def convert_str_to_times(times_list):
    """Converts a list of strings to a list of datetimes"""
    converted_times = []
    for time in times_list:
        try:
            converted_times.append(datetime.strptime(time, '%M.%S'))
        except:
            try:
                converted_times.append(datetime.strptime(time, '%H:%M.%S'))
            except:
                print("This did not work: ", time)
    return converted_times


def get_runner_data(splits_line, cumulative_line):
    """Parse all data and results for a runner, given the 2 lines from winsplit"""
    runner_data = {}

    # regexp to identify fields containing a time
    regexp = re.compile("[0-9]+\.[0-5][0-9]")

    # extract non-time fields containing position and name (filter, convert to dict to remove duplicates, and then to list)
    non_time = list(dict.fromkeys(itertools.filterfalse(regexp.search, splits_line)))
    runner_data['position'] = non_time.pop(0)
    runner_data['name'] = ' '.join([str(elem) for elem in non_time])
    
    # extract non-time fields containing club
    non_time = list(dict.fromkeys(itertools.filterfalse(regexp.search, cumulative_line)))
    runner_data['club'] = ' '.join([str(elem) for elem in non_time])

    # extract split time fields
    splits = list(filter(regexp.search, splits_line))
    runner_data['splits'] = convert_str_to_times(splits)
    # extract cumulative time fields
    cumulative = list(filter(regexp.search, cumulative_line))
    runner_data['cumulative'] = convert_str_to_times(cumulative)
        
    return runner_data


def update_best_splits(best_splits, splits):
    """Updates the best splits between best_splits and splits"""
    if len(best_splits) == 0:
        return splits[:]
    elif len(best_splits) == len(splits):
        for i in range(len(splits)):
            if(splits[i] < best_splits[i]):
                best_splits[i] = splits[i]
        return best_splits

def get_results(file):
    """Extract all results data (for each runner, the winning splits, ..."""
    results = {}
    best_splits = ""
    runners_results = []

    # Odd lines contain split, even lines contain cumulative time
    odd_line = ""
    even_line = ""
    
    # Skip the first lines until the first runner is found
    skip_line = True
    
    for line in file:
        decoded_line = line.decode("iso-8859-1")
        # Skip the lines until the first runner is listed
        if decoded_line[0] != '1' and skip_line:
            continue
        else:
            # Found the first runner
            skip_line = False

        if not odd_line:
            odd_line = decoded_line.split()
        else:
            even_line = decoded_line.split()
            current_runner = get_runner_data(odd_line, even_line)
            # Consider only classified runners
            if current_runner['position'].isnumeric():
                runners_results.append(current_runner)
                best_splits = update_best_splits(best_splits, current_runner['splits'])
            else:
                print(current_runner['position'] + " " + current_runner['name'] + " not classified, skipping it")
            # reset lines
            odd_line = ""
            even_line = ""
            
    results['best_splits'] = best_splits
    results['runners_results'] = runners_results
    results['winning_time'] = runners_results[0]['cumulative'][-1]
    
    return results


def convert_datetime_to_str(datetime):
    string = ""
    if(datetime.hour > 0):
        string += str(datetime.hour) + ":"
    if(datetime.minute < 10):
        string += "0"
    string += str(datetime.minute) + "."
    if(datetime.second < 10):
        string += "0"
    string += str(datetime.second)
    return string


def print_totals(results):
    """Print total results for each runner"""
    for runner in results['runners_results']:
        time_behind = (runner['cumulative'][-1] - results['winning_time']).seconds
        str_time_behind = str(time_behind//60) + "."
        if time_behind%60 < 10:
            str_time_behind += "0"
        str_time_behind += str(time_behind%60)
        str_total_time = convert_datetime_to_str(runner['cumulative'][-1])
        try:
            print(runner['position'] + ". " + runner['name'] + ", " + runner['club'] + ": " + str_total_time + " (+" + str_time_behind + ")")
        except UnicodeEncodeError:
            print(runner['position'] + ". Weird Name")

def print_padded_list(list):
    """Prints the list padding with whitespaces such that each element takes nr_of_chars_per_element in total"""
    print_line = ""
    for element in list:
        for i in range(nr_of_chars_per_element - len(element)):
            print_line += " "
        print_line += element
    print(print_line)        


def print_times(times):
    list_to_print = []
    for element in times:
        list_to_print.append(convert_datetime_to_str(element))
    print_padded_list(list_to_print)


def print_gaps(best_splits, splits):
    """Prints the gap to the winning split times, in seconds and percentage"""
    gap_seconds = []
    gap_percent = []
    if(len(best_splits) == len(splits)):
        for i in range(len(splits)):
            # Get gap in seconds
            delta_time = splits[i] - best_splits[i]
            actual_to_print = "+"
            actual_to_print += str(delta_time.seconds//60) + "."
            if delta_time.seconds%60 < 10:
                actual_to_print += "0"
            actual_to_print += str(delta_time.seconds%60)
            gap_seconds.append(actual_to_print)
            # Get gap in %
            actual_best_split = best_splits[i] - datetime(1900, 1, 1)
            actual_to_print = "(+"
            actual_to_print += str(math.ceil((delta_time / actual_best_split) * 100))
            actual_to_print += "%)"
            gap_percent.append(actual_to_print)
            
    print_padded_list(gap_seconds)
    print_padded_list(gap_percent)

def print_results(results):
    """Print results for each runner"""
    for runner in results['runners_results']:
        time_behind = (runner['cumulative'][-1] - results['winning_time']).seconds
        str_time_behind = str(time_behind//60) + "."
        if time_behind%60 < 10:
            str_time_behind += "0"
        str_time_behind += str(time_behind%60)
        try:
            print(runner['position'] + ". " + runner['name'] + ", " + runner['club'] + " (+" + str_time_behind + "):")
        except UnicodeEncodeError:
            print(runner['position'] + ". Weird Name:")

        for row_nr in range(math.ceil(len(runner['splits']) / nr_of_elements_per_row)):
            first_element = row_nr * nr_of_elements_per_row
            last_element = min(len(runner['splits']),(row_nr+1) * nr_of_elements_per_row)
            print_times(runner['splits'][first_element:last_element])
            print_gaps(results['best_splits'][first_element:last_element], runner['splits'][first_element:last_element])
            print_times(runner['cumulative'][first_element:last_element])
            print("")


def main():
    # Get file handle
    file = get_file()
    
    # Get date of the race, which is in the first line
    first_line = file.readline().decode("iso-8859-1")
    title, date = get_title_and_date(first_line)
    
    # Get all results
    results = get_results(file)

    # Get the desired output file name
    output_file_name = date + ".txt"
    
    # redirect stdout to my file
    stdout = sys.stdout
    sys.stdout = open(output_file_name, 'w')

    # print the title of the race, which is also contained in the first line
    print(title)
    print()
    print_totals(results)
    print()
    print_results(results)
    

    sys.stdout.close()
    sys.stdout = stdout
    
    input("Output written to " + sys.argv[0] + "\\" + output_file_name + "\nPress any key to exit...")


if __name__ == "__main__":
    main()

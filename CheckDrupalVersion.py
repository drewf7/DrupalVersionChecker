#Flashy Title TBD

import os, csv
from urllib.request import Request, urlopen

flag_txt_import = False
flag_csv_import = False
flag_txt_export = False
flag_csv_export = False



"""Correctly parses user inputed url, checks for a site's drupal version and returns it"""
def get_drupal_version_from_url(url_to_check = ""):

    if url_to_check == "":
        return "Ran with Empty or Invalid URL."

    elif not url_to_check.startswith("http"):
        """Just in case any list items were written by a human who writes doamins without 'http'"""
        url_to_check = "http://" + url_to_check

    url_to_check = url_to_check.__add__("/CHANGELOG.txt")

    try:
        url_request = Request(url_to_check)
        url_request.add_header("Range", "bytes=0-100")

        drupal_version_string = urlopen(url_request).read()

        drupal_version_string = sanitize_drupal_version_output(drupal_version_string)

    except Exception:
        drupal_version_string = "ERORR While Connecting: Likely Not A Drupal Site. "

    return drupal_version_string

""" Returns an list of each line of the document living at the path you pass it"""
def import_url_list_to_list(path_to_file, txtorcsv = True):
    if txtorcsv == True:
        flag_txt_import = True
        flag_txt_import = True

    url_list = []

    if flag_txt_import:
        print("Ran Test Import")
        with open(path_to_file) as generic_file_name:
            """
            Before we add the lines to an list, we sanatise them. Took me over an hour to figure out why there were so many line breaks in my output. Oops
            """
            generic_file_name = [x.strip() for x in generic_file_name]

            for line in generic_file_name:
                url_list.append(line)


    elif flag_csv_import:
        with open(path_to_file, 'r') as generic_file_name:
            file_reader = csv.reader(generic_file_name)
            url_list = list(file_reader)

    return url_list



"""Takes the first 100 characters of the Drupal CHANGELOG.txt page and pulls just the Drupal Version Number out"""
def sanitize_drupal_version_output(output_unsanitized):
    output_unsanitized = str(output_unsanitized).split(" ", 1)[-1]
    output_sanitized = output_unsanitized.split(",", 1)[0]

    return(output_sanitized)

"""Gets the level of configurability the user would like from the program. Returns 1 for advanced or 2 for simple"""
def menu_get_user_complexity_level():
    user_complexity_level = 0
    while True:
        print("Please Choose Your Level of Complexity")
        print("1. I am an advanced user who likes options. Let me customize everything.")
        print("2. I don't have time to deal with menu's. Make it simple.")
        user_choice = input(":")

        try:
            user_complexity_level = int(user_choice)

            if user_complexity_level == 1 or user_complexity_level == 2:
                user_complexity_level = 1
                return user_complexity_level

            else:
                print('''
ERROR: I'm sorry, I need to you respond with either the number 1, or 2.
                ''')
        except:
            print('''
ERROR: I'm sorry, I need to you respond with either the number 1, or 2.
            ''')

def menu_get_input_filetype():
    user_choice_inputtype = ""
    while True:
        print("Please Choose Your Level of Complexity")
        print("1. Text file '.txt'")
        print("2. Comma Separated Values '.csv'")
        user_choice_inputtype = input(":")

        if user_choice_inputtype == "txt":
            user_choice_inputtype = "1"
        elif user_choice_inputtype == "csv":
            user_choice_inputtype = "2"

        if user_choice_inputtype == "1" or user_choice_inputtype == "2":
            return user_choice_inputtype

        else:
            print('''
    ERROR: I'm sorry, I didn't understand your answer.
                    ''')

"""Attempts to import a list of urls from a file into an list. Returns the List."""
def menu_get_input_url_list(user_complexity_level):
    print('''
****************************
*Step 1: Importing URL List*
****************************
    ''')
    if user_complexity_level == 1:
        user_input_file_choice = menu_get_input_filetype()
        if user_input_file_choice == "1":
            flag_txt_import = True
            flag_csv_import = False
        else:
            flag_csv_import = True
            flag_txt_import = False


    else:
        flag_txt_import = True

    print("Please provide the file path to your URL list.")
    if flag_txt_import:
        print("Your Selected file type is a text file.")
        print("Please provide the filename (if file is in the current directory) or path to your input file")
        print("NOTE: URL's should be formated one to a line")
        print("----------")
        print("For reference, your current (and default) directory is: " + str(os.getcwd()))
        print("----------")
        while True:
            user_input_directory = input(":")

            """Sanitization"""
            if not user_input_directory.endswith(".txt"):
                user_input_directory = user_input_directory + ".txt"

            """If we don't think the user has supplied a path, supply it for them"""
            if "/" not in user_input_directory:
                user_input_directory = str(os.getcwd()) + '\\' + user_input_directory

            if (os.path.isfile(user_input_directory)):
                break
            else:
                print("I thought you were oging to: " + user_input_directory)
                print('''
                ERROR: Invalid File Path. Please try again.
                            ''')
    elif flag_csv_import:
        print("Your selected file type is a csv file")
        print("Please provide the filename (if file is in the current directory) or path to your input file")
        print("NOTE: URL's should be separated by a single comma")
        print("----------")
        print("For reference, your current (and default) directory is: " + str(os.getcwd()))
        print("----------")
        while True:
            user_input_directory = input(":")

            """Sanitization"""
            if not user_input_directory.endswith(".csv"):
                user_input_directory = user_input_directory + ".csv"

            """If we don't think the user has supplied a path, supply it for them"""
            if "/" not in user_input_directory:
                user_input_directory = str(os.getcwd()) + '\\' + user_input_directory

            if (os.path.isfile(user_input_directory)):
                break
            else:
                print("I thought you were oging to: " + user_input_directory)
                print('''
                        ERROR: Invalid File Path. Please try again.
                                    ''')

    temp_url_list_var = import_url_list_to_list(user_input_directory)
    return temp_url_list_var




print('''
***************************************************************************
*Welcome to Drew's Overly Flashy/Overly Complicated Drupal Version Checker*
***************************************************************************
    ''')

user_current_complexity = menu_get_user_complexity_level()

while True:
    urls_to_parse = menu_get_input_url_list(user_current_complexity)

    print('''
******************************************
*Checking Drupal Versions: Please Wait...*
******************************************
    ''')

    output_drupal_versions_list = []
    for i in range(len(urls_to_parse)):
        print("Currently Checking Drupal Version For: "+urls_to_parse[i])
        output_drupal_versions_list.append(urls_to_parse[i] + "| Drupal Version: " + get_drupal_version_from_url(urls_to_parse[i]))

    print('''
*********************************
*Step 2: Select Export File Name*
*********************************
Please type what you would like the name of the output file to be.
NOTE: This file will be created in the current working directory unless otherwise specified
    ''')

    user_output_directory = input(":")
    """Sanitization Always"""
    if not user_output_directory.endswith(".txt"):
        user_output_directory = user_output_directory + ".txt"

    output_file = open(user_output_directory, "w")
    for item in output_drupal_versions_list:
        output_file.write("%s\n" % item)

    output_file.close()
    break

#Flashy Title TBD

import os
from urllib.request import Request, urlopen


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

""" Returns an array of each line of the document living at the path you pass it"""
def import_url_list_to_array(path_to_file):

    url_array = []

    with open(path_to_file) as generic_file_name:
        """
        Before we add the lines to an array, we sanatise them. Took me over an hour to figure out why there were so many line breaks in my output. Oops
        """
        generic_file_name = [x.strip() for x in generic_file_name]

        for line in generic_file_name:
            url_array.append(line)

        return url_array

"""Takes the first 100 characters of the Drupal CHANGELOG.txt page and pulls just the Drupal Version Number out"""
def sanitize_drupal_version_output(output_unsanitized):
    output_unsanitized = str(output_unsanitized).split(" ", 1)[-1]
    output_sanitized = output_unsanitized.split(",", 1)[0]

    return(output_sanitized)

print('''
***************************************************************************
*Welcome to Drew's Overly Flashy/Overly Complicated Drupal Version Checker*
***************************************************************************
''')

"""
'''Difficulty Settings'''
user_complexity_level = 0
while True:
    print("Please Choose Your Level of Complexity")
    print("1. I am an advanced user who likes options. Let me customize everything.")
    print("2. I don't have time to deal with menu's. Make it simple.")
    user_choice = input(":")

    try:
        user_complexity_level = int(user_choice)

        if user_complexity_level == 1 or user_complexity_level == 2:
            break

        else:
            print('''
ERROR: I'm sorry, I need to you respond with either the number 1, or 2.
            ''')
    except:
        print('''
ERROR: I'm sorry, I need to you respond with either the number 1, or 2.
        ''')
"""

while True:
    while True:
        print('''
****************************
*Step 1: Importing URL List*
****************************
Please provide the file path to your URL list. 
NOTE: URLs whould be formatted one per line.
''')
        print("For reference, your current (and default) directory is: "+ str(os.getcwd()))
        user_input_directory = input(":")

        """Sanitization"""
        if not user_input_directory.endswith(".txt"):
            user_input_directory = user_input_directory + ".txt"

        """If we don't think the user has supplied a path, supply it for them"""
        if "/" not in user_input_directory:
            user_input_directory = str(os.getcwd()) + '\\' + user_input_directory

        if(os.path.isfile(user_input_directory)):
            break
        else:
            print("I thought you were oging to: " + user_input_directory)
            print('''
ERROR: Invalid File Path. Please try again.
            ''')

    user_given_url_array = import_url_list_to_array(user_input_directory)
    print('''
******************************************
*Checking Drupal Versions: Please Wait...*
******************************************
    ''')

    output_drupal_versions_array = []
    for i in range(len(user_given_url_array)):
        output_drupal_versions_array.append(user_given_url_array[i] + "| Drupal Version: " + get_drupal_version_from_url(user_given_url_array[i]))

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
    for item in output_drupal_versions_array:
        output_file.write("%s\n" % item)

    output_file.close()
    break
import os, sys, hashlib, shutil, urllib.request


def get_drupal_version_from_hash_d8(url_to_check = ""):
    
    drupal_version_string = ""

    if url_to_check == "":
        return "Ran with Empty or Invalid URL."

    elif not url_to_check.startswith("http"):
        """Just in case any list items were written by a human who writes doamins without 'http'"""
        url_to_check = "http://" + url_to_check

    url_to_check = url_to_check.__add__("/core/misc/drupal.js")
    try:
        file_save_name = url_to_check.replace('/','')
        file_save_name = file_save_name.replace('http:','')
        with urllib.request.urlopen(url_to_check) as drupal_js_file, open ('tmp/d8/'+file_save_name, 'wb') as out_file:
            shutil.copyfileobj(drupal_js_file, out_file)

        drupal_js_md5 = md5('tmp/d8/'+file_save_name)

        drupal_version_string = drupal_versions_from_hash_d8(drupal_js_md5)

        out_file.close()

    except Exception:
        return "Could not find drupal.js file: Not a Drupal Site"

    return drupal_version_string

def drupal_versions_from_hash_d8(md5_hash):
    return {
        '3dcbe8b1280a271797fe4f1dd5700d0c' : '8.0.0 - 8.0.5',
        '714d7aeb86ea12acc0de88e2b135f14d' : '8.1.0 - 8.2.6',
        '0e18a6096f1a222fab718c153266444a' : '8.3.0 - 8.3.7',
        '423a643a05f801dea5358481e56d83d7' : '8.4.0 - 8.4.4',
        '767df16aa36ccaa000a195ff5680a9c2' : '8.4.5',
        '71bfba813a9f85564220f8e9a1b06da4' : '8.5.1',
    }.get(md5_hash, "Error While Hashing drupal.js file. URL is likely a redirect, or site is a non-Drupal CMS")

def get_drupal_version_from_hash(url_to_check = ""):

    drupal_version_string = ""

    if url_to_check == "":
        return "Ran with Empty or Invalid URL."

    elif not url_to_check.startswith("http"):
        """Just in case any list items were written by a human who writes doamins without 'http'"""
        url_to_check = "http://" + url_to_check

    url_to_check = url_to_check.__add__("/misc/drupal.js")
    try:
        file_save_name = url_to_check.replace('/','')
        file_save_name = file_save_name.replace('http:','')
        with urllib.request.urlopen(url_to_check) as drupal_js_file, open ('tmp/'+file_save_name, 'wb') as out_file:
            shutil.copyfileobj(drupal_js_file, out_file)

        drupal_js_md5 = md5('tmp/'+file_save_name)

        drupal_version_string = drupal_versions_from_hash(drupal_js_md5)

        out_file.close()

    except Exception:
        return "Could not find drupal.js file: Not a Drupal 6 or 7 Site"

    return drupal_version_string
    
def drupal_versions_from_hash(md5_hash):
    return {
        '2ff7dc985e57d1139ce4dc844b06bc64' : '6.1 - 6.2',
        '398b3832c2de0a0ebd08cb7f2afe1545' : '6.3 - 6.13',
        '88682723723be277fb57c0d8e341c0cf' : '6.14 - 6.20',
        '9a1c645566d780facee5ce1a0d3fab7c' : '6.21',
        'fe6f8c678cb511d68a3dbe5a94f2e278' : '6.22 - 6.23',
        '90c0aa7ed8581884c2afe73fc87b5697' : '6.24 - 6.27',
        '1904f6fd4a4fe747d6b53ca9fd81f848' : '6.28 - 6.38',
        '847afc6e14d280e66a564194e166a66e' : '7.0',
        'f3f32021901f4c33d2eebbc634de587d' : '7.1',
        'cea76de12c5bb95dd0789fbd3cd754f0' : '7.2 - 7.3',
        'cea76de12c5bb95dd0789fbd3cd754f0' : '7.4 - 7.8',
        'd4515f21acd461ca04304233bf0daa1e' : '7.9',
        'cbd95e04bad1be13320ebbe63a863245' : '7.10',
        'd4515f21acd461ca04304233bf0daa1e' : '7.11',
        'f9281a1fa8b926ba038bebc3bb0c3d61' : '7.12 - 7.18',
        '0bb055ea361b208072be45e8e004117b' : '7.19 - 7.38',
        'bb9f18fb7a42b95fcad87b98dbb19c87' : '7.39 - 7.50',
        'acf092762cf1cf821a12325fbf494ecf' : '7.51 - 7.54',
        'ce89aafcde644262269009c10d8a9cd2' : '7.55 - 7.56',
        'a4065c93addf975e695586c24a20bda8' : '7.57 - 7.58',
    }.get(md5_hash, "Error While Hashing drupal.js file. URL is likely a redirect, or site is a non-Drupal CMS")

"""Correctly parses user inputed url, checks for a site's drupal version and returns it"""
def get_drupal_version_from_url(url_to_check = ""):
    if url_to_check == "":
        return "Ran with Empty or Invalid URL."

    elif not url_to_check.startswith("http"):
        """Just in case any list items were written by a human who writes doamins without 'http'"""
        url_to_check = "http://" + url_to_check

    url_to_check = url_to_check.__add__("/CHANGELOG.txt")

    try:
        url_request = urllib.request.Request(url_to_check)
        url_request.add_header("Range", "bytes=0-100")

        drupal_version_string = urllib.request.urlopen(url_request).read()
        drupal_version_string = sanitize_drupal_version_output(drupal_version_string)
        try:
            """The reason for this is that for some reason 404 pages still count as a valid return. 
            So we perform a sanity check to ensure that the Drupal version number is actually a number."""
            float(drupal_version_string)
        except Exception:
            drupal_version_string = "ERORR While Connecting: Likely Not A Drupal Site."

    except Exception:
        drupal_version_string = "ERORR While Connecting: Likely Not A Drupal Site."

    return drupal_version_string

"""Takes the first 100 characters of the Drupal CHANGELOG.txt page and pulls just the Drupal Version Number out"""
def sanitize_drupal_version_output(output_unsanitized):
    output_unsanitized = str(output_unsanitized).split(" ", 1)[-1]
    output_sanitized = output_unsanitized.split(",", 1)[0]

    return(output_sanitized)

""" Returns md5 hash of supplied file"""
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

""" Returns an list of each line of the document living at the path you pass it"""
def import_url_list_to_list(path_to_file):

    url_list = []

    try:
        with open(path_to_file) as generic_file_name:
            """
            Before we add the lines to an list, we sanatise them.
            """
            generic_file_name = [x.strip() for x in generic_file_name]

            for line in generic_file_name:
                url_list.append(line)
    except:
        url_list[0] = "Error Opening File"

    return url_list


while True:
    if (len(sys.argv) == 1):
        print("""
========================================================
=        Drew's Drupal Version Checker Usage           =
========================================================
1. "python3 DrupalVersionChecker.py www.MYURL.com"
2. "python3 DrupalVersionChecker.py -f MYTEXTFILE.txt"

The formating of the text file should be one url per line"""
        )
        break

    elif (str(sys.argv[1]) == "-f"):
        output_version_list = []
        
        """Sanitization Always"""
        if not sys.argv[2].endswith(".txt"):
            sys.argv[2] = sys.argv[2] + ".txt"

        sites_to_check = import_url_list_to_list(str(sys.argv[2]))

        if (sites_to_check[0] == "Error Opening File"):
            print("""
========================================================
=        Error Opening File at Supplied Path           =
=                 Proper Usage is:                     =
========================================================
1. "python3 DrupalVersionChecker.py www.MYURL.com"
2. "python3 DrupalVersionChecker.py -f MYTEXTFILE.txt"

The formating of the text file should be one url per line"""
            )
            break
        try:
            os.stat('tmp')
        except:
            os.mkdir('tmp')
        for i in range(len(sites_to_check)):
            print("Currently Checking Drupal Version For: "+sites_to_check[i])
            return_text = get_drupal_version_from_url(sites_to_check[i])
            if return_text == "ERORR While Connecting: Likely Not A Drupal Site.":
                return_text = get_drupal_version_from_hash(sites_to_check[i])
            if return_text == "Could not find drupal.js file: Not a Drupal 6 or 7 Site" or return_text == "Error While Hashing drupal.js file. URL is likely a redirect, or site is a non-Drupal CMS":
                return_text = get_drupal_version_from_hash_d8(sites_to_check[i])
        
            output_version_list.append(return_text)
        shutil.rmtree('tmp')
        
        print('''
===================================
= Step 2: Select Export File Name =
===================================
Please type what you would like the name of the output file to be.
NOTE: This file will be created in the current working directory unless otherwise specified
    ''')

        user_output_directory = input(":")
        """Sanitization Always"""
        if not user_output_directory.endswith(".txt"):
            user_output_directory = user_output_directory + ".txt"

        output_file = open(user_output_directory, "w")
        for item in output_version_list:
            output_file.write("%s\n" % item)

        output_file.close()
        break

    else:
        try:
            os.stat('tmp')
        except:
            os.mkdir('tmp')
        try:
            return_text = get_drupal_version_from_url(str(sys.argv[1]))
            if return_text == "ERORR While Connecting: Likely Not A Drupal Site.":
                return_text = get_drupal_version_from_hash(str(sys.argv[1]))
            if return_text == "Could not find drupal.js file: Not a Drupal 6 or 7 Site" or return_text == "Error While Hashing drupal.js file. URL is likely a redirect, or site is a non-Drupal CMS":
                return_text = get_drupal_version_from_hash_d8(str(sys.argv[1]))
            
            print("Drupal Version For "+sys.argv[1]+": "+return_text)
        except Exception:
            print("""
========================================================
=        Error Opening File at Supplied Path           =
=                 Proper Usage is:                     =
========================================================
1. "python3 DrupalVersionChecker.py www.MYURL.com"
2. "python3 DrupalVersionChecker.py -f MYTEXTFILE.txt"

The formating of the text file should be one url per line"""
            )
        shutil.rmtree('tmp')
        break
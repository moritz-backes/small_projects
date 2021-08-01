#! python3
# sorting_bank.documents.py - This program sorts my bank documents by date and by
# wether they are for the credit card or the debit card

from pathlib import Path
import os, pprint, re, pdfplumber, shutil

# this asks the user for a path as input and then finds all files in that given path
#TODO: only find .pdf files
def pdf_finder():
    print('Please enter the filepath where the documents are saved.')
    os.chdir(input())
    path = Path.cwd()
    return [x for x in path.iterdir() if x.is_file()], path


#TODO: open the files and save the content of the first page in a list
def pdf_opener(file):
    pdf = pdfplumber.open(file)
    page = pdf.pages[0]
    page = page.extract_text()
    pdf.close()
    return page


#TODO: find our which class they belong to and which month by using regexes on the created list
# of pages
def class_and_date(text):
    kontoauszug_regex = re.compile(r'''(
            Kontoauszug|Umsatzaufstellung
            )''', re.VERBOSE)

    datum_regex = re.compile(r'''(
             (0[0-9]|[12][0-9]|3[01])
             \.
             (0[0-9]|1[012])
             \.
             ((?:20)\d\d)
             )''', re.VERBOSE)

    date = datum_regex.search(text)
    day, month, year = date.group(2, 3, 4)
    #print(day, month, year)
    info = kontoauszug_regex.search(text)
    auszug = (info.group(0))
    return day, month, year, auszug

def folder_checker_creator(year, auszug):
    if auszug == 'Umsatzaufstellung':
        path_to_check = Path(r'C:\Users\morit\Google Drive\Banking') / 'Kreditkarte' / year
        if path_to_check.is_dir() != True:
            path_to_check.mkdir(parents=True, exist_ok=False)
            #print('Der Ordner ' + path_to_check + ' wurde neu erstellt.')
    if auszug == 'Kontoauszug':
        path_to_check = Path(r'C:\Users\morit\Google Drive\Banking') / 'Kontoauszüge' / year
        if path_to_check.is_dir() != True:
            path_to_check.mkdir(parents=True, exist_ok=False)
            #print('Der Ordner ' + path_to_check + ' wurde neu erstellt.')

def pdf_renamer(month, year, auszug, file):
    if auszug == 'Umsatzaufstellung':
        new_month = int(month) - 1
        new_month_string = f'{new_month:02d}'
        new_name = (year + '-' + new_month_string + file.suffix)
        new_path = Path(r'C:\Users\morit\Google Drive\Banking') / 'Kreditkarte' / year / new_name
        shutil.move(file, new_path)
        #print(new_name + ' wurde in den Ordner ' + new_path + ' verschoben!')
    if auszug == 'Kontoauszug':
        new_name = (year + '-' + month + file.suffix)
        new_path = Path(r'C:\Users\morit\Google Drive\Banking') / 'Kontoauszüge' / year / new_name
        shutil.move(file, new_path)
        #print(new_name + ' wurde in den Ordner ' + new_path + ' verschoben!')

def sorting_bank_documents():
    file_list, path = pdf_finder()
    #print(pdf_finder())
    for file in file_list:
        print(path)
        print(file)
        text = pdf_opener(file)
        day, month, year, auszug = class_and_date(text)
        folder_checker_creator(year, auszug)
        pdf_renamer(month, year, auszug, file)

sorting_bank_documents()



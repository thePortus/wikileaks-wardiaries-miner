from bs4 import BeautifulSoup, NavigableString, Tag
import os
import csv

field_list = ['ReportKey', 'Date', 'Type', 'Category', 'Tracking number', 'Summary', 'Region', 'Attack on', 'Complex atack', 'Reporting unit', 'Unit name', 'Type of unit', 'FriendlyKIA', 'FriendlyWIA', 'HostNationKIA', 'HostNationWIA', 'CivilianKIA', 'CivilianWIA', 'EnemyKIA', 'EnemyWIA', 'Detained', 'MGRS', 'Latitude', 'Longitude', 'Originator group', 'Updated by group', 'CCIR', 'Sigact', 'Affiliation', 'DColor','ReferenceID']
output_file_name = 'extracted_data.csv'

"""
=====FUNCTIONS=====
"""

#This function receives an html page parsed into a soup and extracts the data, returning it as a dictionary
def make_record(page_soup):
    return_record = {}

    #Grabbing wrapper elements for page data off of the souped html
    report_details = page_soup.find_all("code")
    report_message_wrapper = report_details[0]
    detailed_report_wrapper = report_details[1]

    #Grabbing the table elements
    report_tables = page_soup.find_all("table")
    report_table_2 = report_tables[0]
    report_table_1 = report_tables[1]
    report_table_3 = report_tables[2]

    #Grabbing the individual data rows from their respective table elements
    report_row_2 = report_table_2.find_all("tr")[1]
    report_row_1 = report_table_1.find_all("tr")[1]
    report_row_3 = report_table_3.find_all("tr")
    report_row_3a = report_row_3[1]
    report_row_3b = report_row_3[2]

    #Getting the cells in rows
    report_row_cells_2 = report_row_2.find_all("td")
    report_row_cells_1 = report_row_1.find_all("td")
    report_row_cells_3a = report_row_3a.find_all("td")
    report_row_cells_3b = report_row_3b.find_all("td")

    #Extracting the text data of individual cells from their respective row elements
    return_record['ReportKey'] = report_row_cells_2[0].get_text()
    return_record['Region'] = report_row_cells_2[1].get_text()
    return_record['Latitude'] = report_row_cells_2[2].get_text()
    return_record['Longitude'] = report_row_cells_2[3].get_text()
    return_record['Date'] = report_row_cells_1[0].get_text()
    return_record['Type'] = report_row_cells_1[1].get_text()
    return_record['Category'] = report_row_cells_1[2].get_text()
    return_record['Affiliation'] = report_row_cells_1[3].get_text()
    return_record['Detained'] = report_row_cells_1[4].get_text()
    return_record['EnemyKIA'] = report_row_cells_3a[1].get_text()
    return_record['FriendlyKIA'] = report_row_cells_3a[2].get_text()
    return_record['CivilianKIA'] = report_row_cells_3a[3].get_text()
    return_record['HostNationKIA'] = report_row_cells_3a[4].get_text()
    return_record['EnemyWIA'] = report_row_cells_3b[1].get_text()
    return_record['FriendlyWIA'] = report_row_cells_3b[2].get_text()
    return_record['CivilianWIA'] = report_row_cells_3b[3].get_text()
    return_record['HostNationWIA'] = report_row_cells_3b[4].get_text()

    #Adding on the unparsed general message
    return_record['Summary'] = report_message_wrapper.get_text()

    #Parsing the <br> separated detailed data at page bottom and updating the dictionary with the result
    return_record.update(parse_detailed_summary(detailed_report_wrapper.find("pre")))

    #Sending back the record as a dictionary
    return return_record

def parse_detail_line(detail_string):
    detail_object = {'field_name': '','data':''}
    delimiter_found = False

    for char in detail_string:
        if char == ':':
            delimiter_found = True
            continue
        elif delimiter_found == False:
            detail_object['field_name'] += char
        elif delimiter_found == True:
            detail_object['data'] += char

    return detail_object


def parse_detailed_summary(detail_sum):
    parsed_line_objects = []
    detail_dictionary = {}

    for br in detail_sum.find_all('br'):

        next = br.next_sibling

        if not (next and isinstance(next, NavigableString)):
            continue

        next2 = next.next_sibling

        if next2 and isinstance(next2,Tag) and next2.name == "br":
            text = str(next).strip()

            if text:
                parsed_line_objects.append(parse_detail_line(text))

    for item in parsed_line_objects:
        detail_dictionary[item['field_name']] = item['data']

    return detail_dictionary

#This function processes all files in the folder and subfolders where the script is run, it returns a list of
#dictionaries, each entry representing the data from one page.
def soup_files_by_extension(file_extension):
    total_files = 0
    file_count = 0
    return_records = []

    print('Scanning...', end='')

    #Scanning the directory and all subdirectories to get a count of all files of the correct extension
    for dirpath, dirs, files in os.walk(os.getcwd()):
        for file in files:
            #Excluding files not matching the specified extension
            if file_extension == None or str.endswith(file, '.' + file_extension):
                total_files += 1
            if total_files % 10000 == 0:
                print('.', end='')

    print('Total number of files to convert: ', total_files)

    #Restarting the recursive directory crawl to process the found files
    for dirpath, dirs, files in os.walk(os.getcwd()):

        #Processing individual files found in the walk
        for file in files:

            #Excluding files not matching the specified extension
            if file_extension == None or str.endswith(file, '.' + file_extension):

                #Building the full file path by joining the directory path with the filename
                soup_filepath = os.path.join(dirpath, file)

                #Reading the file to file_content and closing the file to free memory
                file_object = open(soup_filepath, "r")
                file_content = file_object.read()
                file_object.close()

                #Souping file contents and appending extracted data to return records
                souped_file = BeautifulSoup(file_content, "html.parser")
                data_extract = make_record(souped_file)
                return_records.append(data_extract)
                #Incrementing file count variable
                file_count += 1

                #Giving the user a progress update
                if file_count % 10 == 0:
                    progress = (file_count/total_files) * 100
                    progress = format(progress, '.2f')
                    print('Processing file #' + str(file_count) + '/' + str(total_files) + ' - ' + str(progress) + '% - ' + soup_filepath)

    print('Total Files Processed: ' + str(file_count))
    return return_records

def write_to_csv(data_records):
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_list, quotechar='"')
        writer.writeheader()
        for data_record in data_records:
            writer.writerow(data_record)

"""
=====MAIN SCRIPT=====
"""

print('Processing files...')
extracted_data = soup_files_by_extension('html')
print('Data extraction success!')

print('Writing to CSV...')
write_to_csv(extracted_data)
print('Finished writing to CSV')

quit()

#!/usr/bin/env python

import csv # write and read csv file
import requests # make requests to REST API
import os  # manipulating file paths
import json  # converting string value to json
import sys # stop script


URL = 'http://127.0.0.1:5000/employees'


option = False

while option not in [1, 2, 3]:
    option = int(input(
    """
       Hello, this is a script which one can help you to upload or
       download data from my Employee Registry Service

       Please choose an option below:

       1. Upload new emploees from .CSV file to Employee Registry Service.
       2. Download employees from Employee Registry Service to .CSV file.
       3. Exit

    """
    ))

if option == 1:
    file_path = input("Give me a file path:")
    os.path.exists(file_path)

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employee = {
                'name': row['name'],
                'last_name': row['last_name'],
                'birth_date': row['birth_date'],
            }
            requests.post(URL, data = employee)

    print('Data uploaded!')

if option == 2:
    response = requests.get(URL)
    parsed = json.loads(response.text)
    data = parsed["data"]

    with open('downloaded_data.csv', mode='w') as employee_file:
        employee_writer = csv.writer(
            employee_file, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for row in data:
            employee_writer.writerow([
                row['name'],
                row['last_name'],
                row['birth_date']
            ])

    print('Data downloaded into downloaded_data.csv')

else:
    sys.exit("Script stopped")

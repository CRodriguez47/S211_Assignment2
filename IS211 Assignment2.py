import sys
import logging
import datetime
import ssl
import urllib.request

URL = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"

def download_data(url):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(url, context=context)
    return response.read().decode('utf-8')

def process_data(file_contents):
    data_dict = {}
    logger = logging.getLogger('assignment2')
    lines = file_contents.splitlines()
    header_skipped = False
    for line_number, line in enumerate(lines, start=1):
        if not header_skipped and "id" in line.lower():
            header_skipped = True
            continue
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) < 3:
            continue
        person_id = parts[0].strip()
        name = parts[1].strip()
        birthday_str = parts[2].strip()
        try:
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y")
        except ValueError:
            logger.error("Error processing line #%d for ID #%s", line_number, person_id)
            continue
        data_dict[person_id] = (name, birthday)
    return data_dict

def display_person(person_id, person_data):
    key = str(person_id)
    if key not in person_data:
        print("No user found with that id")
    else:
        name, birthday = person_data[key]
        formatted_date = birthday.strftime("%Y-%m-%d")
        print("Person #{} is {} with a birthday of {}".format(person_id, name, formatted_date))

def main():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler('error.log')
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    try:
        csv_data = download_data(URL)
    except Exception as e:
        print("Error downloading data: {}".format(e))
        sys.exit(0)

    person_data = process_data(csv_data)

    while True:
        try:
            user_input = input("Enter a person ID to lookup (negative number or 0 to exit): ")
            person_id = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        if person_id <= 0:
            break

        display_person(person_id, person_data)

    sys.exit(0)

if __name__ == '__main__':
    main()

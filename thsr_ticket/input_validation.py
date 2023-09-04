from datetime import datetime
import re

STATION_MIN = 1
STATION_MAX = 12
TIME_MIN = 1
TIME_MAX = 38

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    try:
        time_num = int(time_str)
        return TIME_MIN <= time_num <= TIME_MAX
    except ValueError:
        return False

def is_valid_station(station_str):
    try:
        station_num = int(station_str)
        return STATION_MIN <= station_num <= STATION_MAX
    except ValueError:
        return False
    
def is_valid_email(email_str):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email_str)

def get_valid_input(prompt, validation_function, error_message):
    while True:
        user_input = input(prompt)
        if validation_function(user_input):
            return user_input
        else:
            print(error_message)

def input_profile():
    profile = {}

    profile['start_station'] = get_valid_input(
        "Please enter the start station number (1-12): ",
        is_valid_station,
        "Invalid station number, please try again."
    )

    profile['dest_station'] = get_valid_input(
        "Please enter the destination station number (1-12): ",
        is_valid_station,
        "Invalid station number, please try again."
    )

    profile['date'] = get_valid_input(
        "Please enter the date (YYYY-MM-DD): ",
        is_valid_date,
        "Invalid date format, please try again."
    )

    '''
        '1':  '1201A', '2':  '1230A', '3':  '600A',  '4': '630A',   '5':  '700A',
        '6':  '730A',  '7':  '800A',  '8':  '830A',  '9': '900A',   '10': '930A',
        '11': '1000A', '12': '1030A', '13': '1100A', '14': '1130A', '15': '1200N',
        '16': '1230P', '17': '100P',  '18': '130P',  '19': '200P',  '20': '230P',
        '21': '300P',  '22': '330P',  '23': '400P',  '24': '430P',  '25': '500P',
        '26': '530P',  '27': '600P',  '28': '630P',  '29': '700P',  '30': '730P',
        '31': '800P',  '32': '830P',  '33': '900P',  '34': '930P',  '35': '1000P',
        '36': '1030P', '37': '1100P', '38': '1130P'
    '''
    profile['time'] = get_valid_input(
        "Please enter the time number (1-38): ",
        is_valid_time,
        "Invalid time number, please try again."
    )

    profile['ID_number'] = input("Please enter your ID number: ")
    profile['phone_number'] = input("Please enter your phone number: ")
    
    while True:
        profile['email_address'] = input("Please enter your email address: ")
        if is_valid_email(profile['email_address']):
            break
        else:
            print("Invalid email address format, please try again.")

    return profile

if __name__ == "__main__":
    user_profile = input_profile()
    print("User Profile:", user_profile)
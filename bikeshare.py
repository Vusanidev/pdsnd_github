import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6
}

DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
]


def get_city_filter():
    while True:
        city = input('Which city do you want to see data for between Chicago, New York City, Washington? : ')
        city = city.lower()
        if city in CITY_DATA:
            confirm = input(f'\nYou requested to see data for {city}. Is that correct? (Yes/No): ')
            if confirm.lower() in ['yes', 'y']:
                return city
            elif confirm.lower() in ['no', 'n']:
                print('Please enter a different city.\n')
            else:
                print('Invalid choice. Please enter Yes or No.\n')
        else:
            print('Invalid city. Please enter a valid city.\n')


def get_filter_choice():
    while True:
        choice = input('Would you like to filter your data by month, day, or not at all? : ')
        choice = choice.lower()
        if choice in ['month', 'day', 'not at all']:
            return choice
        else:
            print('Invalid choice. Please enter month, day, or not at all.\n')


def get_month():
    while True:
        month = input('Please enter a month between January and June: ')
        month = month.lower()
        if month in MONTHS:
            return month
        else:
            print('Invalid month. Please enter a valid month.\n')


def get_day():
    while True:
        day = input('Please enter a day of the week: ')
        day = day.lower()
        if day in DAYS:
            return day
        else:
            print('Invalid day. Please enter a valid day of the week.\n')


def load_data(city):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start-End Station'] = df['Start Station'] + '-' + df['End Station']
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    return df


def apply_month_filter(df, month):
    filtered_df = df[df['Month'] == MONTHS[month]]
    return filtered_df


def apply_day_filter(df, day):
    filtered_df = df[df['Day'].str.lower() == day.lower()]
    return filtered_df


def get_statistics(df):
    print('\n----------Popular times of travel----------\n')

    common_month = df['Month'].mode()[0]
    month_name = list(MONTHS.keys())[list(MONTHS.values()).index(common_month)]
    print('The most common month for the specified filters is', month_name)

    common_day = df['Day'].mode()[0]
    print('The most common day for the specified filters is', common_day)

    common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour for the specified filters is', common_hour)


def main():
    city = get_city_filter()
    choice = get_filter_choice()

    if choice == 'month':
        month = get_month()
        df = load_data(city)
        filtered_df = apply_month_filter(df, month)
        get_statistics(filtered_df)
    elif choice == 'day':
        day = get_day()
        df = load_data(city)
        filtered_df = apply_day_filter(df, day)
        get_statistics(filtered_df)
    else:
        df = load_data(city)
        get_statistics(df)


if __name__ == '__main__':
    main()

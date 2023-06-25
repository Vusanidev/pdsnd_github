import time
import pandas as pd
import numpy as np

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
        city = input(
            'Which city do you want to see data for between chicago, new york city, washington? : '
        )
        if city.lower() in CITY_DATA:
            print(f'\nYou requested to see data for {city.lower()}. Is that correct? \n')
            choice = input('Yes / No: ')

            if choice.lower() == 'yes' or choice.lower() == 'y':
                print('\n')
                break
            elif choice.lower() == 'no' or choice.lower() == 'n':
                print('Please enter a different city. \n')
                print('\n')
            else:
                print('\n Invalid choice. Please enter Yes or No. \n')
        else:
            print('\nInvalid city. Please enter a valid city. \n')
    return city


def get_filter(choice):
    while True:
        if choice in MONTHS:
            month = input("\nPlease enter month between January and June :")
        if month.lower() in MONTHS:
            return month
        if choice.lower() in DAYS:
            return month
        else:
            print('\nPlease enter a vaild month. \n')


def load_data(city, filter):
    df = pd.read_csv(CITY_DATA[city])
    pd.set_option('display.max_columns', None)
    # print(df.head())

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start-End Station'] = (df['Start Station'] + '-' + df['End Station'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    if filter in MONTHS:
        filtered_df = df[df['Month'] == filter]
        return filtered_df
    if filter in DAYS:
        filtered_df = df[df['Day'].str.lower() == filter.lower()]
        return filtered_df
    # print(df.head())
    else:
        return df


def get_statistics(filtered_df):
    """"""

    print("\n----------Popular times of travel---------\n")
    # filtered_df = df[df['Month'] == month]
    # print(filtered_df)
    print(filtered_df.head())

    # most common month
    common_month = filtered_df['Month'].mode()[0]
    month_name = list(MONTHS.keys())[list(MONTHS.values()).index(common_month)]
    print("The most common month for the filters you have specified is ", month_name)

    # most common day of week
    common_day = filtered_df['Day'].mode()[0]
    print("The most common day for the filters you have specified is ",
          common_day)

    # most common hour of day
    common_hour = filtered_df['Start Hour'].mode()[0]
    print('The most common hour for the filters you have specified is ',
          common_hour)
    print("\n----------End of Popular times of travel---------\n")
    print("\n----------Most popular stations and trip---------\n")
    # most common start station
    common_start_station = filtered_df['Start Station'].mode()[0]
    print('The most common start station for the specified filters is', common_start_station)

    # most common end station
    common_end_station = filtered_df['End Station'].mode()[0]
    print('The most common end station for the specified filters   is ', common_end_station)

    # most common start-end station
    common_start_end_station = filtered_df['Start-End Station'].mode()[0]
    print('The most common start-end station for the specified filters is ', common_start_end_station)

    print("\n----------End of most popular stations and trip---------\n")

    print("\n----------Calculating Trip Duration---------\n")

    total_travel_time = filtered_df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time // 86400)) +
                         'd ' + str(int((total_travel_time % 86400) // 3600)) + 'h ' + str(
                int(((total_travel_time % 86400) % 3600) // 60)) + 'm ' + str(
                int(((total_travel_time % 86400) % 3600) % 60)) + 's')

    print('The total travel time for the specified filters is  ', total_travel_time)

    # display average travel time
    average_travel_time = filtered_df['Trip Duration'].mean()
    average_travel_time = (str(int(average_travel_time // 60)) + 'm ' + str(int(average_travel_time % 60)) + 's')
    print("The average travel time for the specified filters is ", average_travel_time)
    print("\n----------End of calculating Trip Duration---------\n")
    print("\n----------User info---------\n")

    # Display counts of user types
    user_types = filtered_df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = filtered_df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("We're sorry! There is no data of user genders for {}.".format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(filtered_df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(filtered_df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(filtered_df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: " + most_common_birth_year)
    except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))
    print("\n----------End of user info---------\n")
    print("\n----------Printing raw data---------\n")

    pd.set_option('display.max_rows', 5)

    # Print the initial 5 rows
    print(df.head())
    start_index = 5

    # Ask the user if they want to see more raw data
    while True:
        show_more = input("Do you want to see more raw data? Enter 'yes' or 'no': ")
        if show_more.lower() == 'yes':
            # Print the next 5 rows
            print(df[start_index:start_index + 5])
            # Increment the start index by 5
            start_index += 5
        else:
            print("\n----------End of printing raw data---------\n")
            break


def get_filters():
    """
      Asks user to specify a city, month, and day to analyze.

      Returns:
          (str) city - name of the city to analyze
          (str) month - name of the month to filter by, or "all" to apply no month filter
          (str) day - name of the day of week to filter by, or "all" to apply no day filter
      """

    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input(
            'Which city do you want to see data for between chicago, new york city, washington?: '
        )
        if city.lower() in CITY_DATA:
            print(f'\nYou requested to see data for {city}. Is that correct? \n')
            choice = input('Yes / No: ')

            if choice.lower() == 'yes' or choice.lower() == 'y':
                print('\n')
                break
            elif choice.lower() == 'no' or choice.lower() == 'n':
                print('Please enter a different city. \n')
                print('\n')
            else:
                print('\n Invalid choice. Please enter Yes or No. \n')
        else:
            print('\nInvalid city. Please enter a valid city. \n')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter month between January and June :")
        if month.lower() in MONTHS:
            break
        else:
            print('\nPlease enter a vaild month. \n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease enter day of the week.\n")
        if day.lower() in DAYS:
            break
        else:
            print('Please enter a valid day of the week')

    print('-' * 40)
    print(city, month, day)
    print('-' * 40)

    return city, month, day

def main():
    while True:
        print('Hello! Let\'s explore some US bikeshare data!\n')
        city = get_city_filter()

        choice = input(
            '\nWould you like to filter your data by month, day, all select one filter: '
        )
        if choice.lower() == 'month':
            filter_month = input('Enter the a month between January and June: ')
            if filter_month in MONTHS:
                df = load_data(city, MONTHS[filter_month])
                get_statistics(df)
            else:
                print('invalid month enter')
        if choice.lower() == 'day':
            filter_day = input('Enter the a day of the week: ')
            if filter_day in DAYS:
                df = load_data(city, filter_day)
                get_statistics(df)
            else:
                print('invalid day enter')
        if choice.lower() == 'all':
            df = load_data(city, 'all')
            get_statistics(df)

        else:
            print('Input did not match any filter.')

if __name__ == '__main__':
    main()

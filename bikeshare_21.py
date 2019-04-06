import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello sir! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs 
    city = ''

    while city not in ('chicago', 'nyc', 'washington'):
        city = input('Which city (chicago, nyc, washington)?: ').lower()

    print(city)

    # get user input for month (all, january, february, ... , june)
    month = ''

    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input('Which month do you want? (all, january, february, ... , june): ').lower()

    print(month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''

    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Which day do you want? (all, monday, tuesday, ... sunday): ').lower()

    print(day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    if city == "nyc":
        df = pd.read_csv('new_york_city.csv')
    else:
        df = pd.read_csv(city + '.csv')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df.month.mode()[0]
    print('The most common month:', popular_month)

    # display the most common day of week
    popular_day = df.day_of_week.mode()[0]
    print('The most common day of week:', popular_day)

    # display the most common start hour
    popular_hour = df.hour.mode()[0]
    print('The most common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_start_end_station = df.trip.mode()[0]
    print('The most common trip:', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_travel_time = df['Trip Duration'].sum()
    print('The total travel time (secs):', sum_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time (secs):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df.groupby('User Type').size()
    print('The counts of user types:', count_user_types)

    # Display counts of gender
    if 'Gender' in df:
        count_gender = df.groupby('Gender').size()
        print('The counts of gender:', count_gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df["Birth Year"].min())
        most_recent_birth_year = int(df["Birth Year"].max())
        most_common_birth_year = int(df["Birth Year"].mode()[0])
        print('The earliest year of birth:', earliest_birth_year)
        print('The most recent year of birth:', most_recent_birth_year)
        print('The most common year of birth:', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data(df):
    number = 0
    while True:
        response = input('\nWould you like to display the next five rows of data? Enter yes or no.\n').lower()
        if response == "yes":
            print(df.iloc[number:number + 5])
            number += 5
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

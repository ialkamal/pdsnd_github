import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

DAY_OF_WEEK_WN = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                  'friday': 4, 'saturday': 5, 'sunday': 6}
MONTH_WN = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
            "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

DAY_OF_WEEK_NW = {value: key for key, value in DAY_OF_WEEK_WN.items()}
MONTH_NW = {value: key for key, value in MONTH_WN.items()}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in ["chicago", "new york city", "washington"]:
        city = input(
            "choose a ciy: chicago, new york city, washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month not in ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]:
        month = input(
            "choose a month: all, january, february, ... , june: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        day = input(
            "choose a month: all, monday, tuesday, ... sunday: ").lower()

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour

    df = df.rename(columns={'Unnamed: 0': 'id'})
    df = df.set_index('id')

    if month != "all":
        df = df.loc[df['month'] == MONTH_WN[month]]

    if day != "all":
        df = df.loc[df['day'] == DAY_OF_WEEK_WN[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
        Returns:
        Nothing
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()
    print('The most common month is:')
    for m in most_common_month:
        print(MONTH_NW[m].capitalize())

    print("\n")

    # display the most common day of week
    most_common_day = df['day'].mode()
    print('The most common day of week is:')
    for d in most_common_day:
        print(DAY_OF_WEEK_NW[d].capitalize())

    print("\n")

    # display the most common start hour
    most_common_hour = df['hour'].mode()
    print('The most common hour is:')
    for h in most_common_hour:
        if h == 0:
            print("12 AM")
        if h > 0 and h < 12:
            print("{} AM".format(h))
        else:
            print("{} PM".format(h-12))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()
    print('The most common start station is:')
    for s in most_common_start:
        print(s)

    print("\n")

    # display most commonly used end station
    most_common_end = df['End Station'].mode()
    print('The most common end station is:')
    for e in most_common_end:
        print(e)

    print("\n")

    # display most frequent combination of start station and end station trip
    df["Combined Station"] = df['Start Station'] + " - " + df['End Station']
    most_common_combined = df['Combined Station'].mode()
    print('The most common combination of start station and end station trip is:')
    for c in most_common_combined:
        print(c)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time:", np.sum(df['Trip Duration']))

    print("\n")

    # display mean travel time
    print("Mean travel time:", np.mean(df['Trip Duration']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    
       Function checks if the city is Washington
       It doesn't have gender or birth year data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types:")
    print(df['User Type'].value_counts())

    print("\n")

    if city != 'washington':
        # Display counts of gender
        print("Counts of Gender:")
        print(df['Gender'].value_counts())

        print("\n")

        # Display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth:")
        print(int(np.min(df['Birth Year'])))

        print("\n")

        print("Most Recent Year of Birth:")
        print(int(np.max(df['Birth Year'])))

        print("\n")

        print("Most common Year of Birth:")
        most_common_year = df['Birth Year'].mode()
        for y in most_common_year:
            print(int(y))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        row = 0
        total_rows = len(df)
        while row < total_rows:
            raw = input(
                '\nWould you like to see the raw data? Enter yes or no.\n')
            print(df.iloc[row:row+5])
            row += 5
            if raw.lower() != 'yes':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 0
    while (city not in CITY_DATA):
        city = input('Enter the name of the city that you want to get the data from..  \n').lower()
        if (city not in CITY_DATA):
            print('\nIt appears that the city name is incorrect, please try again..')
    resp = input("\nDo you want to filter by day or month or both: ")
    # TO DO: get user input for month (all, january, february, ... , june)
    mnth = ['january', 'february', 'march', 'april', 'may', 'june']
    month = 0


    if ( resp == 'month' or resp == 'both'):
        while (month not in mnth):
            month = input('Specify the month (e.g. all, january, february, ... , june) .. \n').lower()
            if (month not in mnth):
                print('\nIt appears that the month entered is incorrect, please try again..')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = 0
    if ( resp == 'day' or resp == 'both'):
        while (day not in days):
            day = input('Specify the day of week (e.g. all, monday, tuesday, ... sunday) .. \n').lower()
            if (day not in days):
                print('\nIt appears that the day entered is incorrect, please try again..')
        if day!='all':
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = days.index(day) + 1

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if (month != 'all' and month != 0):
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if (day != 'all' and day != 0):
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day]



    return df

def data_display(df):
    count = 0
    resp = 0
    while True:
        while(resp!='yes' or resp!='no'):
            resp = input("Do you want to see raw data (yes or no): ").lower()
            if resp == 'yes':
                count = int(input("\nHow many rows you want to see (please enter an integer): "))
                print(df.head(count))
                break
            elif resp == 'no':
                break
            else:
                print("\nPlease enter a valid response...\nTry again!\n")

        while (resp != 'no'):
            resp = input("Do you want to see more raw data (yes or no): ").lower()
            if resp == 'yes':
                count += int(input("\nHow many more rows you want to see (please enter an integer): "))
                print(df.head(count))

        if (resp == 'no'):
            break




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month is:   ', months[df['month'].mode()[0] - 1])
    # TO DO: display the most common day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('\nMost common day is:  ',days[df['day of week'].mode()[0]])
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('\nMost popular start hour is:  ', df['hour'].mode()[0])

    print("\nThis took {} seconds." .format( (time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    #df['Start Station'] = df['Start Station'].to_string(index = False, header = False)

    # TO DO: display most commonly used start station
    dfx = df[df['hour'] == df['hour'].mode()[0]]
    print('The most commonly used start station: ', dfx['Start Station'].mode()[0])
    # TO DO: display most commonly used end station
    print('The most commonly used end station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    x = str(df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1).index[0])
    x = x.replace('(', '').replace(')', '').replace("'", '')
    print('Most frequent combination of start and end station: ',x.strip())
    print("\nThis took {} seconds."  .format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time in seconds: ", df['Trip Duration'].sum() )

    # TO DO: display mean travel time
    print("Mean travel time in seconds: ", df['Trip Duration'].mean() )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        var = '\n' + df['User Type'].value_counts().to_string()
    else:
        var = 'N/A'
    print('Count of user types: {}'.format(var))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        var = '\n' + df['Gender'].value_counts().to_string()
    else:
        var = 'N/A'
    print('\nCount of Genders: {}'.format(var))


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        var = int(df['Birth Year'].min())
    else:
        var = 'N/A'
    print('\nEarliest year of birth: {}'.format(var))

    if 'Birth Year' in df.columns:
        var = int(df['Birth Year'].max())
    else:
        var = 'N/A'
    print('\nMost recent birth year: {}'.format(var))

    if 'Birth Year' in df.columns:
        var = int(df['Birth Year'].mode()[0])
    else:
        var = 'N/A'
    print('Most common year of birth: {}'.format(var))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

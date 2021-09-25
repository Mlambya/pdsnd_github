import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    """ To get user input for city (chicago, new york city, washington). """
    
    while True:
        try:
            city = input('Choose a city to explore from "chicago, new york city, washington"').lower()
            if city in CITY_DATA:
                break
        except:
            print('Please choose from the list')
                        

    """ To get user input for month """
    
    while True:
        try:
            month = input('Choose a month from january, february, march, april, may, june or "all" to inlcude all ')
            if month in months or month == 'all':
                break
        except:        
            print('Please choose from the list')
            
            print('You have chosen ' + month)

    """ To get user input for day of week (all, monday, tuesday, ... sunday)"""
    
    while True:
        try:
            day = input('Choose a day of the week or "all" ')
            if day in days or day == 'all':
                break
        except:
            print('Please choose from the list')
        
                
            print('You have chosen ' + day)

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
    
    """ load data file into a dataframe """
    
    df = pd.read_csv(CITY_DATA[city])

    """ convert the Start Time column to datetime """
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ extract month and day of week from Start Time to create new columns """
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week  

    """ filter by month if applicable """
    
    if month != 'all':
        """ use the index of the months list to get the corresponding int """
        month = months.index(month) + 1

        """ filter by month to create the new dataframe """
        df = df[df['month'] == month]

    """ filter by day of week if applicable """
    
    if day != 'all':
        """  filter by day of week to create the new dataframe """
        df = df[df['day_of_week'] == day.title()]


def raw_data(df):
    """ this part displays raw data following the request of user when askesd
    
    this will display 5 rows of data at a time and continue till the end or user aborts
    by typing no"""
        
    rowi = 0
    response = input('Before procceeding, would you like to see the raw data, 5 lines at a time? yes or no').lower()
    pd.set_option('display.max_columns', None)             
    
    while True:
        try:
            if response == 'no':
                break
            print(df[rowi:rowi+5])
            response = input('Before procceeding, would you like to see the raw data, 5 lines at a time? yes or no').lower()
            rowi += 5
        except:
            print('Please type "yes" or "no"')
               


    return df




    
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    """To display the most common month """
    most_common_month = df['month'].mode()
    print('The most common month is ', most_common_month + 1) 
    
    
    """To display the most common day of week """
    most_common_day = df['day_of_week'].mode()
    print('The most common day of the week is ', most_common_day + 1)
   
    """To display the most common start hour """
    df['hour'] = df['Start Time'].dt.hour
    most_common_start = df['hour'].mode()
    print('The most common start hour is ', most_common_start + 1)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ display most commonly used start station """
    """ try removing the zeroes and square brackets """
    common_start_station = df['Start Station'].mode()
    print('The most common start station is ', common_start_station)
    """ display most commonly used end station """
    common_end_station = df['End Station'].mode()
    print('The most common end station is ', common_end_station)

    """ display most frequent combination of start station and end station trip """
    most_frequent = common_start_station, ' & ', common_end_station
    print('The most frequent combination of start and end station is ', most_frequent )
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
 
    """To display total travel time """
    total_trip_duration = df['Trip Duration'].sum() 
    total_in_hours = total_trip_duration/3600
    total_in_days = total_trip_duration/86400
    print('The total travel time is ', total_in_hours, 'hours or ', total_in_days, 'day(s)')

    """ To display mean travel time """
    ave_trip_duration = df['Trip Duration'].mean()
    print('The average trip duration is ', ave_trip_duration/60, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """To Display counts of user types"""
    user_types = df['User Type'].value_counts()
    print('The counts of user types are: ', user_types)

    "To display counts of gender if provided"""
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts(dropna=True)
        print('The counts of gender types are: ', gender_types)
    
    if 'Birth Year' in df:
        df['Birth Years'] = df['Birth Year'].dropna(inplace=True)
        
        """To display earliest, most recent, and most common year of birth """
        earliest_birth_year = df['Birth Years'].min()
        print('The earliest year of birth is ', earliest_birth_year)
    
        recent_birth_year = df['Birth Years'].max()
        print('The most recent year of birth is ', recent_birth_year)
    
        common_birth_year = df['Birth Years'].mode()
        print('The most common year of birth is ', common_birth_year)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
import calendar as cal

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Give city : ')
            city = city.lower()
            if city in ('chicago', 'new york city', 'washington'):
                break
            else: 
                print('Should be either Chicago, New York City or Washington')
        except:
            pass
            

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Would you like to filter by month or not ( "all" = no filter) : ')
            if month.isdigit() and int(month) > 0 and int(month) < 13:
                break
            elif month == 'all':
                break
            else:
                print('Should be a number between 1 and 12 or all!')
        except:
            pass


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Would you like to filter by day or not ( 0 = Monday, 6 = Sunday, ... all = no filter) : ')
            if day.isdigit() and  int(day)  >= 0 and int(day) <= 6:
                break
            elif day == 'all':
                break
            else:
                print('Should be a number between 0 and 6 or all')
                
        except:
            pass
            
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
    filename = CITY_DATA[city]

    df = pd.read_csv(filename)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["dow"] = df["Start Time"].dt.weekday


    if month != 'all':
        df = df[df['month'] == int(month)]

    if day != 'all':
        df = df[df['dow'] == int(day)]

    return df
    

def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel (most common month/day/hour to travel).

    Args :
          df - the filtered dataframe
          (str) month - } 
          (str) day   - }} only used for corny message if the dataframe is filtered on month and/or day

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popidx = df['month'].value_counts().idxmax()
    popmth = cal.month_name[popidx]
    popcnt = df['month'].value_counts().max()
    print('Most common month is {} with {} starters'.format(popmth , popcnt))
    if month.isdigit():
        print ('                  What did you expect when you filtered on {} ?'.format(popmth))

    # display the most common day of week
    popidx = df['dow'].value_counts().idxmax()
    popday = cal.day_name[popidx]
    popcnt = df['dow'].value_counts().max()
    print('Most common day of the week is {} with {} starters'.format(popday , popcnt))
    if day.isdigit():
        print ('                  What did you expect when you filtered on {} ?'.format(popday))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popidx = df['hour'].value_counts().idxmax()
    popcnt = df['hour'].value_counts().max()
    print('Most common start hour is {} hour with {} starters'.format(popidx , popcnt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args :
          df - the filtered dataframe
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popidx = df['Start Station'].value_counts().idxmax()
    popcnt = df['Start Station'].value_counts().max()
    print('Most common station to start is {} with {} people.'.format(popidx , popcnt))

    # display most commonly used end station
    popidx = df['End Station'].value_counts().idxmax()
    popcnt = df['End Station'].value_counts().max()
    print('Most common station to end is {} with {} people.'.format(popidx , popcnt))


    # display most frequent combination of start station and end station trip
    #first count all values
    dfse = df[['Start Station','End Station']].value_counts().reset_index(name='count')
    #only retain the max values (can be more than 1)
    dfse = dfse[dfse['count']==dfse['count'].max()]
    
    print('Most common combination(s) stations to start and end is/are : ')
    for i in dfse.index:
        print('Start: ', dfse.iloc[i]['Start Station'] , ' End: ' , dfse.iloc[i]['End Station'] , ' Nbr: ' , dfse.iloc[i]['count'] )  
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args : 
          df - the filtered dataframe
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('Total Travel Time was {} days, {} hours, {} minutes and {} seconds.'.format(int(d),int(h),int(m),int(s)))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    m, s = divmod(mean, 60)
    print('Mean Travel Time was {} minutes and {} seconds.'.format(int(m),int(s)))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args : 
          df - the filtered dataframe
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    dfut = df[['User Type']].value_counts().reset_index(name='count')
    print('Breakdown on User Types :')
    for i in dfut.index:
        print('    ', dfut.iloc[i]['User Type']     , ': '     , dfut.iloc[i]['count'])

    # Display counts of gender (watch out : gender column not always present!!)
    try:
        dfge = df[['Gender']].value_counts().reset_index(name='count')
        print('Breakdown on Gender :')
        for i in dfge.index:
            print('    ', dfge.iloc[i]['Gender']     , ': '     , dfge.iloc[i]['count'])
    except:
        print('    No breakdown on gender possible')
        
        
    # Display earliest, most recent, and most common year of birth (also here, not always present)
    try:
        print('Breakdown on Birth Year :')
        print('    Most common Birth Year : ' , df['Birth Year'].value_counts().idxmax())
        print('    Most recent Birth Year : ' , df['Birth Year'].max())
        print('    Earliest Birth Year : ' , df['Birth Year'].min())

    except:
        print('    No breakdown on birth year possible')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    give back 5 rows of raw data upon request

    Args : 
          df - the filtered dataframe
    """
    rd_answer = input('Would you like to see some data from the file (yes/no)?\n')
    start_pos = 0
    while True:
        if rd_answer.lower() != 'yes':
            break

        while rd_answer == 'yes':
            for i in range(start_pos, start_pos +5):
                print(df.iloc[i].tolist())
            start_pos += 5
            rd_answer = input('Would you like to see some more date (yes/no)?\n')

def main():
    while True:
        city, month, day = get_filters()
        print('Seems like you want to know more about {} in this month : {} and this day : {}'.format(city, month, day))
        
        df = load_data(city, month, day)
        time_stats(df,month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

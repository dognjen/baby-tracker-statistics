from optparse import OptionParser
from datetime import datetime

import plotly.plotly as py

parser = OptionParser()

parser.add_option("-u", "--username", dest="username", help="input username for plotly.", metavar="UNAME")
parser.add_option("-k", "--apikey", dest="apikey", help="input apikey for plotly.", metavar="APIKEY")

(options, args) = parser.parse_args()


MINUTES_IN_DAY = 1440


def longest_nap(data):
    return


def clean_data(data):
    x = [] # recorded dates
    y = [] # number of minutes slept in each date
    time_carried_over = 0 # time sleeping that gets carried over to next date

    for i, row in enumerate(data):

        # initialize values
        new_date = False
        time_not_carried_over = time_carried_over

        # parse date and time
        # sleep_datetime; contains datetime
        # started_sleeping; contains at what time the baby fell asleep
        sleep_date = row[1].split('. ')
        started_sleeping = sleep_date[2].split(' ')[1].split(':')
        started_sleeping = 60 * int(started_sleeping[0]) + int(started_sleeping[1])
        sleep_datetime = datetime(year=int('20' + sleep_date[2].split(' ')[0]), month=int(sleep_date[1]), day=int(sleep_date[0]))

        # check if date already in list
        if sleep_datetime not in x:
            x.append(sleep_datetime)
            new_date = True # new date added to list; flag set to True

        # parse sleep duration
        hours = '0'; minutes = '0'
        if row[2] != '':
            if 'hrs' in row[2]:
                hours = row[2].split(' hrs')[0]
                if 'min' in row[2]:
                    minutes = row[2].split(' hrs')[1].split(' min')[0]
                else:
                    minutes = 0
            elif 'hr' in row[2]:
                hours = 1
                if 'min' in row[2]:
                    minutes = row[2].split(' hr')[1].split(' min')[0]
                else:
                    minutes = 0
            else:
                hours = 0
                minutes = row[2].split(' min')[0]
        else:
            if sleep_datetime not in x:
                y.append(0)
            continue

        # calculate minutes
        sleep_duration = 60 * int(hours) + int(minutes)

        # check if sleep after midnight.
        # ex: started_sleeping -> 23h, sleep_duration -> 7h => time_not_carried_over -> 1h, time_carried_over -> 6h
        if started_sleeping + sleep_duration > MINUTES_IN_DAY:
            time_carried_over = (started_sleeping + sleep_duration) - MINUTES_IN_DAY
            time_not_carried_over += (sleep_duration - time_carried_over)
            sleep_duration = time_not_carried_over

        # check: if date is new, append sum of time sleeping else add sleep_duration to current value
        if new_date:
            y.append(sleep_duration + time_not_carried_over)
            time_carried_over = 0
        else:
            idx = x.index(sleep_datetime)
            y[idx] += sleep_duration

    return x, y


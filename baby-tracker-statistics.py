from optparse import OptionParser
from datetime import datetime

import plotly.plotly as py
import plotly.graph_objs as go

# constants
MINUTES_IN_DAY = 1440

# read from console
parser = OptionParser()
parser.add_option("-u", "--username", dest="username", help="input username for plotly.", metavar="UNAME")
parser.add_option("-k", "--apikey", dest="apikey", help="input apikey for plotly.", metavar="APIKEY")

# parse arguments
(options, args) = parser.parse_args()
py.sign_in(options['username'], options['apikey'])


def clean_data(data):
    clean_data = {} # key - recorded dates, value - list of naps in that day
    time_carried_over = 0 # time sleeping that gets carried over to next date

    for i, row in enumerate(data):

        # initialize values
        new_date = False

        # parse date and time
        # sleep_datetime; contains datetime
        # started_sleeping; contains at what time the baby fell asleep
        sleep_date = row[1].split('. ')
        started_sleeping = sleep_date[2].split(' ')[1].split(':')
        started_sleeping = 60 * int(started_sleeping[0]) + int(started_sleeping[1])
        sleep_datetime = datetime(year=int('20' + sleep_date[2].split(' ')[0]), month=int(sleep_date[1]), day=int(sleep_date[0]))

        # check if date already in list
        if sleep_datetime not in clean_data:
            clean_data[sleep_datetime] = []
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

        # calculate minutes
        sleep_duration = 60 * int(hours) + int(minutes)

        # check if sleep after midnight.
        # ex: started_sleeping -> 23h, sleep_duration -> 7h => time_not_carried_over -> 1h, time_carried_over -> 6h
        if started_sleeping + sleep_duration > MINUTES_IN_DAY:
            time_carried_over = (started_sleeping + sleep_duration) - MINUTES_IN_DAY
            time_not_carried_over = (sleep_duration - time_carried_over)
            clean_data[sleep_datetime].append(time_not_carried_over)
            continue

        # check if need to add carried time
        if new_date and time_carried_over > 0:
            clean_data[sleep_datetime].append(time_carried_over)
            time_carried_over = 0

        clean_data[sleep_datetime].append(sleep_duration)

    return clean_data


def number_of_naps(data):
    x = list(data.keys())
    y = list(map(lambda x : len(x), data.values()))

    d = [go.Bar(x=x, y=y)]
    py.iplot(d)

def daily_sum_naps(data):
    x = list(data.keys())
    y = list(map(lambda x: sum(x), data.values()))

    d = [go.Bar(x=x, y=y)]
    py.iplot(d)

def daily_avg_naps(data):
    x = list(data.keys())
    y = list(map(lambda x: sum(x)/len(x), data.values()))

    d = [go.Bar(x=x, y=y)]
    py.iplot(d)


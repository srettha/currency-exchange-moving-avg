from __future__ import print_function

from operator import itemgetter

import csv

CSV_PATH = './data/aud-jpy-test-200(hourly).csv'
TIMING_LINE = 10
DECISION_LINE = 50
START_DATE_PROGRAM = 50

with open(CSV_PATH, encoding='utf-8') as csvfile:
    row = csv.reader(csvfile, delimiter=',')
    data_lists = list(row)

def get_closing_price(list):
    closing_price_lists = []
    for data_list in data_lists:
        closing_price_lists.append([data_list[1], float(data_list[len(data_list[0]) - 1])])
    
    return closing_price_lists

def average_closing_price_of_n_day(closing_price_lists, start, n):
    closing_price_lists = closing_price_lists[start - n:start]
    avg = 0.00
    for closing_price_list in closing_price_lists:
        avg += closing_price_list[1]

    return avg / len(closing_price_lists)

def make_decision(closing_price_lists):
    position_in_hand = False
    position = ''
    start_position = 0.00
    start_date = ''
    profit = []
    # len 50 - 100
    for i, closing_price_list in enumerate(closing_price_lists[START_DATE_PROGRAM:len(closing_price_lists)]):
        CURRENT_DAY = (START_DATE_PROGRAM + i) + 1
        avg_of_10 = average_closing_price_of_n_day(
            closing_price_lists, CURRENT_DAY, TIMING_LINE)
        avg_of_50 = average_closing_price_of_n_day(
            closing_price_lists, CURRENT_DAY, DECISION_LINE)
        if position_in_hand:
            if position == 'buy': # buy in hand
                if closing_price_list[1] < avg_of_10:  # close buy
                    actual_profit = closing_price_list[1] - start_position
                    profit.append(
                        [i, position, start_date, closing_price_list[0], actual_profit, start_position, closing_price_list[1], avg_of_10, avg_of_50])
                    position_in_hand = False
                    position = ''
                    start_position = 0.00
                    start_date = ''
                    if closing_price_list[1] > avg_of_50 and closing_price_list[1] > avg_of_10 and avg_of_10 > avg_of_50:
                        position_in_hand = True
                        position = 'buy'
                        start_position = closing_price_list[1]
                        start_date = closing_price_list[0]
                    elif closing_price_list[1] < avg_of_50 and closing_price_list[1] < avg_of_10 and avg_of_50 > avg_of_10:
                        position_in_hand = True
                        position = 'sell'
                        start_position = closing_price_list[1]
                        start_date = closing_price_list[0]
            else: # sell in hand
                if closing_price_list[1] > avg_of_10:
                    actual_profit = start_position - closing_price_list[1]
                    profit.append([i, position, start_date, closing_price_list[0], actual_profit,
                                start_position, closing_price_list[1], avg_of_10, avg_of_50])
                    position_in_hand = False
                    position = ''
                    start_position = 0.00
                    start_date = ''
                    if closing_price_list[1] > avg_of_50 and closing_price_list[1] > avg_of_10 and avg_of_10 > avg_of_50:
                        position_in_hand = True
                        position = 'buy'
                        start_position = closing_price_list[1]
                        start_date = closing_price_list[0]
                    elif closing_price_list[1] < avg_of_50 and closing_price_list[1] < avg_of_10 and avg_of_50 > avg_of_10:
                        position_in_hand = True
                        position = 'sell'
                        start_position = closing_price_list[1]
                        start_date = closing_price_list[0]
        else: # open order
            if closing_price_list[1] > avg_of_50 and closing_price_list[1] > avg_of_10 and avg_of_10 > avg_of_50:
                position_in_hand = True
                position = 'buy'
                start_position = closing_price_list[1]
                start_date = closing_price_list[0]
            elif closing_price_list[1] < avg_of_50 and closing_price_list[1] < avg_of_10 and avg_of_50 > avg_of_10:
                position_in_hand = True
                position = 'sell'
                start_position = closing_price_list[1]
                start_date = closing_price_list[0]

    return profit

def total_profit(profit):
    avg = 0.00
    for p in profit:
        avg += p[4]

    return avg / len(profit)
# reverse data
data_lists = data_lists[::-1]

closing_price_lists = get_closing_price(data_lists)
profit = make_decision(closing_price_lists)
avg_profit = total_profit(profit)
print(avg_profit)

import csv
from collections import defaultdict

from constants import ORDER_ID, USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY, PRODUCT_ID, DEPARTMENT_ID, DEPARTMENT_NAME, DAYS, \
    HOURS, PERCENTAGE, TRAIN_CSV, PRIOR_CSV
from dict_computing import get_col_indices, get_dicts
from pandas_impl import get_totals_pandas


def get_totals_absolutes(filename, orders_dict, products_dict, departments_dict):
    with open(filename, "r") as csvfile:
        print("computing orders for file: " + filename)
        parsed_combinations = set()
        counter = defaultdict(int)
        reader = csv.reader(csvfile, delimiter=",")
        header = next(reader)
        order_ix, product_ix = get_col_indices(header, ORDER_ID, PRODUCT_ID)
        for index, row in enumerate(reader):
            if index % 1000000 == 0 and index != 0:
                print("parsed " + str(int(index / 1000000)) + "M orders")
            order_id = row[order_ix]
            product_id = row[product_ix]
            user_id = orders_dict[order_id][USER_ID]
            dow = orders_dict[order_id][ORDER_DOW]
            hour = orders_dict[order_id][ORDER_HOUR_OF_DAY]
            department = departments_dict[products_dict[product_id][DEPARTMENT_ID]][DEPARTMENT_NAME]
            combination = (user_id, department, dow, hour)
            if combination not in parsed_combinations:
                parsed_combinations.add(combination)
                counter[(dow, hour, department)] += 1
        return counter


def get_percentages(absolute_vals):
    temp_list = [defaultdict(int) for _ in range(DAYS)]
    percentages = {}
    for (dow, hour, department) in absolute_vals:
        temp_list[int(dow)][int(hour)] += absolute_vals[(dow, hour, department)]
    for (dow, hour, department) in absolute_vals:
        percentages[(dow, hour, department)] = absolute_vals[(dow, hour, department)] / temp_list[int(dow)][int(hour)]
    return percentages


def print_totals(totals_perc_sorted):
    for i in range(DAYS):
        print("Day " + str(i) + ":")
        for j in range(HOURS):
            print("\tHour " + str(j) + ":")
            cur_stats = totals_perc_sorted[i][j]
            for key_index, key in enumerate(sorted(cur_stats, key=lambda x: cur_stats[x], reverse=True)):
                print("\t\t" + str(key_index) + "." + key.capitalize() + " (" + str(cur_stats[key]) + "%)")


def get_sorted(percentages_vals):
    totals_sorted = []
    for i in range(DAYS):
        totals_sorted.append([{} for _ in range(HOURS)])
    for (day, hour, department) in percentages_vals:
        totals_sorted[int(day)][int(hour)][department] = round(percentages_vals[day, hour, department] * 100)
    return totals_sorted


def validate(df, totals_perc_sorted):
    for index, row in df.iterrows():
        dow = row[ORDER_DOW]
        hour = row[ORDER_HOUR_OF_DAY]
        department = row[DEPARTMENT_NAME]
        percentage = row[PERCENTAGE]
        assert totals_perc_sorted[dow][hour][department] == percentage


def get_my_totals(filename):
    absolute_vals = get_totals_absolutes(filename, orders_dict, products_dict, departments_dict)
    percentages_vals = get_percentages(absolute_vals)
    return get_sorted(percentages_vals)


if __name__ == '__main__':
    orders_dict, products_dict, departments_dict = get_dicts()
    df = get_totals_pandas(TRAIN_CSV)
    totals_train = get_my_totals(TRAIN_CSV)
    validate(df, totals_train)
    totals_prior = get_my_totals(PRIOR_CSV)
    print_totals(totals_prior)

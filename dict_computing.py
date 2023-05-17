import csv

from constants import ORDER_ID, USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY, PRODUCT_ID, DEPARTMENT_ID, DEPARTMENT_NAME, \
    ORDERS_CSV, PRODUCTS_CSV, DEPARTMENTS_CSV


def get_col_indices(header, *kwargs):
    indices = []
    for col in kwargs:
        if col not in header:
            raise ValueError("invalid column")
        indices.append(header.index(col))
    return *indices,


def get_dict(filename, *kwargs):
    with open(filename, "r") as csvfile:
        my_dict = {}
        reader = csv.reader(csvfile, delimiter=",")
        header = next(reader)
        my_tuple = get_col_indices(header, *kwargs)
        for row in reader:
            my_dict[row[my_tuple[0]]] = {elem: row[my_tuple[i + 1]] for i, elem in enumerate(kwargs[1:])}
        return my_dict


def get_dicts():
    orders_dict = get_dict(ORDERS_CSV, ORDER_ID, USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY)
    products_dict = get_dict(PRODUCTS_CSV, PRODUCT_ID, DEPARTMENT_ID)
    departments_dict = get_dict(DEPARTMENTS_CSV, DEPARTMENT_ID, DEPARTMENT_NAME)
    return orders_dict, products_dict, departments_dict

import pandas as pd

from constants import ORDER_ID, USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY, PRODUCT_ID, DEPARTMENT_ID, DEPARTMENT_NAME, \
    PERCENTAGE, ORDERS_CSV, PRODUCTS_CSV, DEPARTMENTS_CSV

SIZE = "size"
TOTALS = "totals"


def get_totals_pandas(filename):
    orders_df = pd.read_csv(ORDERS_CSV, usecols=[ORDER_ID, USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY])
    products_df = pd.read_csv(PRODUCTS_CSV, usecols=[PRODUCT_ID, DEPARTMENT_ID])
    departments_df = pd.read_csv(DEPARTMENTS_CSV, usecols=[DEPARTMENT_ID, DEPARTMENT_NAME])
    order_products_df = pd.read_csv(filename, usecols=[ORDER_ID, PRODUCT_ID])
    df = order_products_df.merge(orders_df)
    df = df.merge(products_df)
    df = df.merge(departments_df)
    df.drop_duplicates(subset=[USER_ID, ORDER_DOW, ORDER_HOUR_OF_DAY, DEPARTMENT_NAME], inplace=True)
    df.drop(columns=[DEPARTMENT_ID, PRODUCT_ID, ORDER_ID, USER_ID], inplace=True)
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    totals = df.groupby([ORDER_DOW, ORDER_HOUR_OF_DAY])[SIZE].transform('sum')
    df[TOTALS] = totals
    df[PERCENTAGE] = (df[SIZE] / df[TOTALS] * 100).round()
    df.drop(columns=[SIZE, TOTALS], inplace=True)
    return df

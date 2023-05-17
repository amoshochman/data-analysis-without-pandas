# data-analysis-without-pandas
### Statistics computing over datasets done by pure Python data structures

#### Instructions to use:

create in the root directory the following files, all of them with suffix ".csv": 

- aisles: aisle_id,aisle
- departments: department_id,department
- order_products__prior: order_id,product_id,add_to_cart_order,reordered
- order_products__train: order_id,product_id,add_to_cart_order,reordered
- orders: order_id,user_id,eval_set,order_number,order_dow,order_hour_of_day,days_since_prior_order
- products: product_id,product_name,aisle_id,department_id

The comma separated values after the colon are the names of the columns.

The Schema:

**orders**:

order_id: order identifier
user_id: customer identifier
eval_set: which evaluation set this order belongs in (see SET described below)
order_number: the order sequence number for this user (1 = first, n = nth)
order_dow: the day of the week the order was placed on
order_hour_of_day: the hour of the day the order was placed on
days_since_prior_order: days since the last order, capped at 30 (with NAs for order_number = 1)

**products**:

product_id: product identifier
product_name: name of the product
aisle_id: foreign key
department_id: foreign key

**aisles**:

aisle_id: aisle identifier
aisle: the name of the aisle

**departments**:

department_id: department identifier
department: the name of the department

**order_products__SET**:

order_id: foreign key
product_id: foreign key
add_to_cart_order: order in which each product was added to cart
reordered: 1 if this product has been ordered by this user in the past, 0 otherwise

where SET is one of the following two evaluation sets (eval_set in orders):

"prior": orders prior to that users most recent order
"train": training data for model building

The task implemented: Without using of Pandas, SQL or similar tools, using this datasets to generate a report that shows the most popular Departments purchased from, segmented by the hour for every day of the week.

**Example report output**:

    Day 0:

        Hour 0:

            1. Frozen (20%)

            2. Bakery (15%)

            ...

            21. Pets (0%)

        Hour 1:

            1. Bakery (19%)

            ...

        Hour 23:

            1. Bakery (19%)

            ...

    Day 1:

        Hour 0:

            1. Frozen (19%)

            ...



    ...

    Day 6:

        Hour 0:

            1. Alcohol (20%)

Additionally, any given user shouldn't inflate the data for a given hour, say “User A” buys from the Frozen department multiple times in hour 10, then it shouldn't inflate the Frozen department percentage for that hour.
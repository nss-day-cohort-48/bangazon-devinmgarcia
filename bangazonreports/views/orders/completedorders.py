"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def completeorder_list(request):
    """Function to build an HTML report of complete orders"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all customers, with related user info.
            db_cursor.execute("""
                SELECT 
                o.id,
                u.first_name || ' ' || u.last_name as full_name,
                sum(p.price) as order_total,
                pt.merchant_name as merchant
                FROM bangazonapi_order as o
                LEFT JOIN bangazonapi_customer as c on c.id = o.customer_id
                LEFT JOIN auth_user as u on u.id = c.user_id
                LEFT JOIN bangazonapi_orderproduct as op on op.order_id = o.id
                left join bangazonapi_product as p on op.product_id = p.id
                LEFT JOIN bangazonapi_payment as pt on o.payment_type_id = pt.id
                where o.payment_type_id NOTNULL
                GROUP BY o.id    
            """)

            dataset = db_cursor.fetchall()

            orders_by_customer = {}

            for row in dataset:

                orders_by_customer[row['id']] = {}
                orders_by_customer[row['id']]['id'] = row["id"]
                orders_by_customer[row['id']]['customer'] = row["full_name"]
                orders_by_customer[row['id']]['total'] = '{0:.2f}'.format(row["order_total"]) if row["order_total"] else 0
                orders_by_customer[row['id']]['merchant'] = row['merchant']
                
        # Get only the values from the dictionary and create a list from them
        list_of_complete_orders = orders_by_customer.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_complete_orders.html'
        context = {
            'orders_list': list_of_complete_orders
        }

        return render(request, template, context)

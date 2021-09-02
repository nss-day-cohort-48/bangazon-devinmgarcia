"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def inexpensiveproduct_list(request):
    """Function to build an HTML report of incomplete orders"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all customers, with related user info.
            db_cursor.execute("""
                SELECT
                p.name,
                p.description,
                p.price
                FROM bangazonapi_product as p
                WHERE p.price < 1000      
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = {}

            for row in dataset:

                inexpensive_products[row['id']] = {}
                inexpensive_products[row['id']]['id'] = row["id"]
                inexpensive_products[row['id']]['name'] = row["name"]
                inexpensive_products[row['id']]['description'] = row["description"]
                inexpensive_products[row['id']]['price'] = '{0:.2f}'.format(row["price"]) if row["price"] else 0
                
        # Get only the values from the dictionary and create a list from them
        list_of_inexpensive_products = inexpensive_products.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_inexpensive_products.html'
        context = {
            'product_list': list_of_inexpensive_products
        }
        return render(request, template, context)
"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection

def expensiveproduct_list(request):
    """Function to build an HTML report of incomplete orders"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all customers, with related user info.
            db_cursor.execute("""
                SELECT
                p.id,
                p.name,
                p.description,
                p.price
                FROM bangazonapi_product as p
                WHERE p.price > 1000      
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:

                expensive_products[row['id']] = {}
                expensive_products[row['id']]['id'] = row["id"]
                expensive_products[row['id']]['name'] = row["name"]
                expensive_products[row['id']]['description'] = row["description"]
                expensive_products[row['id']]['price'] = '{0:.2f}'.format(row["price"]) if row["price"] else 0
                
        # Get only the values from the dictionary and create a list from them
        list_of_expensive_products = expensive_products.values()

        # Specify the Django template and provide data context
        template = 'products/list_of_expensive_products.html'
        context = {
            'product_list': list_of_expensive_products
        }
        return render(request, template, context)
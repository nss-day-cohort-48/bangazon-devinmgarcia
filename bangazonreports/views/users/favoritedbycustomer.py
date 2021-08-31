"""Module for generating games by user report"""
from bangazonapi.models.favorite import Favorite
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazonreports.views import Connection


def favoritedbycustomer_list(request):
    """Function to build an HTML report of favorited sellers by customer"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all customers, with related user info.
            db_cursor.execute("""
                SELECT
                c.id,
                f.seller_id,
                au.first_name || ' ' || au.last_name AS customer_name,
                u.first_name || ' ' || u.last_name AS seller_name
                FROM bangazonapi_favorite as f
                JOIN bangazonapi_customer as c on c.id = f.customer_id
                JOIN auth_user as au on c.user_id = au.id
                JOIN bangazonapi_customer as ca on ca.id = f.seller_id
                JOIN auth_user as u on ca.user_id = u.id;       
            """)

            dataset = db_cursor.fetchall()

            favorites_by_customer = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                favorite = {"customer": "", "seller": ""}
                favorite['customer'] = row["id"]
                favorite['seller'] = row["seller_id"]
    

                # If the user's id is already a key in the dictionary...
                if row["id"] in favorites_by_customer:
                    # Add the current game to the `games` list for it
                    favorites_by_customer[row['id']]['favorited'].append(row["seller_name"])
                else:
                    # Otherwise, create the key and dictionary value
                    favorites_by_customer[row['id']] = {}
                    favorites_by_customer[row['id']]['full_name'] = row["customer_name"]
                    favorites_by_customer[row['id']]['favorited'] = [row["seller_name"]]

        # Get only the values from the dictionary and create a list from them
        list_of_favorites_by_customer = favorites_by_customer.values()

        # Specify the Django template and provide data context
        template = 'users/list_of_customer_favorites.html'
        context = {
            'favorites_list': list_of_favorites_by_customer
        }

        return render(request, template, context)

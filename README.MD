# EcommerceDjango
This is a project made so that I could learn more about web development.

It has:
- A main page where you can see side scrollable icons of products.
- Login and sign up page.
- A product page where you can view and add a product to your cart.
- A cart page where you can review your cart and make an order.
- An order page where you can see the status of the order and go to Stripe checkout.
- A search bar where you can type and make a query for a product name.

# How to Run
## With Docker
1 - `git clone https://github.com/GabrirelBRAA/EcommerceDjango.git`

2 - `docker compose up`

3 - `docker exec <app-tag-here> python manage.py populate_database_no_stripe`

(This third command populates the database with mock items, you will not have anything in the site
if you do no call it.)

## Locally
The python version used for development was 3.12.2, anything above that should work

1 - `git clone https://github.com/GabrirelBRAA/EcommerceDjango.git`

2 - Create a venv and activate it

3 - Into the repository: `pip install --no-cache-dir -r requirements.txt`

4 - Configure the database in settings.py. The default is set to the docker postgreSQL one but
    you probably want to change to the Django default SQLite in the local environment.

5 - `python manage.py migrate`

6 - `python manage.py populate_database_no_stripe`

7 - `python manage.py runserver`


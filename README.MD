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

2 - `docker build . -t <tag>`

3 - `docker run <tag>`

## Locally
The python version used for development was 3.12.2, anything above that should work

1 - `git clone https://github.com/GabrirelBRAA/EcommerceDjango.git`

2 - Create a venv and activate it

3 - Into the repository: `pip install --no-cache-dir -r requirements.txt`

4 - `python manage.py migrate`

5 - `python manage.py populate_database_no_stripe`

5 - `python manage.py runserver`


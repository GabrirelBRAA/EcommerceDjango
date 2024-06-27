# EcommerceDjango
This is a project made so that I could learn more about web development.

It has:
- A main page where you can see side scrollable icons of products.
- Login and sign up page.
- A product page where you can view and add a product to your cart.
- A cart page where you can review your cart and make an order.
- An order page where you can see the status and go to Stripe checkout.
- A search bar where you can type and make a query for a product name.

# How to Run
## With Docker
1 - `git clone https://github.com/GabrirelBRAA/EcommerceDjango.git`

2 - `docker build --build-arg STRIPE_PUBLIC_API=x .`

3 - `docker run <image_id>`

## Locally
The python version used for development was 3.12.2, so anything above that should work

1 - `git clone https://github.com/GabrirelBRAA/EcommerceDjango.git`


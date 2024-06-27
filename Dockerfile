FROM python:3

ARG STRIPE_PUBLIC_API
ARG STRIPE_PRIVATE_API

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STRIPE_PUBLIC_KEY = $STRIPE_PUBLIC_KEY
ENV STRIPE_SECRET_KEY = $STRIPE_PRIVATE_KEY
ENV PYTHONUNBUFFERED = 1

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py populate_database_no_stripe	

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

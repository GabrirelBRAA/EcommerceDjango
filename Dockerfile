FROM python:3

ENV STRIPE_PUBLIC_KEY=None
ENV STRIPE_PRIVATE_KEY=None

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
ENV STRIPE_SECRET_KEY=$STRIPE_PRIVATE_KEY
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=emoveis.settings	

EXPOSE 8000

CMD ["bash", "run_script.sh"]

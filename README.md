# Bookshop by baidy

This project is a containerized e-commerce book-selling platform consisting of multiple services.
The main idea of this project is to use separate store API to update in it information about books and their quantity, process orders and order statuses.
The shop service sends requests to API to: periodically synchronise info on books, create new orders, periodically synchronise info on customers' orders statuses.
Customers also receive email notifications after: sending an order, order status changes in API.
API requests and email sending is being performed by Celery service.

## Stack:

- Django (To create a Shop website)
- Django Rest Framework (To create a Store API)
- Docker (To make many microservices work together)
- PostgreSQL (To store data for Shop and Store)
- Nginx (To forward client's requests to right web applications: Shop port 8000, Store port 8001, Mailhog port 8025)
- Celery (To perform time-intensive tasks for shop, as described above)
- RabbitMQ (To receive tasks for celery)
- Redis (To save celery tasks results)
- Bootstrap (To make my shop service look awesome)
- jQuery, AJAX (To increment and decrement items in cart without reloading the page)
- MailHog (To simulate email sending)
- Flake8 (To maintain the backend code readable)
- Debug Toolbar (To help in database queries optimization)

## My Bookshop is built on such services:

1. **Shop Service**: The "shop" service is responsible for handling the main functionalities of the e-commerce shop. It is built from the Dockerfile located at `docker/shop/Dockerfile` and has a container name of "shop". The service runs on port 8000 and is connected to the following networks: shop_store_network, shop_network, and nginx_network. It depends on the "db_shop" service, "redis" service, and "celery" service. The service uses environment variables to configure the database connection.

2. **Database for Shop Service**: The "db_shop" service is a PostgreSQL database specifically used by the "shop" service. It uses the official "postgres" image and has a container name of "db_shop". The service runs on port 5433 and is connected to the shop_network. It exposes port 5432 and uses a volume called "db_shop_volume" to persist data.

3. **Redis Service**: The "redis" service is a standalone Redis server used by the "shop" service. It uses the official "redis" image and has a container name of "redis". The service runs on port 6379 and is connected to the shop_network.

4. **Celery Service**: The "celery" service is responsible for asynchronous task processing in the e-commerce platform. It is built from the Dockerfile located at `docker/shop/celery/Dockerfile` and has a container name of "celery". The service runs on port 8002 and is connected to the shop_store_network, shop_network, and mailhog_network. It depends on the "rabbitmq" service. The service uses environment variables to configure the broker URL and database connection.

5. **RabbitMQ Service**: The "rabbitmq" service provides a message broker for communication between services. It uses the official "rabbitmq" image and has a container name of "rabbitmq". The service runs on ports 5672 and 15672 and is connected to the shop_network. It depends on the "redis" service.

6. **Store Service**: The "store" service is responsible for managing the store functionalities of the e-commerce platform. It is built from the Dockerfile located at `docker/store/Dockerfile` and has a container name of "store". The service runs on port 8001 and is connected to the shop_store_network, store_network, mailhog_network, and nginx_network. It depends on the "db_store" service. The service uses environment variables to configure the database connection.

7. **Database for Store Service**: The "db_store" service is a PostgreSQL database specifically used by the "store" service. It uses the official "postgres" image and has a container name of "db_store". The service runs on port 5432 and is connected to the store_network. It exposes port 5432 and uses a volume called "db_store_volume" to persist data.

8. **SMTP Server**: The "smtp-server" service provides a local SMTP server for email testing and debugging. It uses the "mailhog/mailhog" image and has a container name of "smtp-server". The service exposes ports 1025 and 8025 and is connected to the mailhog_network and nginx_network. It depends on the "celery" service.

9. **Nginx**: The "nginx" service acts as a reverse proxy and serves as the entry point for the e-commerce platform. It is built from the Dockerfile located at `docker/nginx/Dockerfile` and has a container name of "nginx". The service runs on ports 8080, 8081, and 8082. It is connected to the nginx_network and depends on the "shop", "store", and "smtp-server" services. It uses a restart policy of on-failure.

## Installation:

___I don't guarantee you that this project will work on Windows! Docker works a bit different on it.___

1. Install and run docker on your computer.
2. Clone this repository.
3. Create a .env file in backend/shop and fill it with many random letters and numbers for SECRET_KEY variable and an empty string for TOKEN. For example:
   ```.env
   SECRET_KEY="tnc4tyo4n5yg4vw5ygc4wgmwrgeqgyr8guwerugh4w58gh45ugtrwhg"
   TOKEN=""
   ```
4. Create a .env file in backend/store and fill it with many random letters and numbers for SECRET_KEY. For example:
   ```.env
   SECRET_KEY="c7ty4578wvngvwgw4gyrt9grbgutr8gh84hw8hg8w4g9tgwb9r9g"
   ```
5. Open terminal in root folder (Bookshop) and run:
   ```shell
   docker-compose -f docker/docker-compose.yml build
   docker-compose -f docker/docker-compose.yml up
   ```
   P.S.: If "docker-compose" not working, try writing like this: "docker compose"

6. Finally, we can access our shop service: localhost:8000, store service: localhost:8001, mailhog: localhost:8025
7. This is not all. Now let's add some books to our store. But at first we need to create an admin user for store. Open a new console tab in the root folder and write these commands:
    ```shell
   docker-compose -f docker/docker-compose.yml exec store bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   You will have to enter what shell is asking. Do not exit this terminal window.
8. In this step let's create and save admin's token in order shop can send requests to store which will create orders in it. Run these commands:
   ```shell
   python manage.py shell
   ```
   ```python
   from django.contrib.auth import get_user_model
   from rest_framework.authtoken.models import Token
   User = get_user_model()
   # In the command below you have to input in quotes the username which you have created for admin user
   admin_user = User.objects.get(username='')
   token = Token.objects.create(user=admin_user)
   token.key
   ```
   Then copy the key which was printed out (WITHOUT THE QUOTES) and paste it into backend/shop/.env file into TOKEN variable quotes. Close this terminal window.
9. Open a new terminal window in the root folder. Now we are creating a shop admin:
    ```shell
   docker-compose -f docker/docker-compose.yml exec shop bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   You will have to enter what shell is asking.
10. Finally, you are ready to go to localhost:8001/admin and to finally create some books.
11. You are welcome to return to localhost:8000 to test my project further.

P.S.: Books are being synchronised every 5 minutes and orders statuses are being synchronised every 10 minutes. So keep patient ;)

__Thank You and have fun!__
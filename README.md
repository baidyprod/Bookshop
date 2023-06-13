# Bookshop by baidy

This project is a containerized e-commerce book-selling platform consisting of multiple services.
The main idea of this project is to use separate store API to update in it information about books and their quantity, process orders and order statuses.
The shop service sends requests to API in order to: periodically synchronise info on books, create new orders, periodically synchronise info on customers' orders statuses.
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
   docker-compose build
   docker-compose up
   ```
   Wait a bit until terminal logs stop.
   This will be our terminal window in which the project is running. DON'T CLOSE IT UNTIL MY PROJECT IS IN USE.
   P.S.: ___1. If docker says something like "You don't have permission", add a word "sudo" before executing every command which begins with "docker". 
         2. If "docker-compose" not working, try writing like this: "docker compose".___

6. This is not all. Now let's add some books to our store. But at first we need to create an admin user for store. Open a new terminal window in the root folder and write these commands:
    ```shell
   docker-compose exec store bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   You will have to enter what shell is asking. Do not exit this terminal window.
7. In this step let's create and save admin's token in order shop can send requests to store which will create orders in it. Run these commands:
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
   ```python
   exit()
   ```
   ```python
   exit
   ```
   Then copy the key which was printed out (WITHOUT THE QUOTES) and paste it into backend/shop/.env file into TOKEN variable quotes. Close this terminal window. Go to the main terminal window where the project is running and press CTRL+C (CMD+C on Mac) to stop the container. Now you have to go to the fifth step and do what I wrote there once again. After you're done with it, return to the next step :)
8. Open a new terminal window in the root folder. Now we are creating a shop admin:
    ```shell
   docker-compose exec shop bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   ```python
   exit
   ```
   You will have to enter what shell is asking.
9. I have created a management command for you to populate store db with books and book items!
    Just open a new terminal window in a project folder and run this command:
    ```shell
    docker-compose exec store bash
    ```
    ```python
    python manage.py populate_db
    ```
    ```python
    exit
    ```
    This command will create 50 books and random quantity of book items of these books.
10. You are welcome to go to the store admin page (127.0.0.1:8001/admin) click on "Books", choose any book and add a picture to it. The picture will be shown in the book's detail page in the shop!
11. So, your main services are: 127.0.0.1:8000 (Shop), 127.0.0.1:8001 (Store), 127.0.0.1:8025 (Emails)
12. Now I want to walk you through the whole selling process.
    1. Go to the shop (127.0.0.1:8000)
    2. Register, add some books to cart and create an order
    3. Now go to the admin page of the store (127.0.0.1:8001/admin)
    4. Navigate to "Orders" tab
    5. Choose the newly created order
    6. Add BookItems to it, and change status to success
    7. When you open this order again you can see that there are no BookItems left in it - they were entirely deleted from the store after marking the order as a successful one!
    8. In case if you forget to mark the order as successful, the book items won't be deleted. You can open this order again, change the status to success - only after that, book items you have chosen for the order will be deleted.
    9. I find this is the most interesting part of the project, because store-admin doesn't have to handle book items management after packing the order.
    10. Also, I hope you have noticed how easy it is to pack users order - just select book items which you want to pack, mark the order as the successful and hit "save"!
    11. Finally, you can go to Mailhog (127.0.0.1:8025) and notice an email, saying that your order was successfully proceeded.
13. Especially for you, I have created a management command to clear databases after testing my project in one click! Just open a shell of shop/store (Examples higher) and run this command:
    ```python
    python manage.py clear_db
    ```
14. To stop the project just press CMD+C (CTRL+C) in main terminal (where you run docker-compose up) and wait until all containers stop.
    All the data will be the saved.
15. To rerun the project go to the project root folder and paste this command:
    ```shell
    docker-compose up
    ```
P.S.: Books are being synchronized every 2 minutes and orders statuses are being synchronized every 1 minute. So keep patient ;)

__Thank You and have fun!__
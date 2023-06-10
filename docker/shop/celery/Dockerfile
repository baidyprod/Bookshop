FROM python:3.10

WORKDIR /app

COPY requirements/shop/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/shop/ .

EXPOSE 8000

CMD sh -c "sleep 20 && celery -A core worker --beat --loglevel=info"
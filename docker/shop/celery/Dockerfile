FROM python:3.10

WORKDIR /app

COPY backend/shop/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD sh -c "sleep 20 && celery -A core worker --beat --loglevel=info"
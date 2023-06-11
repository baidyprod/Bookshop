FROM python:3.10

WORKDIR /app

COPY backend/store/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD sh -c "sleep 20 && python manage.py migrate && python manage.py runserver 0.0.0.0:8001"

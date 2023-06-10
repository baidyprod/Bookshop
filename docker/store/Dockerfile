FROM python:3.10

WORKDIR /app

COPY requirements/store/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/store/ .

EXPOSE 8001

CMD sh -c "sleep 20 && python manage.py migrate && python manage.py runserver 0.0.0.0:8001"

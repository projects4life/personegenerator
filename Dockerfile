FROM python:alpine3.17
# FROM python

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt awscli==1.27.79

COPY templates/ ./templates

COPY static/  ./static

COPY app.py .

COPY blueprints/ ./blueprints

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

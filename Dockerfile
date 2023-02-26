FROM python:alpine3.17

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt awscli==1.27.79

COPY templates/ ./templates

COPY static/  ./static

COPY app.py .

ENTRYPOINT [ "./app.py" ]
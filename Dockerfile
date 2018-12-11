FROM python:3.7

WORKDIR /home/application

COPY requirements.txt requirements.txt
COPY app app
COPY migrations migrations
COPY application.py config.py .env ./

ENV FLASK_APP application.py
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]

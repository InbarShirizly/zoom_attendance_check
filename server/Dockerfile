FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
ADD . /app

RUN pip install --upgrade pip && pip install python-dev && pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]
FROM python:3

WORKDIR /app

ADD . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "bittrex_app_src.app", "--host", "0.0.0.0"]
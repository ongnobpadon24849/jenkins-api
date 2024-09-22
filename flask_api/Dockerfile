FROM python:3.9-alpine

WORKDIR /flask_api

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
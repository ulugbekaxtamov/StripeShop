FROM python:3.10-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .


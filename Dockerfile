FROM python:3.10-buster
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
#COPY pyproject.toml /code/
COPY requirements.txt /code/
#RUN #poetry install
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

#CMD python manage.py runserver
FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system
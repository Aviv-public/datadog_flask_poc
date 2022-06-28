FROM python:3.8-slim
ADD . /code
WORKDIR /code
ENV PYTHONPATH /code

RUN pip install pipenv
RUN pipenv install
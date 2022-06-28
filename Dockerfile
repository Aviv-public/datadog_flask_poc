FROM python:3.7-slim
ADD . /code
WORKDIR /code
ENV PYTHONPATH /code

RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv"]
CMD ["run", "ddtrace-run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

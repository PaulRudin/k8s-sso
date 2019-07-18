FROM python:3.7.3-stretch AS prod

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install --deploy --system

COPY app /usr/src/app

CMD ["python", "./app.py"]

FROM prod AS dev

RUN pipenv install --dev --system

CMD ["adev", "runserver", "--app-factory", "make_app", "app.py"]

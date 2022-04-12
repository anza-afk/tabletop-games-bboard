FROM python:3.10.4-slim as base

ARG HOMEDIR=/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile --dev

WORKDIR ${HOMEDIR}

COPY . ${HOMEDIR}

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
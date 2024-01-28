FROM node:latest as tailwind-builder

WORKDIR /app
COPY ./app/package.json ./app/package-lock.json .
RUN npm install
COPY ./app/. .
RUN npm run build

FROM python:3.11-slim-buster

#RUN useradd django

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn==20.0.4"
RUN pip install poetry

# Install the project requirements.
COPY pyproject.toml poetry.lock /
WORKDIR /
RUN poetry export -o requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

#RUN chown django:django /app

#COPY --chown=django:django ./app/. .
COPY ./app/. .
COPY --from=tailwind-builder /app/static/main.css /app/static/main.css

#USER django

RUN python manage.py collectstatic --noinput --clear

CMD gunicorn studiowiki.wsgi:application

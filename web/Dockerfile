# --------------------------------------------BASE IMAGE--------------------------------------------

FROM python:3.8.1-slim-buster as builder

# Setup work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# --------------------------------------------MAIN IMAGE--------------------------------------------

FROM python:3.8.1-slim-buster

RUN mkdir -p /home/app

# Create required directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# Copy entrypoint.sh to created DB schema
COPY ./entrypoint.sh $APP_HOME

# Copy project
COPY . $APP_HOME

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

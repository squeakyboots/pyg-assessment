FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/root/.poetry/bin"
ENV WORKDIR="/app"

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing \
    apt-utils \
    apt-transport-https \
    build-essential

#Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Nicer Bash Setup
RUN sed -i "s/# export LS_OPTIONS/export LS_OPTIONS/" /root/.bashrc
RUN sed -i "s/# alias ll/alias ll/" /root/.bashrc
RUN sed -i "s/# alias ls/alias ls/" /root/.bashrc
RUN sed -i "s/# alias l/alias l/" /root/.bashrc

# Install and set up cron job and related tools
# I couldn't get cron to start in the container so had the app just run a while loop
#RUN apt-get -y install cron
#RUN apt-get -y install vim
#COPY app_cron /etc/cron.d/app_cron
#RUN chmod 0644 /etc/cron.d/app_cron
#RUN crontab /etc/cron.d/app_cron
#CMD /etc/init.d/crond start

# App
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Install poetry packages before copying entire directory to take advantage of docker layer caching
COPY ./poetry.lock ${WORKDIR}/poetry.lock
COPY ./pyproject.toml ${WORKDIR}/pyproject.toml

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . ${WORKDIR}

CMD /bin/bash

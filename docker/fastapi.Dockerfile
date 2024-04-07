FROM python:3.10-slim-bullseye
LABEL Storyly Backend Demo

ENV TYPE=PROD
ADD . /code
WORKDIR /code
COPY requirements.txt requirements.txt
RUN apt-get update \
    && apt-get install -y gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
FROM python:3.9-slim AS build

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /hall

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY collector.py .
COPY hall-exporter.py .

FROM python:3.9-slim AS run

RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y; \
    rm -rf /var/lib/apt/lists/*; \
    apt-get clean

WORKDIR /hall

COPY --from=build /opt/venv /opt/venv
COPY --from=build /hall .

ENV TZ="Europe/Paris"
ENV PATH="/opt/venv/bin:$PATH"

CMD [ "hall-exporter.py" ]
ENTRYPOINT [ "python" ]

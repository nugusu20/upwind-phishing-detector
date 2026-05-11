FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /analysis

COPY monitor.py /analysis/monitor.py
COPY samples/ /samples/

RUN mkdir -p /sandbox_area /logs /reports

CMD ["python3", "/analysis/monitor.py"]

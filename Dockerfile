FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY samples/ samples/

EXPOSE 5000

CMD ["python3", "src/web_app.py"]

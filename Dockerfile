FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY search.py .
COPY app.py .

EXPOSE 2225

CMD ["python", "app.py"]

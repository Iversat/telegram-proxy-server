FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -O https://raw.githubusercontent.com/alexbers/mtprotoproxy/master/mtprotoproxy.py

COPY . .

CMD ["python3", "main.py"]
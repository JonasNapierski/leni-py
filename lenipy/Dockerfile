FROM python:3.8.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
EXPOSE 6248

CMD ["uvicorn","--port","6248", "Leni:app"]

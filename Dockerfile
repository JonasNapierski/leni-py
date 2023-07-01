FROM python:3.8.10

WORKDIR /app

COPY lenipy/requirements.txt .

RUN pip install -r requirements.txt

COPY . .
EXPOSE 6248

WORKDIR lenipy/
CMD ["uvicorn","--port","6248", "Leni:app"]

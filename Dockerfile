FROM alpine:latest

RUN apk update 
RUN apk upgrade
RUN apk add python3 python3-pip

WORKDIR /app

COPY lenipy/requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .
EXPOSE 6248

WORKDIR lenipy/

CMD ["uvicorn","--port","6248", "Leni:app"]

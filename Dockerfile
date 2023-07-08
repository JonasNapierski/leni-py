FROM alpine:latest

LABEL maintainer="Jonas Napierski gihub@jonas-napierski.de"

RUN apk update 
RUN apk upgrade
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN python3 --version | echo
COPY lenipy/requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN apk add git 
RUN apk add cmake
RUN git clone --recursive https://github.com/pytorch/pytorch \
    && cd pytorch && python setup.py install

WORKDIR /app
COPY . .
EXPOSE 6248

WORKDIR lenipy/

CMD ["uvicorn","--port","6248", "Leni:app"]

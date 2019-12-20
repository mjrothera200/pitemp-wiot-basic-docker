FROM arm32v6/alpine:latest
COPY app/. /app
WORKDIR /app
RUN apk add build-base
RUN apk add --no-cache python3
RUN apk add --no-cache python3-dev
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip
RUN pip3 install -r requirements.txt
CMD python3 iot-temp.py

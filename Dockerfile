FROM python:3.10-alpine

WORKDIR /home/text-processing

RUN apk update && apk add --no-cache build-base gcc vim htop && pip install --upgrade pip && pip install --upgrade wheel

COPY . .

RUN mkdir -p logs && sh install.sh

VOLUME logs

CMD ["sh", "start.sh"]

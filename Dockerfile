FROM python:3.11

WORKDIR /usr/src/faa-api

ADD requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

RUN chmod +x ./run.sh

EXPOSE 8001

CMD ["bash", "./run.sh"]

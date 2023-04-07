FROM python:3.9.2-slim-buster

WORKDIR /app

COPY main.py ./
COPY gsheets.py ./
COPY requirements.txt ./
COPY config.ini ./
COPY YOUR_SESSION_NAME.session ./
COPY noted-wares-377821-051686d108d1.json ./

RUN pip install -r requirements.txt
CMD ["python", "main.py"]
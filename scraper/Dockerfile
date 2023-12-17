#use base image
FROM python:3.12-slim-bookworm

#set working dir
WORKDIR /app

#copy requirements
COPY requirements.txt .

#Install requirements
RUN pip install --no-cache-dir -r requirements.txt 

#Copy over the entire scrapy project
COPY . .

WORKDIR /app/price_tracker

CMD ["python", "run_spiders.py"]
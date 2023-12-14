
#base python image
FROM python:3.12-alpine

#set working dir
WORKDIR /app

#copy requirements
COPY requirements.txt .

#Install requirements
RUN pip install --no-cache-dir -r requirements.txt 

#Copy over the entire scrapy project
COPY . . 

#initial commaand to run scrapy 
CMD [ "scrapy", "crawl", "amazon" ]
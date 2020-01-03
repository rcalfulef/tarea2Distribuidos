FROM ubuntu:latest

MAINTAINER Andres calfulef "rcalfulef@gmail.com"

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip 
RUN pip install pipenv
RUN pipenv install 
RUN pipenv shell


RUN mkdir archivos

COPY server.py /
COPY Pipfile /

CMD ["python3","-u" ,"./server.py"]
FROM ubuntu:20.04

# Update apt cache
RUN apt-get update

# Install Python3 and Pip3
RUN apt-get install python3 python3-distutils -y 
RUN apt-get install python3-pip -y

# Install dev & build packages
RUN apt-get install python3-dev build-essential -y

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -t lib -r requirements.txt

COPY ./src /app/src

WORKDIR /app/src

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
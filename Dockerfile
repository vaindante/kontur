FROM ubuntu:17.10
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get update

RUN apt-get install -y python3.6
RUN apt-get install -y python3.6-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3.6-venv
RUN apt-get install -y git
RUN apt-get install -y locales

# Делаем локаль юникодной
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

WORKDIR /app

COPY requirements.txt .
RUN python3.6 -m pip install pip --upgrade
RUN pip3.6 install -r requirements.txt

COPY . .

#CMD bash
ENV GENERATE_REPORT=''
CMD output=$(py.test -m "$TESTS") && chmod -R 777 ./reports && echo "$output"
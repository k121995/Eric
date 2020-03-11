
# Install Python
FROM python:latest as api
RUN apt-get update && apt-get install -y swig && apt-get install -y --no-install-recommends nano sudo iputils-ping && rm -rf /var/lib/apt/lists/*

# Create folder code and copy all files
RUN mkdir /home/Eric
ADD requirements.txt /home/Eric
ADD . /home/Eric
WORKDIR /home/Eric
RUN ls -al
# Install Python
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt


FROM ubuntu:latest

ARG work_dir=/tmp/

RUN apt update

ADD requirements.txt $work_dir

RUN apt-get update && apt-get install -y python3.6
RUN apt-get install -y python3.6
RUN apt-get install -y python3-distutils
RUN apt-get install -y python3-pip

RUN pip install --upgrade pip

WORKDIR $work_dir
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "/usr/local/lab_management/run.py"]
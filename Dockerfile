FROM ubuntu:16.04
RUN apt-get update
FROM python:2
ADD indeed_worker.py /
ADD pass_data.py /
ADD sort_file.py /
ADD requirements.txt /
RUN apt-get update && apt-get -y install redis-server
RUN pip install --no-cache-dir -r requirements.txt
CMD rq-dashboard --port=5000
CMD redis-server
# CMD [ "python", "" ]
# CMD [ "python", "./my_script.py" ]
EXPOSE 5000

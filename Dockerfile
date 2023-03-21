FROM python:3.10
WORKDIR ./
COPY ./requirement.txt ./requirement.txt
RUN pip install -r requirement.txt
COPY ./kafka_consumer.py ./kafka_consumer.py
CMD ["python3","./kafka_consumer.py"]

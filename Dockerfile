FROM python:3

ADD process_sales.py /app/
ADD requirements.txt /app/
ADD SalesProcessing /app/SalesProcessing

RUN pip install -r /app/requirements.txt

WORKDIR "/app"

#CMD [ "cd","app"]
CMD [ "python", "./process_sales.py" ]
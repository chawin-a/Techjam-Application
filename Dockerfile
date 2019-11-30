FROM python:3.7-buster

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY webapp /app/webapp
RUN gcc /app/webapp/closestpair.c -o /app/webapp/closestpair

WORKDIR /app
EXPOSE 8000
CMD ["python", "-m", "webapp"]

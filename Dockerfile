FROM python:3.10
WORKDIR /app

RUN pip install flask
RUN pip install mysql-connector-python

RUN mkdir -p controllers fonts static templates

COPY controllers/ controllers/
COPY app.py app.py
COPY fonts/ fonts/
COPY templates/ templates/
COPY static/ static/

RUN chmod -R a+rwx controllers fonts static templates
CMD ["python","app.py", "0.0.0.0:5000"]
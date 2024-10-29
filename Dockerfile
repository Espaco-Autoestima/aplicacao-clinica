FROM python:3.10
WORKDIR /app

RUN pip install flask
RUN pip install mysql-connector-python

RUN mkdir -p controllers static templates tests

COPY controllers/ controllers/
COPY app.py app.py
COPY tests/ tests/
COPY templates/ templates/
COPY static/ static/

RUN chmod -R a+rwx controllers static templates tests
CMD ["python","app.py", "0.0.0.0:5000"]
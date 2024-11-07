FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p controllers static templates tests

COPY controllers/ controllers/
COPY app.py app.py
COPY tests/ tests/
COPY templates/ templates/
COPY static/ static/

RUN chmod -R a+rwx controllers static templates tests
CMD ["python","app.py"]
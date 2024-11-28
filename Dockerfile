FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p controllers static templates tests

COPY controllers/ controllers/
COPY app.py app.py
COPY pytest.ini pytest.ini
COPY tests/ tests/
COPY templates/ templates/
COPY static/ static/

RUN chmod -R a+rwx controllers tests templates static
CMD ["python","app.py"]
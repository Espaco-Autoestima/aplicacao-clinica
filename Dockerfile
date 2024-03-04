FROM python:3.7-slim
WORKDIR /espaco-autoestima
RUN pip install flask
RUN pip install flask-mysqldb
COPY app.py app.py
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","app.py"]
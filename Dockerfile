FROM python:3.7-slim
RUN pip install flask
RUN pip install mysql-connector-python
COPY clientes.py clientes.py
RUN mkdir templates
RUN mkdir static
COPY templates/*  /templates/
COPY templates/static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","clientes.py"]

FROM python:3.7-slim
WORKDIR /espaco-autoestima
RUN pip install flask
# Não está rodando o comando abaixo na execução do comando docker-compose up
RUN pip install flask-mysqldb
COPY clientes.py clientes.py
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","clientes.py"]

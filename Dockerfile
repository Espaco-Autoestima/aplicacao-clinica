FROM python:3.7-slim
WORKDIR /app
RUN pip install flask
RUN pip install mysql-connector-python
COPY controllers/* /app/controllers
COPY app.py /app/app.py
COPY calendario/* /app/calendario/
COPY fonts/* /app/fonts/
RUN mkdir /app/templates
RUN mkdir /app/static
COPY templates/* /app/templates/
COPY static/* /app/static/
RUN chmod -R a+rwx /app/templates
RUN chmod -R a+rwx /app/static
CMD ["python","app.py"]
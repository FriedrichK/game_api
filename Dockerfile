FROM python:3.10-alpine
EXPOSE 8000
COPY . /opt/api
WORKDIR /opt/api
RUN pip install -r requirements.txt
RUN /opt/api/manage.py makemigrations
RUN /opt/api/manage.py migrate
ENTRYPOINT /opt/api/manage.py runserver 0.0.0.0:8000
FROM python:3.6.4-jessie
RUN mkdir -p  /opt/app/web
COPY web/requirements.txt /opt/app/
RUN pip install --no-cache-dir -r /opt/app/requirements.txt
RUN pip install gunicorn
RUN pip install flup
COPY web /opt/app
EXPOSE 8000
WORKDIR /opt/app
ENTRYPOINT gunicorn wsgi:app  --bind 0.0.0.0:8000  --workers 4

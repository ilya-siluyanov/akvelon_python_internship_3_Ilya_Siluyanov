FROM python:3.9

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD python src/manage.py makemigrations && \
    python src/manage.py migrate && \
    cd src && \
    DEBUG=False gunicorn src.wsgi -b 0.0.0.0:8000


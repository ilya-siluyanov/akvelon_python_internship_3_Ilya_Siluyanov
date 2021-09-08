FROM python:3.9

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD python src/manage.py makemigrations && \
    python src/manage.py migrate && \
    DEBUG=False python src/manage.py runserver 0.0.0.0:${SERVER_PORT:-8000}


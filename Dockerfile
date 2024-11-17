FROM python:3.12
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# RUN apt-get update && apt-get install -y redis-server
# RUN apt-get update && apt-get install -y supervisor

# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000 6379

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && celery -A config worker --beat -l INFO && -A python manage.py runserver 0.0.0.0:8000"]
# CMD ["/usr/bin/supervisord"]

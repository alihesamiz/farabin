FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/

# RUN apt-get update && apt-get install -y redis-server
# RUN apt-get update && apt-get install -y supervisor

# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf



EXPOSE 8000 6379

CMD ["sh", "entrypoint.sh"]

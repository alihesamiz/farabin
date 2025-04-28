FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y gettext 
RUN apt-get install -y redis-server 
RUN apt-get install -y graphviz libgraphviz-dev

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

EXPOSE 8000 6379

CMD ["sh", "entrypoint.sh"]

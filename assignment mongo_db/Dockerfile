FROM python:3.9.7-slim
RUN apt update && sleep 10 && \
    apt install build-essential libzbar-dev curl -y && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
COPY . /code
CMD [ "python", "app.py" ]

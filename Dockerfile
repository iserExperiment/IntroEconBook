FROM python:3.10-bullseye

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

EXPOSE 8000

CMD ["otree", "devserver", "0.0.0.0:8000"]

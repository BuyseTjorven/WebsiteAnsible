FROM python:3.10.7-alpine3.16 as build-image
WORKDIR /app
COPY requirements.txt .
RUN apk update
RUN apk add sshpass
RUN pip install cffi
RUN pip install -r requirements.txt
RUN ansible-galaxy collection install arensb.truenas
COPY . .

CMD ["python", "main.py"]

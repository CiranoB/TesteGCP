FROM python:3.11.10-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000:8000

CMD ["fastapi", "run"]
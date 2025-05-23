FROM python:alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--port", "5000", "--host", "0.0.0.0", "--workers", "4"]
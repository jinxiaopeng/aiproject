FROM python:3.9-slim as builder

WORKDIR /install

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app.py .
COPY requirements.txt .

RUN mkdir -p templates
COPY src/templates/login.html templates/

EXPOSE 8081

CMD ["python", "app.py"]

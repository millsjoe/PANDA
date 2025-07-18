FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY example_patients.json .
COPY example_appointments.json .

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py"] 
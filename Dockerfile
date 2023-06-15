FROM python:3.9-alpine
WORKDIR /app
COPY src/pynamer/. /app
COPY requirements/production.txt .
RUN ["pip", "install",  "--no-cache-dir", "-r", "production.txt"]
RUN pip install --upgrade pip setuptools wheel
CMD ["python", "pynamer.py"]

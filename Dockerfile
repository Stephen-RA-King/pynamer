FROM python:3.9-alpine
WORKDIR /apps/pynamer/
COPY src/pynamer/. .
COPY requirements/development.txt .
RUN ["pip", "install",  "--no-cache-dir", "-r", "development.txt"]
CMD ["python", "pynamer.py"]

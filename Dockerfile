FROM python:3.9


WORKDIR /app

COPY src /app/src
COPY requirements/production.txt .
COPY setup.py .
COPY setup.cfg .
COPY pyproject.toml .
COPY README.md .


# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"


RUN pip install --upgrade pip setuptools wheel
RUN ["pip", "install",  "--no-cache-dir", "-r", "production.txt"]

# Install your local package in editable mode
RUN pip install -e .

CMD ["pynamer"]

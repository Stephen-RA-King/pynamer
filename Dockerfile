FROM python:3.11-slim

WORKDIR /app

# Copy the local application and build files to the container
COPY src /app/src
COPY requirements/production.txt .
COPY setup.py .
COPY setup.cfg .
COPY pyproject.toml .
COPY README.md .

# Create and activate a virtual environment
RUN ["python", "-m", "venv", "/venv"]
ENV PATH="/venv/bin:$PATH"

# Update the python build tools
RUN ["pip", "install", "--no-cache-dir", "--upgrade", "pip", "setuptools", "wheel"]

# Install the additional production requirements if any
RUN ["pip", "install", "--no-cache-dir", "-r", "production.txt"]

# Install your local package in editable mode
RUN ["pip", "install", "--no-cache-dir", "-e", "."]

# Run the application
CMD ["pynamer"]

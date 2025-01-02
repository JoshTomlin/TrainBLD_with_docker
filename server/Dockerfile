FROM python:3.9-slim
LABEL authors="rotohands"

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y install gcc

# Set the working directory


# Create and activate a virtual environment
WORKDIR /app

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install psycopg2
# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=flask_analyze_server.py

# Create a non-root user and switch to it
RUN useradd -m flaskuser
USER flaskuser
ENV PYTHONPATH=/app

# Copy the current directory contents into the container at /app
COPY . /app
# Run the application
CMD ["venv/bin/python", "-u", "-m",  "flask", "run", "--host=0.0.0.0", "--port=8080"]
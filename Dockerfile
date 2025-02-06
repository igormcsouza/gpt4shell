# Use the official Python image from the Docker Hub
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
RUN pip install poetry==2.0.1 \
  && poetry config virtualenvs.create false  \
  && poetry install --only main --no-interaction --no-ansi

# Set the entrypoint to your script
ENTRYPOINT ["poetry", "--quiet", "run", "gpt"]

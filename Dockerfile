# Dockerfile

# Use the official Python image as the base image
FROM python:3.9

RUN apt-get update && \
    apt-get install -y default-mysql-client
# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]

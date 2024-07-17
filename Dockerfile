# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . /app

# Install the required dependencies
RUN pip install flask

# Expose port number
EXPOSE 3000

# start the server
CMD ["python", "app.py"]

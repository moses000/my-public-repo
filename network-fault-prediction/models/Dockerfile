# # Use Python 3.8 as the base image
# FROM python:3.8-slim

# # Set the working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

# # Copy the Python code
# COPY . /app

# # Expose the port for the Flask app
# EXPOSE 5000

# # Command to run the Flask app
# CMD ["python", "predict.py"]


# Start with a base Python image
FROM python:3.9-slim

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Python application
CMD ["python", "predict.py"]

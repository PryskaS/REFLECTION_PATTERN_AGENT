# Stage 1: Use an official lightweight Python image as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the file with dependencies first
COPY requirements.txt .

# Install the dependencies
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of application code into the container
COPY . .

# Tell Docker that the container will listen on port 8001
EXPOSE 8001

# The command to run application when the container starts
# Use 0.0.0.0 to make the server accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
# Use an existing Python base image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the required files to the container
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variables from the .env file
ENV FLASK_APP=api.py
ENV $(cat .env | xargs)

# Expose port 8000
EXPOSE 8000

# Run the command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

# Base image
FROM python:3.8-slim

# Set working directory 
WORKDIR /app

# Copy requirements file 
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project to the container
COPY . /app

# Expose the port 
EXPOSE 5000

# Optional: Specify environment variables if needed
# ENV MONGO_URI="mongodb://mongo:27017/mydb"

# Run my application
CMD ["python", "taskpdf.py"]  # update this after

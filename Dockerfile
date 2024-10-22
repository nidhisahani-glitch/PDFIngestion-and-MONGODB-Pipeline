# Base image with Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to leverage Docker layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose any ports if needed (MongoDB default is 27017, but only if running locally)
# EXPOSE 27017

# Run the PDF processing pipeline
CMD ["python", "taskpdf.py"]

FROM python:3.12-slim

# Set working directory
WORKDIR /refactoredapp

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application file
COPY app_refactored2.py .

# Create directories for data and output
RUN mkdir -p /data /output

# Run the application
ENTRYPOINT ["python3", "./app_refactored2.py"]
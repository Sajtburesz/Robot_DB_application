# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /robot_db

# Copy the current directory contents into the container at /app
COPY . /robot_db/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

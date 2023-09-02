# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /realtyhive

# Copy the requirements file into the container
COPY ./requirements.txt /realtyhive/requirements.txt

RUN pip install -r requirements.txt

COPY . /realtyhive/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
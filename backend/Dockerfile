FROM python:3.11-alpine AS development


# Set environment variables
ENV DockerHOME=/home/app/backend

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p $DockerHOME
RUN mkdir $DockerHOME/staticfiles

# Where your backend app lives in your docker container
WORKDIR $DockerHOME

# Copy the current directory contents into the container at $DockerHOME
COPY .. $DockerHOME

# Install necessary packages on the container
RUN apk update && apk add --no-cache gcc python3-dev postgresql-dev gettext musl-dev icu-data-full

# Install any needed packages specified in requirements.txt and upgrade pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Make port available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python3", "manage.py", "runserver", "8000"]


#######################################################################################
FROM python:3.11-alpine AS production


# Set environment variables
ENV DockerHOME=/home/app/backend

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p $DockerHOME
RUN mkdir $DockerHOME/staticfiles

# Where your backend app lives in your docker container
WORKDIR $DockerHOME

# Copy the current directory contents into the container at $DockerHOME
COPY .. $DockerHOME

# Install necessary packages on the container
RUN apk update && apk add --no-cache gcc python3-dev musl-dev icu-data-full postgresql-dev gettext

# Install any needed packages specified in requirements.txt and upgrade pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Make port available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]

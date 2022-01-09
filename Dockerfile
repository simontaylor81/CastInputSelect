# Use an official Python runtime as a base image
# Use the Alpine variant to keep image size down
FROM python:3-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
# Must also install gcc etc. (required for building netifaces) and
# then remove it again to avoid bloat.
# Must be all one RUN command or docker stores the intermediate result,
# nullifying the benefit of removing stuff.
RUN apk add --no-cache build-base linux-headers \
  && pip install -r requirements.txt \
  && apk del build-base linux-headers

# Make port 80 available to the world outside this container
#EXPOSE 80

# Run the command. -u is for unbuffered stdout/stderr
CMD ["python", "-u", "CastInputSelect.py", "--show-chromecast-debug"]

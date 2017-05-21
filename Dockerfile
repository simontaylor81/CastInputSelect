# Use an official Python runtime as a base image
FROM simontaylor81/python27-alpine-gcc

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80

CMD ["python", "CastInputSelect.py"]
